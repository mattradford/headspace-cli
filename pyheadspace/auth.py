import base64
import json
import re
import time

import requests
from rich.console import Console

LOGIN_URL = "https://www.headspace.com/login"
AUTH_URL = "https://auth.headspace.com/co/authenticate"
BEARER_TOKEN_URL = "https://auth.headspace.com/authorize"

session = requests.Session()
console = Console()


def normalize_bearer_token(token):
    token = (token or "").strip()
    if not token:
        raise ValueError("Bearer token is empty")
    if token.lower().startswith("bearer "):
        return token
    return f"bearer {token}"


def extract_hsngjwt_from_cookie(cookie_value):
    cookie_value = (cookie_value or "").strip()
    if not cookie_value:
        raise ValueError("Cookie value is empty")

    match = re.search(r"(?:^|;\s*)hsngjwt=([^;\s]+)", cookie_value, re.IGNORECASE)
    if match:
        return match.group(1)

    if cookie_value.lower().startswith("eyj"):
        return cookie_value

    raise ValueError("Could not find hsngjwt cookie value")


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "Origin": "https://www.headspace.com",
    "Connection": "keep-alive",
    "TE": "Trailers",
}

session.headers.update(headers)

def get_client_id():
    for attempt in range(5):
        response = session.get(LOGIN_URL)
        text = response.text or ""

        if response.status_code == 429 or "rate limit" in text.lower():
            if attempt < 4:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(
                "Headspace login is temporarily rate-limited. Please wait a few minutes and try again."
            )

        old_match = re.search(r'"clientId":"([^"]+)"', text)
        if old_match:
            return old_match.group(1)

        alt_match = re.search(r'"client_id":"([^"]+)"', text)
        if alt_match:
            return alt_match.group(1)

        new_match = re.search(r'atob\("([^"]+)"\)', text)
        if new_match:
            payload = json.loads(
                base64.b64decode(new_match.group(1)).decode("utf-8")
            )
            for key in ("client", "clientConfig", "data"):
                client = payload.get(key, {})
                if isinstance(client, dict):
                    if "id" in client:
                        return client["id"]
            if "clientId" in payload:
                return payload["clientId"]
            if "client_id" in payload:
                return payload["client_id"]

        if attempt < 4:
            time.sleep(1)
            continue

    raise RuntimeError("Unable to extract client ID from login page")

def prompt():
    email = console.input(f"[bold red]?[/] Email: ")
    password = console.input(f"[bold red]?[/] Password: ", password=True)

    return email, password


def get_bearer_token(client_id, login_ticket):
    params = {
        "client_id": client_id,
        "response_type": "token",
        "response_mode": "web_message",
        "redirect_uri": "https://www.headspace.com/auth",
        "scope": "openid email",
        "audience": "https://api.prod.headspace.com",
        "realm": "User-Password-Headspace",
        "login_ticket": login_ticket,
        "prompt": "none",
    }
    response = session.get(BEARER_TOKEN_URL, params=params)
    html = response.text
    match = re.search(r'"access_token":"(.+?)"', html)
    if not match:
        raise RuntimeError("Unable to extract bearer token from login response")
    return match.group(1)


def authenticate(email, password):
    try:
        client_id = get_client_id()
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        return False

    data = {
        "client_id": client_id,
        "username": email,
        "password": password,
        "realm": "User-Password-Headspace",
        "credential_type": "http://auth0.com/oauth/grant-type/password-realm",
    }
    response = session.post(
        AUTH_URL,
        headers=headers,
        data=json.dumps(data),
    )
    resp_json: dict = response.json()
    try:
        login_ticket = resp_json["login_ticket"]
    except KeyError:
        if "error" in resp_json.keys():
            console.print(resp_json["error"], style="red")
            if "error_description" in resp_json.keys():
                console.print(resp_json["error_description"])
        else:
            console.print(resp_json)
        return False
    try:
        bearer_token = get_bearer_token(data["client_id"], login_ticket)
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        return False
    bearer_token = "bearer " + bearer_token
    return bearer_token

# headspace-cli
[![PyPI version](https://badge.fury.io/py/pyheadspace.svg)](https://badge.fury.io/py/pyheadspace)

Command line script to download Headspace packs, singles, and everyday meditations.

<p align="center">

<img src = "https://user-images.githubusercontent.com/57002207/147270294-de0ec3f9-7bfa-4c63-84de-b4239fd4995e.gif" alt = "demo">
</p>

- [👶 Dependencies](#-dependencies)
- [🛠️ Installation](#️-installation)
- [🔐 Authentication](#-authentication)
- [🚀 Usage](#-usage)

## 👶 Dependencies
* [Python 3.7 or higher](https://www.python.org/downloads/)

## 🛠️ Installation
```sh
pip install --upgrade pyheadspace
```

If installing with `pip install --user`, add the user-level bin directory to your `PATH`:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

Or install with [pipx](https://github.com/pypa/pipx):

```sh
pipx install pyheadspace
```

### This tool is only meant for personal use. Do not use this for piracy.

## 🔐 Authentication

Headspace has blocked the legacy direct email/password login flow used by older CLI versions. The CLI can no longer complete a normal `headspace login` with just an email and password.

Use one of the supported browser-backed login methods instead:

### Option 1: use a browser session cookie

1. Open https://my.headspace.com in your browser and sign in.
2. Open browser devtools.
3. Go to the cookie storage for the site.
4. Copy the value of the `hsngjwt` cookie.
5. Run:

```sh
headspace login --cookie '<hsngjwt value>'
```

### Option 2: use a bearer token you already have

```sh
headspace login --token 'bearer <token>'
```

### Option 3: old flow (no longer works)

```sh
headspace login
```

This older flow is no longer accepted by Headspace and will fail with `unauthorized_client` / `Cross origin login not allowed.`

Once valid authentication is stored, the CLI will write the bearer token to the local token file and future commands can run without re-entering the token.

## 🚀 Usage

## Download all packs at once
```sh
# Download all packs with each session of duration 15 minutes
headspace pack --all --duration 15

# Download all packs with session duration of 10 & 20 minutes
headspace pack --all --duration 10 --duration 15
```

**Exclude specific packs from downloading:**

To exclude packs, use the `--exclude` option.

It expects a text file containing one pack URL per line.

**links.txt**:
```txt
https://my.headspace.com/modes/meditate/content/154
https://my.headspace.com/modes/meditate/content/150
```

**command**:
```sh
headspace packs --all --exclude links.txt
```

This downloads all packs except the ones listed in `links.txt`.

## Downloading a specific pack
```sh
headspace pack <PACK_URL> [Options]
```

**Basic usage**:
```sh
# Download all sessions at 15 minutes
headspace pack https://my.headspace.com/modes/meditate/content/151 --duration 15

# Download sessions of multiple durations
headspace pack https://my.headspace.com/modes/meditate/content/151 -d 20 -d 15
```

**Options**:
```sh
--id INTEGER         ID of video.
-d, --duration TEXT  Duration or list of duration.
-a --author INTEGER  The author ID for the audio.
--no_meditation      Only download meditation sessions without techniques.
--no_techniques      Only download techniques and not meditation sessions.
--out TEXT           Download directory.
--all                Download all Headspace packs.
-e, --exclude TEXT   Use with `--all`; file containing pack URLs to skip.
--help               Show this message and exit.
```

## Download a single session
```sh
headspace download <SESSION_URL> [options]
```

**Basic usage**:
```sh
headspace download https://my.headspace.com/player/204?authorId=1&contentId=151&contentType=COURSE&mode=meditate&trackingName=Course&startIndex=1 --duration 15
```

**Options**:
```sh
--out TEXT           Download directory.
--id INTEGER         ID of the video. Not required if URL is provided.
-d, --duration       Duration or list of duration.
--help               Show this message and exit.
```

## Download everyday meditations
```sh
headspace everyday [OPTIONS]
```

**Basic usage**:
```sh
# Download today's meditation
headspace everyday

# Download everyday meditations for a specific date range
# DATE FORMAT: yyyy-mm-dd
headspace everyday --from 2021-03-01 --to 2021-03-20

# Prefix each daily meditation filename with its date
headspace everyday --prepend-date
```

**Options**:
```sh
--from TEXT          Start date. FORMAT: yyyy-mm-dd
--to TEXT            End date. FORMAT: yyyy-mm-dd
--prepend-date       Prefix each downloaded file with the date.
-d, --duration TEXT  Duration or list of duration.
--out TEXT           Download directory.
--help               Show this message and exit.
```

## Changing language preference
By default, the language is English. You can change it to other languages supported by Headspace.

Other languages:
- de-DE
- es-ES
- fr-FR
- pt-BR

To change the language, set the environment variable `HEADSPACE_LANG`:

- Bash / fish: `export HEADSPACE_LANG="fr-FR"`
- PowerShell: `$env:HEADSPACE_LANG="fr-FR"`

**If you encounter any issue or bug, open a new issue on [GitHub](https://github.com/yashrathi-git/pyHeadspace).**







**If you encounter any issue or bug, open a new issue on [github](https://github.com/yashrathi-git/pyHeadspace)**




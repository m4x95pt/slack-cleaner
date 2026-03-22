# slack-cleaner

Automatically deletes all non-pinned messages from all Slack channels every hour.

## How it works

A GitHub Actions workflow runs every hour, triggering a Python script that:

1. Fetches all public and private channels the bot is a member of
2. For each channel, fetches all messages
3. Skips pinned messages
4. Deletes everything else

## Setup

### 1. Slack App permissions

Go to [api.slack.com/apps](https://api.slack.com/apps) → your app → **OAuth & Permissions** and add these **Bot Token Scopes**:

- `channels:history`
- `channels:read`
- `chat:write`
- `groups:history`
- `groups:read`
- `pins:read`

Reinstall the app to your workspace after adding scopes.

### 2. GitHub Secret

Add the following secret to this repository under **Settings → Secrets and variables → Actions**:

| Secret            | Value                                  |
| ----------------- | -------------------------------------- |
| `SLACK_BOT_TOKEN` | Your Bot User OAuth Token (`xoxb-...`) |

### 3. Deploy

Push this repo to GitHub. The workflow will run automatically every hour.
You can also trigger it manually via **Actions → Clean Slack Messages → Run workflow**.

## Files

- `clean_slack.py` — main script
- `.github/workflows/clean-slack.yml` — GitHub Actions workflow

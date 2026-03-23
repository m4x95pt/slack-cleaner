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

Go to [api.slack.com/apps](https://api.slack.com/apps) → your app → **OAuth & Permissions**.

Add these **Bot Token Scopes**:

- `channels:history`
- `channels:read`
- `groups:history`
- `groups:read`
- `pins:read`

Add these **User Token Scopes**:

- `chat:write`
- `channels:history`
- `channels:read`
- `groups:history`
- `groups:read`
- `pins:read`

After adding the scopes, click **Reinstall to Workspace** at the top of the page.

> **Why User Token?** The Slack API only allows deleting messages sent by others when using a User OAuth Token (`xoxp-`). A Bot Token (`xoxb-`) can only delete the bot's own messages.

### 2. Invite the bot to your channels

In each Slack channel you want to clean, invite the app:

1. Click the channel name → **Integrations** → **Add apps**
2. Search for your app and add it

### 3. GitHub Secret

Add the following secret to this repository under **Settings → Secrets and variables → Actions**:

| Secret            | Value                                  |
| ----------------- | -------------------------------------- |
| `SLACK_BOT_TOKEN` | Your **User** OAuth Token (`xoxp-...`) |

### 4. Deploy

Push this repo to GitHub. The workflow will run automatically every hour.
You can also trigger it manually via **Actions → Clean Slack Messages → Run workflow**.

## Files

- `clean_slack.py` — main script
- `.github/workflows/clean-slack.yml` — GitHub Actions workflow

import os
import time
import requests

SLACK_TOKEN = os.environ["SLACK_BOT_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {SLACK_TOKEN}",
    "Content-Type": "application/json",
}

def slack_get(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def slack_post(url, data=None):
    r = requests.post(url, headers=HEADERS, json=data)
    r.raise_for_status()
    return r.json()

def get_channels():
    channels = []
    cursor = None
    while True:
        params = {"types": "public_channel,private_channel", "limit": 200}
        if cursor:
            params["cursor"] = cursor
        data = slack_get("https://slack.com/api/conversations.list", params)
        if not data.get("ok"):
            print(f"Error fetching channels: {data.get('error')}")
            break
        for ch in data.get("channels", []):
            if ch.get("is_member"):
                channels.append(ch)
        cursor = data.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return channels

def get_pinned_ts(channel_id):
    data = slack_get("https://slack.com/api/pins.list", {"channel": channel_id})
    if not data.get("ok"):
        return set()
    pinned = set()
    for item in data.get("items", []):
        msg = item.get("message", {})
        if msg.get("ts"):
            pinned.add(msg["ts"])
    return pinned

def get_messages(channel_id):
    messages = []
    cursor = None
    while True:
        params = {"channel": channel_id, "limit": 200}
        if cursor:
            params["cursor"] = cursor
        data = slack_get("https://slack.com/api/conversations.history", params)
        if not data.get("ok"):
            print(f"  Error fetching messages: {data.get('error')}")
            break
        messages.extend(data.get("messages", []))
        cursor = data.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return messages

def delete_message(channel_id, ts):
    data = slack_post("https://slack.com/api/chat.delete", {
        "channel": channel_id,
        "ts": ts,
    })
    if not data.get("ok"):
        print(f"  ❌ Failed to delete {ts}: {data.get('error')}")
    return data.get("ok")

def clean_channel(channel):
    channel_id   = channel["id"]
    channel_name = channel.get("name", channel_id)
    print(f"\n#{channel_name}")

    pinned   = get_pinned_ts(channel_id)
    messages = get_messages(channel_id)
    print(f"  Found {len(messages)} message(s), {len(pinned)} pinned")

    deleted = 0
    skipped = 0
    for msg in messages:
        ts = msg.get("ts")
        if ts in pinned:
            skipped += 1
            continue
        ok = delete_message(channel_id, ts)
        if ok:
            deleted += 1
        time.sleep(1.2)

    print(f"  Deleted: {deleted} | Skipped (pinned): {skipped}")

def main():
    print("🧹 Starting Slack cleaner...")
    channels = get_channels()
    print(f"Found {len(channels)} channel(s).")
    for ch in channels:
        clean_channel(ch)
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
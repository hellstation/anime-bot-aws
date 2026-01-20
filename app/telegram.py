import os
import time
import requests
import boto3
import json

def get_credentials():
    try:
        client = boto3.client("secretsmanager")
        response = client.get_secret_value(SecretId="anime-notifier-secrets")
        secrets = json.loads(response["SecretString"])
        return secrets["TELEGRAM_BOT_TOKEN"], secrets["TELEGRAM_CHAT_ID"]
    except Exception:
        return os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")

BOT_TOKEN, CHAT_ID = get_credentials()

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("Credentials not found")

def send_message(text: str, chat_id=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id or CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload, timeout=10).raise_for_status()

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 30} if offset else {"timeout": 30}
    return requests.get(url, params=params, timeout=35).json()

def format_anime_info(anime):
    title = anime["title"]["english"] or anime["title"]["romaji"]
    description = anime.get("description", "No description.").replace("<br>", "\n").replace("<b>", "*").replace("</b>", "*")

    info = f"🎬 *{title}*\n\n"
    info += f"📊 *Status:* {anime.get('status', 'Unknown')}\n"
    if anime.get('season') and anime.get('seasonYear'):
        info += f"📅 *Season:* {anime['season']} {anime['seasonYear']}\n"
    if anime.get('episodes'):
        info += f"🎞️ *Episodes:* {anime['episodes']}\n"
    if anime.get('genres'):
        info += f"🏷️ *Genres:* {', '.join(anime['genres'])}\n"
    if anime.get('averageScore'):
        info += f"⭐ *Score:* {anime['averageScore']}/100\n"

    if anime.get('nextAiringEpisode'):
        next_ep = anime['nextAiringEpisode']
        airing_time = time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime(next_ep['airingAt']))
        info += f"📺 *Next Episode:* {next_ep['episode']} (airs {airing_time})\n"

    info += f"\n📝 *Description:*\n{description[:500]}{'...' if len(description) > 500 else ''}"
    return info

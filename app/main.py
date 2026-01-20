import logging
import time
from anilist import get_airing_anime, search_anime
from telegram import send_message, get_updates, format_anime_info
from state import load_state, save_state

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_new_episodes():
    try:
        logger.info("Checking for new episodes...")
        state = load_state()
        anime_list = get_airing_anime()

        for anime in anime_list:
            next_ep = anime.get("nextAiringEpisode")
            if not next_ep:
                continue

            anime_id = str(anime["id"])
            episode = next_ep["episode"]

            if state.get(anime_id) == episode:
                continue

            title = anime["title"]["romaji"]
            message = f"🎬 *New episode announced!*\n{title}\nEpisode: {episode}"
            send_message(message)
            logger.info(f"Sent notification for {title} episode {episode}")
            state[anime_id] = episode

        save_state(state)
    except Exception as e:
        logger.error(f"Error checking episodes: {e}")

def handle_anime_search(text, chat_id):
    try:
        anime_name = text.lower().replace('/anime', '').replace('/search', '').strip()

        if not anime_name:
            send_message("Please specify anime name after command. Example: `/anime Naruto`", chat_id)
            return

        logger.info(f"Searching: {anime_name}")
        anime = search_anime(anime_name)

        if anime:
            message = format_anime_info(anime)
            send_message(message, chat_id)
        else:
            send_message(f"Anime '{anime_name}' not found. Try different name.", chat_id)

    except Exception as e:
        logger.error(f"Search error: {e}")
        send_message("Error searching anime. Try again later.", chat_id)

def process_message(message):
    try:
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()

        if not text:
            return

        logger.info(f"Message: '{text}' from {chat_id}")

        if text.startswith('/anime') or text.startswith('/search'):
            handle_anime_search(text, chat_id)
        elif text.startswith('/start'):
            welcome = """
🎬 *Hello! I'm anime bot!*

I can:
• Search anime information
• Send automatic notifications for new episodes

📝 *How to use:*
Send: `/anime [english name]`
Example: `/anime Naruto` or `/anime Attack on Titan`

⏰ Auto notifications come every hour!
            """
            send_message(welcome, chat_id)
        elif text.startswith('/help'):
            help_text = """
📚 *Commands:*

• `/anime [name]` - search anime info
• `/start` - show welcome message
• `/help` - show this help

Examples:
`/anime Naruto`
`/anime Death Note`
            """
            send_message(help_text, chat_id)
        else:
            handle_anime_search(text, chat_id)

    except Exception as e:
        logger.error(f"Message error: {e}")

def main():
    logger.info("Starting bot...")
    offset = None
    send_message("🤖 Bot started! Send `/help` or anime name.")

    while True:
        try:
            current_time = time.time()
            if not hasattr(main, 'last_check') or current_time - main.last_check > 3600:
                check_new_episodes()
                main.last_check = current_time

            updates = get_updates(offset)
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                if "message" in update:
                    process_message(update["message"])

            time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Bot stopped")
            break
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

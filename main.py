import ptbot
import os
import random
from dotenv import load_dotenv
from pytimeparse import parse


def render_progressbar(
    total, iteration, prefix="", suffix="", length=30, fill="█", zfill="░"
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)


def last_message(author_id, bot):
    bot.send_message(author_id, "Время вышло")


def notify_progress(secs_left, author_id, id, total, bot):
    message = "Осталось {} секунд.\n {}".format(
        secs_left, render_progressbar(total, total - secs_left)
    )
    bot.update_message(author_id, id, message)


def reply(chat_id, time, bot):
    seconds = parse(time)
    total_sec = seconds
    message_id = bot.send_message(chat_id, "Запускаю таймер")
    bot.create_countdown(
        seconds,
        notify_progress,
        author_id=chat_id,
        id=message_id,
        total=total_sec,
        bot=bot,
    )
    bot.create_timer(seconds, last_message, author_id=chat_id, bot=bot)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()


if __name__ == "__main__":
    main()

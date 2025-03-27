import ptbot
import os
import random
from decouple import config
from pytimeparse import parse


TG_TOKEN = config("TG_TOKEN")
BOT = ptbot.Bot(TG_TOKEN)


def render_progressbar(
    total, iteration, prefix="", suffix="", length=30, fill="█", zfill="░"
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)


def last_message(author_id):
    BOT.send_message(author_id, "Время вышло")


def notify_progress(secs_left, author_id, id, total):
    message = "Осталось {} секунд.\n {}".format(
        secs_left, render_progressbar(total, total - secs_left)
    )
    BOT.update_message(author_id, id, message)


def reply(chat_id, time):
    seconds = parse(time)
    total_sec = seconds
    message_id = BOT.send_message(chat_id, "Запускаю таймер")
    BOT.create_countdown(
        seconds, notify_progress, author_id=chat_id, id=message_id, total=total_sec
    )
    BOT.create_timer(seconds, last_message, author_id=chat_id)


def main():
    BOT.reply_on_message(reply)
    BOT.run_bot()


if __name__ == "__main__":
    main()

from aiogram.filters import Command # для боту
from aiogram.types.bot_command import BotCommand #для пользователей

START_BOT_COMMAND =BotCommand(command="start",description="Запустити бота")
BOOKS_BOT_COMMAND =BotCommand(command="books",description="Показати список книг")
BOOKS_BOT_CREATE_COMMAND =BotCommand(command="add_book",description="Додати книгу")

BOOKS_COMMAND = Command("books")
BOOKS_CREATE_COMMAND = Command("add_book")
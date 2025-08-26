import asyncio
import json
import logging
import sys
from state import BookForm
from aiogram.fsm.context import FSMContext
from keyboard import books_keyboard_markup
from conf import BOT_TOKEN,ADMIN_ID
from keyboard import BookCallback
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove
import cohere
from commands import (
BOOKS_CREATE_COMMAND,
    START_BOT_COMMAND,
    BOOKS_BOT_COMMAND,
    BOOKS_BOT_CREATE_COMMAND,
    BOOKS_COMMAND,
)




class Book:
    def __init__(
        self,
        name: str,
        description: str,
        rating: float,
        genre: str,
        authors: list[str],
        poster: str | None = None,
    ):
        self.name = name
        self.description = description
        self.rating = rating
        self.genre = genre
        self.authors = authors
        self.poster = poster



TOKEN = BOT_TOKEN #Наш токен!!!
dp = Dispatcher()



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")



def get_books(file_path: str = "data.json", book_id: int | None = None):
    with open(file_path, "r", encoding="utf-8") as fp:
        books = json.load(fp)
        if book_id is not None and 0 <= book_id < len(books):
            return books[book_id]
        return books


def add_books(book:dict,file_path:str =  "data.json"):
    books = get_books()
    if books:
        books.append(book)
        with open(file_path, "w", encoding="utf-8") as fp:
            json.dump(
                books,
                fp,
                indent=4,
                ensure_ascii=False

            )



@dp.message(BOOKS_COMMAND)
async def books(message: Message) -> None:
    data = get_books()
    markup = books_keyboard_markup(book_list=data)
    await message.answer("Список книг. Нажмите название для деталей", reply_markup=markup)


@dp.message(BOOKS_CREATE_COMMAND)
async def book_create(message: Message, state: FSMContext) -> None:
    if message.from_user.id ==int(ADMIN_ID):
        await state.set_state(BookForm.name)
        await message.answer(f"Введіть назву книги", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Только Администратор может добавлять книги", reply_markup=ReplyKeyboardRemove())
@dp.message(BookForm.name)
async def book_name (message:Message,state:FSMContext)->None:
    await state.update_data(name=message.text)
    await state.set_state(BookForm.description)
    await message.answer("Введите опис книги",reply_markup=ReplyKeyboardRemove())



@dp.message(BookForm.description)
async def book_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(BookForm.rating)
    await message.answer("Введите рейтинг книги от 1 до 10", reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.rating)
async def book_rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=message.text)
    await state.set_state(BookForm.genre)
    await message.answer("Введите жанр книги ", reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.genre)
async def book_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(BookForm.authors)
    await message.answer("Введите авторов книги.\n"+
                         html.bold("Обязательно кома та отступ после неё"),
                         reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.authors)
async def book_authors(message: Message, state: FSMContext) -> None:
    await state.update_data(authors=[x for x in message.text.split(",")])
    await state.set_state(BookForm.poster)
    await message.answer("Введите ссылку на обложку книги.", reply_markup=ReplyKeyboardRemove())

@dp.message(BookForm.poster)
async def book_poster(message:Message,state:FSMContext)-> None:
    data = await  state.update_data(poster=message.text)
    book = Book(**data)
    add_books(book.model_dump())
    await state.clear()
    await message.answer(f"Книгу {book.name} успешно добавленно ", reply_markup=ReplyKeyboardRemove())


@dp.callback_query(BookCallback.filter())
async def callback_book(callback: CallbackQuery, callback_data: BookCallback) -> None:
    book_id = callback_data.id
    book_data = get_books(book_id=book_id)
    book = Book(**book_data)

    text = (
        f"📖 Книга: {book.name}\n"
        f"📝 Описание: {book.description}\n"
        f"⭐ Рейтинг: {book.rating}\n"
        f"📚 Жанр: {book.genre}\n"
        f"✍ Авторы: {', '.join(book.authors)}\n"
    )

    try:
        if book.poster:
            await callback.message.answer_photo(
                photo=URLInputFile(
                    book.poster,
                    filename=f"{book.name}_cover.{book.poster.split('.')[-1]}",
                ),
                caption=text,
            )
        else:
            await callback.message.answer(text)
    except Exception as e:
        await callback.message.answer(text)
        logging.error(f"Failed to load image for book {book.name}: {e}")

    await callback.answer()


def generate_text(prompt):
    co = cohere.ClientV2(api_key="fVHBPOpecGhg864OTKYkFikoZWx3Ujr8PPRRkkmx")
    res = co.chat(
    model="command-a-03-2025",
messages=[
{
"role": "user",
"content": f"{prompt}",
}
],
)
    return res.message.content[0].text


@dp.message()
async def echo_handler(message: Message):
    user_input = message.text
    await message.answer(f"Спасибо{message.from_user.full_name}"
    f"Генерирую ответ, подожди...")
    generated_text = generate_text(user_input)
    await message.answer(generated_text)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(
        [
            START_BOT_COMMAND,
            BOOKS_BOT_COMMAND,
            BOOKS_BOT_CREATE_COMMAND,
        ]
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from keyboards.keyboards import create_search_result_keyboard, create_docs_keyboard, create_navigation_keyboard
from lexicon.lexicon import LEXICON, LEXICON_DOCS
from config.config import FSMSearch
from model.model import default_search, doc_search


user_router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять ему приветственное сообщение
@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@user_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/default"
# и отправлять пользователю сообщение о вводе запроса для поиска по всем документам
@user_router.message(Command(commands="default"))
async def process_default_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["insert_text"] + "все документы")
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/choice"
# и отправлять пользователю клавиатуру для выбора документа
@user_router.message(Command(commands="choice"))
async def process_choice_command(message: Message):
    await message.answer(
        text=LEXICON["choice_doc"],
        reply_markup=create_docs_keyboard()
    )


# Этот хэндлер будет срабатывать выбор документа из списка,
# отправлять пользователю сообщение о вводе запроса
# и сохранять информацию о выборе пользователя
@user_router.callback_query(F.data.in_(LEXICON_DOCS))
async def process_doc_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=LEXICON["insert_text"] + LEXICON_DOCS[callback.data],
        reply_markup=create_navigation_keyboard("backtochoice"))
    await state.set_state(FSMSearch.doc_state[callback.data])
    await state.update_data(doc = callback.data)


# Этот хэндлер будет срабатывать на возвращение к стартовому сообщению
@user_router.callback_query(F.data == "backtostart")
async def process_backtostart_press(callback: CallbackQuery):
    await callback.message.answer(LEXICON["/start"])


# Этот хэндлер будет срабатывать на возвращение к выбору документа
@user_router.callback_query(F.data == "backtochoice")
async def process_backtochoice_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["choice_doc"],
        reply_markup=create_docs_keyboard()
    )


# Этот хэндлер будет срабатывать на возвращение к результатам поиска по всем документам
@user_router.callback_query(F.data == "backtolist", StateFilter(default_state))
async def process_backtolist_def_press(callback: CallbackQuery, db: dict):
    await callback.message.edit_text(
            text=LEXICON["search_result"] + "всех документов",
            reply_markup=create_search_result_keyboard(db[callback.from_user.id], "backtostart")
        )


# Этот хэндлер будет срабатывать на возвращение к результатам поиска по выбранному документу
@user_router.callback_query(F.data == "backtolist", ~StateFilter(default_state))
async def process_backtolist_doc_press(callback: CallbackQuery, db: dict, state: FSMContext):
    doc = await state.get_data()
    await callback.message.edit_text(
            text=LEXICON["search_result"] + "документа " + LEXICON_DOCS[doc['doc']],
            reply_markup=create_search_result_keyboard(db[callback.from_user.id], "backtochoice")
        )


# Этот хэндлер будет срабатывать на сообщение без выбранного документа,
# выполнять поиск и показывать результаты в виде клавиатуры
@user_router.message(StateFilter(default_state))
async def process_default_search_insert(message: Message, docs: dict, db: dict, embeddings: dict):
    db[message.from_user.id] = default_search(message.text, docs, embeddings)
    await message.answer(
            text=LEXICON["search_result"] + "всех документов",
            reply_markup=create_search_result_keyboard(db[message.from_user.id], "backtostart")
        )


# Этот хэндлер будет срабатывать на сообщение с выбранным документом,
# выполнять поиск и показывать результаты в виде клавиатуры
@user_router.message(~StateFilter(default_state))
async def process_doc_search_insert(message: Message, state: FSMContext, docs: dict, db: dict, embeddings: dict):
    doc = await state.get_data()
    db[message.from_user.id] = doc_search(message.text, doc["doc"], docs, embeddings)
    text = LEXICON["search_result"] + "документа " + LEXICON_DOCS[doc["doc"]]
    await message.answer(
            text=text,
            reply_markup=create_search_result_keyboard(db[message.from_user.id], "backtochoice")
        )
    

# Этот хэндлер будет срабатывать на нажатие кнопки клавиатуры с результатами поиска
# и открывать выбранный пункт для прочтения
@user_router.callback_query()
async def process_page_press(callback: CallbackQuery, db: dict):
    await callback.message.edit_text(
        text = db[callback.from_user.id][callback.data][0],
        reply_markup=create_navigation_keyboard("backtolist")
    )


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON, LEXICON_DOCS


# Функция создает клавиатуру из результатов поиска модели
def create_search_result_keyboard(search_list: dict, back: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for punkt in search_list:
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{punkt} - {search_list[punkt][0]}",
                callback_data=str(punkt)
            )
        )
    kb_builder.row(InlineKeyboardButton(text=LEXICON[back], callback_data=back))
    return kb_builder.as_markup()


# Функция создает клавиатуру из списка документов
def create_docs_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in LEXICON_DOCS:
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{button} - {LEXICON_DOCS[button]}",
                callback_data=str(button)
            )
        )
    kb_builder.row(InlineKeyboardButton(text=LEXICON["backtostart"], callback_data="backtostart"))
    return kb_builder.as_markup()


# Функция создает клавиатуру с навигацией
def create_navigation_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button,
            )
            for button in buttons
        ]
    )
    return kb_builder.as_markup()
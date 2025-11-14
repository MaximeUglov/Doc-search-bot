from dataclasses import dataclass
from environs import Env
from aiogram.fsm.state import State, StatesGroup


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class LogSettings:
    level: str
    format: str


@dataclass
class Config:
    bot: TgBot
    log: LogSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(token=env("BOT_TOKEN")),
        log=LogSettings(level=env("LOG_LEVEL"), format=env("LOG_FORMAT")),
    )

class FSMSearch(StatesGroup):
    PGO_search = State()
    PRV_search = State()
    PSR_search = State()

    doc_state = {"PGO": PGO_search,
                 "PRV": PRV_search,
                 "PSR": PSR_search
    }

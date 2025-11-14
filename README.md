## Телеграм-бот для поиска пунктов правил по охране труда
С помощью такого бота можно искать по смыслу пункты правил из загруженных документов. На данный момент доступны три, можно добавить новые или удалить настоящие. Поиск может осуществляться как по всем документам, так и по выбранному одному для более точного ответа. Ответ приходит в виде списка из 10 пунктов наиболее подходящих по смыслу.

### Запуск бота

1. Установить [Python 3.12.10](https://www.python.org/downloads/)   
2. Склонировать репозиторий.
3. Создать бота в Telegram через BotFather, отправив команду "/newbot", и придумать название боту. В ответ придет токен, который нужно сохранить.
4. Полученный токен скопировать в файл .env
5. Создать виртуальное окружение и установить библиотеки, указанные в requirements.txt   
6. Запустить файл main.py и открыть чат с ботом.

### Описание файлов

>__main.ipynb__ - описание признаков, их обработка, создание и обучение модели.   
__requirements.txt__ - список используемых библиотек.   
__submission.csv__ - прогноз модели.   
__text_to_embeddings.ipynb__ - обработка текстов.    
   
__data__ - папка с исходными данными, таблицы разделены на обучающую и тестовую выборки.
>>__Combined_News_DJIA.csv__ - содержит топ 25 заголовков новостей.    
__DJIA_Table.csv__ - содержит данные биржи.    
__Reddit_News.csv__ - неранжированные заголовки новостей.    
__sample_submission.csv__ - форма ответа для соревнования.    

### Библиотеки

<div id="badges">
  <img src="https://img.shields.io/badge/pandas-black?style=for-the-badge&logo=pandas"/>
  <img src="https://img.shields.io/badge/numpy-black?style=for-the-badge&logo=numpy"/>
  <img src="https://img.shields.io/badge/aiogram-black?style=for-the-badge&logo=aiogram"/>
  <img src="https://img.shields.io/badge/sentence_transformers-black?style=for-the-badge&logo=sentence_transformers"/>
</div>

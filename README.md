# khakas-asr

Сбор и подготовка данных (предложений) на хакасском языке для будущего датасета Common Voice / ASR.

## Структура проекта

- [`main.py`](main.py) — скачивает датасет предложений `adeshkin/kjh-asr-sents` с Hugging Face, добавляет новые предложения из локального txt-файла, убирает дубликаты и заливает обновлённый датасет обратно на Hugging Face Hub.
- [`prepare_sentences_for_common_voice.py`](prepare_sentences_for_common_voice.py) — фильтрует и чистит "сырые" предложения (по длине, количеству слогов, допустимым символам, наличию цифр/аббревиатур и т.д.), готовя их к формату Common Voice.
- `requirements.txt` — зависимости проекта.
- `.env` — локальный файл с токеном Hugging Face (**не коммитить**, уже в `.gitignore`). Пример структуры — в `.env.example`.

## Настройка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Создать `.env` на основе `.env.example` и вписать свой токен Hugging Face с правом записи (write):

```bash
cp .env.example .env
```

⚠️ Токен в `.env` даёт право пушить датасет на Hugging Face от вашего имени — храните его только локально и не публикуйте нигде (чаты, скриншоты, публичные репозитории).

## Важно про пути

В обоих скриптах пути к входным/выходным файлам (`/home/adeshkin/Downloads/...`) захардкожены под конкретную машину — перед запуском на другой машине их нужно поменять.

## Полезные ссылки (контекст задачи Common Voice)

- Обсуждение добавления хакасского языка в Common Voice: https://github.com/common-voice/common-voice/issues/5278
- Локализация интерфейса (Pontoon): https://pontoon.mozilla.org/kjh/common-voice/ (нужно довести перевод нескольких строк до 100%, сверяясь при необходимости с русской локализацией: https://pontoon.mozilla.org/ru/common-voice/)
- После перевода откроется страница сбора предложений: https://commonvoice.mozilla.org/kjh/write — нужно набрать 750 предложений, не защищённых авторским правом, чтобы язык стал доступен для сбора голосовых записей.
- Референс похожего проекта для башкирского языка (синтетический датасет + ASR-модель на w2v-bert-2.0): https://huggingface.co/datasets/AigizK/bashkort_voice, https://huggingface.co/AigizK/w2v-bert-2.0-bashkort-russian-omnivoice

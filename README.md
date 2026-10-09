# Автотесты Кинопоиск (UI + API)

Дипломный проект: автотесты поиска, карточки фильма и фильтров
(kinopoisk.ru — UI, kinopoisk.dev — API).

## Установка
pip install -r requirements.txt
cp .env.example .env  # укажите API_KEY с kinopoisk.dev

## Запуск
python -m pytest tests/api          # API-тесты
python -m pytest tests/ui           # UI-тесты
python -m pytest                    # всё вместе
allure serve allure-results         # отчёт Allure
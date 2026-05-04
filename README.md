# GitHub User Finder

**Автор:** Чубуков Владимир Сергеевич

## Описание

GitHub User Finder — это десктопное GUI-приложение на Python, которое позволяет:
- Искать пользователей GitHub по логину.
- Просматривать основную информацию (кол-во репозиториев, имя, подписчиков).
- Добавлять пользователей в избранное.
- Сохранять избранных пользователей в JSON-файл.
- Открывать профиль избранного пользователя в браузере.

## Как использовать GitHub API

Приложение использует **GitHub REST API v3**:
- Эндпоинт: `GET https://api.github.com/users/IccYtIce111`
- Ответ содержит информацию о пользователе: `login`, `name`, `public_repos`, `followers`, `html_url` и т.д.
- API работает без аутентификации (до 60 запросов в час с одного IP). Для увеличения лимита можно добавить токен в заголовок `Authorization`.

### Пример запроса через `requests`:

```python
import requests
response = requests.get("https://api.github.com/users/octocat")
print(response.json()["login"])  # octocat

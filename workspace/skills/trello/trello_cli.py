#!/usr/bin/env python3
"""
Trello CLI для nanobot навыка.
Кроссплатформенный интерфейс к Trello REST API.
"""

import json
import sys
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Any, Dict, Optional


def load_secrets() -> Dict[str, str]:
    """Загружает API ключ и токен из trello.json в той же директории."""
    skill_dir = Path(__file__).parent.resolve()
    secrets_file = skill_dir / 'trello.json'

    if not secrets_file.exists():
        print(f"Ошибка: файл {secrets_file} не найден", file=sys.stderr)
        sys.exit(1)

    try:
        with open(secrets_file, 'r', encoding='utf-8') as f:
            secrets = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}", file=sys.stderr)
        sys.exit(1)

    api_key = secrets.get('api_key')
    token = secrets.get('token')

    if not api_key or not token:
        print("Ошибка: в trello.json отсутствуют api_key или token", file=sys.stderr)
        sys.exit(1)

    return {'api_key': api_key, 'token': token}


def trello_get(path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """Выполняет GET-запрос к Trello API."""
    base_url = 'https://api.trello.com/1'
    url = f"{base_url}/{path.lstrip('/')}"

    secrets = load_secrets()
    query = {
        'key': secrets['api_key'],
        'token': secrets['token'],
    }
    if params:
        query.update(params)

    full_url = f"{url}?{urllib.parse.urlencode(query)}"

    try:
        with urllib.request.urlopen(full_url, timeout=10) as response:
            content_type = response.headers.get('Content-Type', '')
            data = response.read()
            if 'application/json' in content_type:
                return json.loads(data.decode('utf-8'))
            else:
                return data.decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"HTTP ошибка {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Ошибка сети: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def trello_post(path: str, data: Dict[str, Any]) -> Any:
    """Выполняет POST-запрос к Trello API."""
    base_url = 'https://api.trello.com/1'
    url = f"{base_url}/{path.lstrip('/')}"

    secrets = load_secrets()
    query = {
        'key': secrets['api_key'],
        'token': secrets['token'],
    }
    full_url = f"{url}?{urllib.parse.urlencode(query)}"

    post_data = urllib.parse.urlencode(data).encode('utf-8')

    try:
        req = urllib.request.Request(full_url, data=post_data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req, timeout=10) as response:
            content_type = response.headers.get('Content-Type', '')
            resp_data = response.read()
            if 'application/json' in content_type:
                return json.loads(resp_data.decode('utf-8'))
            else:
                return resp_data.decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"HTTP ошибка {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Ошибка сети: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def trello_put(path: str, data: Dict[str, Any]) -> Any:
    """Выполняет PUT-запрос к Trello API."""
    base_url = 'https://api.trello.com/1'
    url = f"{base_url}/{path.lstrip('/')}"

    secrets = load_secrets()
    query = {
        'key': secrets['api_key'],
        'token': secrets['token'],
    }
    full_url = f"{url}?{urllib.parse.urlencode(query)}"

    post_data = urllib.parse.urlencode(data).encode('utf-8')

    try:
        req = urllib.request.Request(full_url, data=post_data, method='PUT')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req, timeout=10) as response:
            content_type = response.headers.get('Content-Type', '')
            resp_data = response.read()
            if 'application/json' in content_type:
                return json.loads(resp_data.decode('utf-8'))
            else:
                return resp_data.decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"HTTP ошибка {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Ошибка сети: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list_boards():
    """Список досок пользователя."""
    boards = trello_get('members/me/boards')
    for board in boards:
        print(f"- {board['name']} (ID: {board['id']})")


def cmd_list_lists(board_id: str):
    """Список списков в доске."""
    lists = trello_get(f'boards/{board_id}/lists')
    for lst in lists:
        print(f"- {lst['name']} (ID: {lst['id']})")


def cmd_list_cards(list_id: str):
    """Список карточек в списке."""
    cards = trello_get(f'lists/{list_id}/cards')
    for card in cards:
        print(f"- {card['name']} (ID: {card['id']})")
        if card.get('desc'):
            print(f"  Описание: {card['desc'][:50]}{'...' if len(card['desc']) > 50 else ''}")


def cmd_create_card(list_id: str, name: str, desc: str = ''):
    """Создание карточки."""
    data = {'idList': list_id, 'name': name}
    if desc:
        data['desc'] = desc
    card = trello_post('cards', data)
    print(f"Карточка создана: {card['name']} (ID: {card['id']})")


def cmd_move_card(card_id: str, list_id: str):
    """Перемещение карточки в другой список."""
    card = trello_put(f'cards/{card_id}', {'idList': list_id})
    print(f"Карточка {card_id} перемещена в список {list_id}")


def cmd_add_comment(card_id: str, text: str):
    """Добавление комментария к карточке."""
    action = trello_post(f'cards/{card_id}/actions/comments', {'text': text})
    print(f"Комментарий добавлен: {action['data']['text']}")


def cmd_archive_card(card_id: str):
    """Архивация карточки."""
    card = trello_put(f'cards/{card_id}', {'closed': True})
    print(f"Карточка {card_id} архивирована")


def main():
    if len(sys.argv) < 2:
        print("Использование: trello_cli.py <команда> [аргументы]", file=sys.stderr)
        print("Команды:", file=sys.stderr)
        print("  list-boards", file=sys.stderr)
        print("  list-lists <board_id>", file=sys.stderr)
        print("  list-cards <list_id>", file=sys.stderr)
        print("  create-card <list_id> <name> [description]", file=sys.stderr)
        print("  move-card <card_id> <list_id>", file=sys.stderr)
        print("  add-comment <card_id> <text>", file=sys.stderr)
        print("  archive-card <card_id>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == 'list-boards':
        cmd_list_boards()
    elif cmd == 'list-lists':
        if len(args) != 1:
            print("Ошибка: требуется board_id", file=sys.stderr)
            sys.exit(1)
        cmd_list_lists(args[0])
    elif cmd == 'list-cards':
        if len(args) != 1:
            print("Ошибка: требуется list_id", file=sys.stderr)
            sys.exit(1)
        cmd_list_cards(args[0])
    elif cmd == 'create-card':
        if len(args) < 2:
            print("Ошибка: требуется list_id и name", file=sys.stderr)
            sys.exit(1)
        list_id = args[0]
        name = args[1]
        desc = args[2] if len(args) > 2 else ''
        cmd_create_card(list_id, name, desc)
    elif cmd == 'move-card':
        if len(args) != 2:
            print("Ошибка: требуется card_id и list_id", file=sys.stderr)
            sys.exit(1)
        cmd_move_card(args[0], args[1])
    elif cmd == 'add-comment':
        if len(args) < 2:
            print("Ошибка: требуется card_id и text", file=sys.stderr)
            sys.exit(1)
        cmd_add_comment(args[0], args[1])
    elif cmd == 'archive-card':
        if len(args) != 1:
            print("Ошибка: требуется card_id", file=sys.stderr)
            sys.exit(1)
        cmd_archive_card(args[0])
    else:
        print(f"Неизвестная команда: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

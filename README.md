# nanobot-skills

Навыки для AI-ассистента nanobot.

## 📦 Содержимое

- `clawdhub/` — поиск и установка скиллов из ClawHub
- `gog/` — интеграция с Google Workspace (Gmail, Calendar, Drive)
- `openmeteo/` — точный прогноз погоды через Open-Meteo API
- `summarize/` — суммаризация текста/видео/подкастов
- `weather/` — погода через wttr.in (fallback)

## 🚀 Установка

Скопируйте папку нужного скилла в:
```
~/.nanobot/workspace/skills/
```

## 📖 Документация

Каждый скилл содержит файл `SKILL.md` с описанием и примерами использования.

## 🔧 Требования

- nanobot >= 0.1.0
- Для некоторых скиллов требуются внешние утилиты (curl, gh и т.д.)

## 📝 Лицензия

MIT
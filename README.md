# Telegram-bot-for-viewing-the-weather
Telegram bot that shows sunrise, sunset, day length and current weather for any city. Uses Yandex Geocoder for coordinates, Sunrise-Sunset API v2 for solar data, and Open-Meteo for live weather. Built with Python, pyTelegramBotAPI and requests. Handles unknown cities and API errors.

# Telegram Weather Bot: Sunrise, Sunset & Current Weather

A simple Telegram bot that accepts a city name and returns:
- 🌅 Sunrise and sunset time
- ☀️ Day length
- 🌡 Current temperature
- ☁️ Weather description
- 💧 Precipitation and humidity

## Features

- Get coordinates for any city via Yandex Geocoder
- Calculate sunrise, sunset and day length via Sunrise-Sunset API v2
- Fetch current weather via Open-Meteo API
- Timezone-aware output (local time for the requested location)
- Handles unknown cities and API errors gracefully

## Tech Stack

- **Python 3.10+**
- **pyTelegramBotAPI** — Telegram Bot API wrapper
- **requests** — HTTP client for API calls
- **python-dotenv** — loading secrets from `.env`

## APIs Used

| API | Purpose |
|---|---|
| [Yandex Geocoder](https://developer.tech.yandex.ru/) | Convert city name to coordinates |
| [Sunrise-Sunset API v2](https://sunrise-sunset.org/api) | Sunrise, sunset, day length |
| [Open-Meteo](https://open-meteo.com/) | Current temperature, weather, precipitation, humidity |

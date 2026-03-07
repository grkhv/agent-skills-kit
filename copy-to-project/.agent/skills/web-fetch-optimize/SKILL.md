---
name: web-fetch-optimize
description: Оптимизация получения веб-контента через markdown.new.
---

При необходимости получить контент веб-страницы, сначала попробуй сервис markdown.new:

## Использование

```bash
curl -s 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d '{"url": "<URL>", "method": "auto"}'
```

Ответ — JSON с полем `content` (чистый markdown). Экономит ~80% токенов по сравнению с HTML.

## Fallback

Если markdown.new недоступен (ошибка, таймаут, пустой ответ) — используй стандартный метод получения контента.

## Ограничения

- 500 запросов/день на IP
- Только публичные URL (без авторизации)
- JS-heavy страницы: используй `"method": "browser"`

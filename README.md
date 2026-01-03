# MyOS - Кастомная ОС с интерфейсом в стиле Windows 11

## Быстрый старт

### 1. Посмотреть preview (прямо сейчас)
Открой `preview/index.html` в браузере — полноценный рабочий интерфейс.

### 2. Получить ISO для VirtualBox

**Вариант A: Через GitHub (рекомендуется)**
1. Создай репозиторий на GitHub
2. Загрузи туда эту папку
3. Зайди в Actions → Build MyOS ISO → Run workflow
4. Скачай готовый ISO из Artifacts

**Вариант B: Локально на Linux/WSL**
```bash
./build.sh
```

### 3. Запуск в VirtualBox
1. Создай VM: Type=Linux, Version=Other Linux (64-bit)
2. RAM: 512MB+, Video: 32MB+
3. Storage → Add optical drive → Выбери myos.iso
4. Start!

## Что внутри
- Рабочий стол в стиле Windows 11
- Панель задач по центру
- Меню Пуск с поиском
- Приложения: Files, Notepad, Terminal, Settings, Paint, Calculator, Browser
- Перетаскиваемые окна
- Контекстное меню
- Смена обоев

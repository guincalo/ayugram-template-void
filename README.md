# AyuGram Desktop для Void Linux
[English](README-en.md)

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png)

Неофициальная сборка мода [AyuGram](https://github.com/AyuGram/AyuGramDesktop) под **Void Linux**.

> **Это форк.** Он не разрабатывает AyuGram — только поддерживает шаблон пакета Void в актуальном состоянии относительно релизов [AyuGram](https://github.com/AyuGram/AyuGramDesktop/releases) и собирает его автоматически: ежедневный бот поднимает версию шаблона при выходе нового релиза, а GitHub Actions собирает `.xbps` пакеты для glibc и musl на каждый бамп.

## Установка из Releases

1. Перейди на страницу [Releases](https://github.com/guincalo/ayugram-template-void/releases)
2. Скачай последний релиз для нужной архитектуры:
   - **x86_64-glibc** — для большинства систем
   - **x86_64-musl** — для musl-based Void Linux
3. Установи пакет:

```bash
cd <директория_с_скачанным_файлом>
# Создаём индекс репозитория (необходимо перед установкой)
xbps-rindex -a *.xbps
# Устанавливаем пакет
sudo xbps-install --repository=$PWD ayugram-desktop
```

Для обновления позже: скачай новый `.xbps` в ту же директорию и выполни `xbps-rindex -a *.xbps && sudo xbps-install --repository=$PWD -u ayugram-desktop`.

## Сборка вручную

```bash
# Клонируем шаблон
git clone https://github.com/guincalo/ayugram-template-void.git

# Клонируем официальный void-packages
git clone https://github.com/void-linux/void-packages.git

# Копируем исходники пакета
cp -r ayugram-template-void/srcpkgs/* void-packages/srcpkgs/

# Переходим в каталог
cd void-packages

# Собираем пакет (занимает ~10-40 минут в зависимости от машины)
./xbps-src pkg ayugram-desktop

# Устанавливаем собранный пакет
sudo xbps-install -R hostdir/binpkgs ayugram-desktop
```

## Автоматизация

- **update.yml** запускается ежедневно: сравнивает версию шаблона с последним тегом AyuGram и коммитит бамп версии, если вышел новый релиз.
- **build.yml** собирает `ayugram-desktop` для x86_64-glibc и x86_64-musl при каждом изменении шаблона и прикрепляет пакеты к GitHub Release.

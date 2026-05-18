# AyuGram Desktop для Void Linux
[English](README-en.md)

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png) ![VoidBTW](.forgejo/void-logo.png)

Неофициальная сборка мода [AyuGram](https://github.com/AyuGram/AyuGramDesktop) под **Void Linux**.

## Два способа установки

### Способ 1 — готовый бинарный пакет

1. Перейди на страницу [Releases](https://codeberg.org/OverLessArtem/ayugram-template-void/releases)
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

### Способ 2 — собрать самому
```bash
# Клонируем шаблон
git clone https://codeberg.org/OverLessArtem/ayugram-template-void.git

# Клонируем официальный репозиторий void-packages
git clone https://github.com/void-linux/void-packages.git

# Копируем наш пакет в srcpkgs
cp -r ayugram-template-void/srcpkgs/* void-packages/srcpkgs/

# Переходим в директорию
cd void-packages

# Собираем пакет (может занять 10–40 минут)
./xbps-src pkg ayugram-desktop

# Устанавливаем собранный пакет
sudo xbps-install -R hostdir/binpkgs ayugram-desktop
```
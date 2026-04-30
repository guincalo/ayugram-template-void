# AyuGram Desktop для Void Linux
[English](README-en.md)

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png) ![VoidBTW](https://github.com/void-linux/void-packages/blob/master/srcpkgs/void-artwork/files/icons/void-logo-128.png)

Неофициальная сборка мода [AyuGram](https://github.com/AyuGram/AyuGramDesktop) под **Void Linux**.

## Два способа установки

### Способ 1 — готовый бинарный пакет (только x86_64-glibc)

```bash
# Скачиваем последний релиз с https://codeberg.org/OverLessArtem/ayugram-template-void/releases/latest
# или используем команду ниже (требует установки curl)

# Устанавливаем
curl -sL https://codeberg.org/OverLessArtem/ayugram-template-void/releases/latest/download/ayugram-desktop-*.xbps | xbps-install -
```

Или вручную: скачать `.xbps` файл из Release на странице релизов и установить `xbps-install -p ./файл.xbps`.

### Способ 2 — собрать самому
```bash
# Клонируем шаблон
git clone https://github.com/OverLessArtem/ayugram-template-void.git

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

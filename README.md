# AyuGram Desktop для Void Linux
[English](README-en.md)

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png)

Неофициальная сборка мода [AyuGram](https://github.com/AyuGram/AyuGramDesktop) под **Void Linux**.

> **Это форк.** Он не разрабатывает AyuGram — только поддерживает шаблон пакета Void в актуальном состоянии относительно релизов [AyuGram](https://github.com/AyuGram/AyuGramDesktop/releases) и собирает его автоматически: ежедневный бот поднимает версию шаблона при выходе нового релиза, а GitHub Actions собирает `.xbps` пакеты для glibc и musl на каждый бамп.

## Подключение репозитория (рекомендуется)

Пакеты публикуются как подписанный xbps-репозиторий (ветка `binaries`). После подключения `xbps-install -Su` обновляет AyuGram автоматически вместе со всей системой.

```bash
echo 'repository=https://raw.githubusercontent.com/guincalo/ayugram-template-void/binaries' | sudo tee /etc/xbps.d/20-ayugram.conf
sudo xbps-install -S   # при первом синке подтверди fingerprint репозитория
sudo xbps-install ayugram-desktop
```

## Установка из Releases (вручную)

1. Перейди на страницу [Releases](https://github.com/guincalo/ayugram-template-void/releases)
2. Скачай `.xbps` для нужной архитектуры:
   - **x86_64-glibc** — для большинства систем
   - **x86_64-musl** — для musl-based Void Linux
3. Установи пакет:

```bash
cd <директория_с_скачанным_файлом>
xbps-rindex -a *.xbps
sudo xbps-install --repository=$PWD ayugram-desktop
```

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
- **build.yml** собирает `ayugram-desktop` для x86_64-glibc и x86_64-musl при каждом изменении шаблона, подписывает пакеты ключом из секретов, публикует их в ветку `binaries` (это и есть xbps-репозиторий) и создаёт Release с автогенерируемым changelog; тег имеет вид `v<версия>-r<ревизия>-<sha>`.

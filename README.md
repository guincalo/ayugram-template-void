# AyuGram Desktop для Void Linux
[English](README-en.md)

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png)

Неофициальный шаблон пакета и сборки [AyuGram Desktop](https://github.com/AyuGram/AyuGramDesktop) для **Void Linux**.

Этот репозиторий — форк шаблона пакета для Void Linux, а не самого клиента. Разработкой AyuGram занимается [команда upstream-проекта](https://github.com/AyuGram/AyuGramDesktop); здесь поддерживаются упаковка и автоматизированная сборка `.xbps` для x86_64 (glibc и musl).

## Подключение репозитория (рекомендуется)

Готовые пакеты публикуются в ветке `binaries` как подписанный xbps-репозиторий. Для публикации требуется ключ `PRIV_KEY`. После подключения команда `sudo xbps-install -Su` обновляет AyuGram вместе с системой, если в репозитории есть более новая версия.

```bash
echo 'repository=https://raw.githubusercontent.com/guincalo/ayugram-template-void/binaries' | sudo tee /etc/xbps.d/20-ayugram.conf
sudo xbps-install -S   # при первом подключении проверь отпечаток ключа
sudo xbps-install ayugram-desktop
```

## Установка из Releases (вручную)

1. Перейди на страницу [Releases](https://github.com/guincalo/ayugram-template-void/releases)
2. Скачай `.xbps` для нужной архитектуры:
   - **x86_64-glibc** — для Void Linux с glibc
   - **x86_64-musl** — для Void Linux с musl
3. Установи пакет:

```bash
cd <директория_с_скачанным_файлом>
xbps-rindex -a *.xbps
sudo xbps-install --repository="$PWD" ayugram-desktop
```

Для обновления скачай новый `.xbps` в тот же каталог, повтори `xbps-rindex -a *.xbps` и выполни `sudo xbps-install --repository="$PWD" -u ayugram-desktop`.

## Сборка вручную

На Void Linux с установленным `base-devel`:

```bash
# Клонируем шаблон
git clone https://github.com/guincalo/ayugram-template-void.git

# Клонируем официальный void-packages
git clone https://github.com/void-linux/void-packages.git

# Копируем шаблон пакета
cp -r ayugram-template-void/srcpkgs/* void-packages/srcpkgs/

# Переходим в каталог
cd void-packages

# Подготавливаем окружение и собираем пакет
./xbps-src binary-bootstrap
./xbps-src pkg ayugram-desktop

# Устанавливаем собранный пакет
sudo xbps-install -R hostdir/binpkgs ayugram-desktop
```

## Автоматизация

- **update.yml** запускается по расписанию (ежедневно в 06:00 UTC) или вручную. Он сверяет версию шаблона с последним релизом AyuGram и записывает точную версию Qt6 из репозитория Void в `qt6_build_version`. Изменение Qt6 повышает ревизию пакета; новая версия AyuGram сбрасывает её на `1`. Для коммита и запуска сборки нужен `BOT_PAT` с правами записи в репозиторий.
- **build.yml** запускается при изменениях в `srcpkgs/**` на ветке `main` или вручную. Он собирает пакеты для glibc и musl; после успешной сборки публикует их в `binaries` и Releases. Тег имеет вид `v<версия>-r<ревизия>-<sha>`. Подписание требует секрета `PRIV_KEY`.

Автоматическое обновление шаблона не гарантирует успешную сборку или совместимость нового релиза. Проверка Qt6 перед сборкой останавливает её при несовпадении установленной версии с маркером или невозможности проверить версию.

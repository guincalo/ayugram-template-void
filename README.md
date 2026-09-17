# AyuGram Desktop для Void Linux

[English](README-en.md)

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png)

Неофициальные пакеты [AyuGram Desktop](https://github.com/AyuGram/AyuGramDesktop) для Void Linux.

Сам AyuGram разрабатывает [команда AyuGram](https://github.com/AyuGram/AyuGramDesktop). Этот репозиторий только собирает пакет: шаблон для Void и автоматические сборки `.xbps` для x86_64 (glibc и musl).

## Установка

Пакеты публикуются в ветке `binaries` как подписанный xbps-репозиторий.

```bash
echo 'repository=https://raw.githubusercontent.com/guincalo/ayugram-template-void/binaries' | sudo tee /etc/xbps.d/20-ayugram.conf
sudo xbps-install -S   # при первом синке подтверди отпечаток ключа
sudo xbps-install ayugram-desktop
```

Дальше `sudo xbps-install -Su` обновляет AyuGram вместе с системой.

## Установка вручную

1. Скачай `.xbps` со страницы [Releases](https://github.com/guincalo/ayugram-template-void/releases):
   - `x86_64-glibc` — обычный Void
   - `x86_64-musl` — Void на musl
2. Установи:

```bash
cd <папка_со_скачанным_файлом>
xbps-rindex -a *.xbps
sudo xbps-install --repository="$PWD" ayugram-desktop
```

Для обновления скачай новый файл в ту же папку и повтори команды с `-u`.

## Сборка вручную

Нужен Void Linux и `base-devel`.

```bash
git clone https://github.com/guincalo/ayugram-template-void.git
git clone https://github.com/void-linux/void-packages.git
cp -r ayugram-template-void/srcpkgs/* void-packages/srcpkgs/
cd void-packages
./xbps-src binary-bootstrap
./xbps-src pkg ayugram-desktop
sudo xbps-install -R hostdir/binpkgs ayugram-desktop
```

## Как это обновляется автоматически

- `update.yml` запускается раз в день. Вышел новый релиз AyuGram — бот поднимает версию шаблона. Обновился Qt6 в Void — бот поднимает ревизию. После этого запускается сборка.
- `build.yml` собирает пакеты для glibc и musl, подписывает их и публикует в `binaries` и Releases. Если версия Qt6 в окружении сборки не совпадает с ожидаемой, сборка останавливается.

Новый релиз AyuGram не гарантирует, что сборка пройдёт или что всё будет работать.

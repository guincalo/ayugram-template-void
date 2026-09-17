# AyuGram Desktop for Void Linux

[Русский](README.md)

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png)

Unofficial [AyuGram Desktop](https://github.com/AyuGram/AyuGramDesktop) packages for Void Linux.

AyuGram itself is developed by the [AyuGram team](https://github.com/AyuGram/AyuGramDesktop). This repo only does the packaging: a Void template and automatic `.xbps` builds for x86_64 (glibc and musl).

## Install

Packages are published on the `binaries` branch as a signed xbps repository.

```bash
echo 'repository=https://raw.githubusercontent.com/guincalo/ayugram-template-void/binaries' | sudo tee /etc/xbps.d/20-ayugram.conf
sudo xbps-install -S   # accept the repository fingerprint on first sync
sudo xbps-install ayugram-desktop
```

After that, `sudo xbps-install -Su` keeps AyuGram up to date with the rest of the system.

## Install manually

1. Grab the `.xbps` from the [Releases](https://github.com/guincalo/ayugram-template-void/releases) page:
   - `x86_64-glibc` — regular Void
   - `x86_64-musl` — Void on musl
2. Install it:

```bash
cd <download directory>
xbps-rindex -a *.xbps
sudo xbps-install --repository="$PWD" ayugram-desktop
```

To update later, download the new file into the same folder and repeat with `-u`.

## Build it yourself

You need Void Linux and `base-devel`.

```bash
git clone https://github.com/guincalo/ayugram-template-void.git
git clone https://github.com/void-linux/void-packages.git
cp -r ayugram-template-void/srcpkgs/* void-packages/srcpkgs/
cd void-packages
./xbps-src binary-bootstrap
./xbps-src pkg ayugram-desktop
sudo xbps-install -R hostdir/binpkgs ayugram-desktop
```

## How updates work

- `update.yml` runs once a day. New AyuGram release — it bumps the template version. Qt6 updated in Void — it bumps the revision. Either way a build starts afterwards.
- `build.yml` builds the glibc and musl packages, signs them, and publishes them to `binaries` and Releases. If the Qt6 version in the build environment doesn't match what the template expects, the build stops.

A new AyuGram release is not a guarantee that it builds or that everything works.

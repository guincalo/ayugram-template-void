# AyuGram Desktop for Void Linux
[Русский](README.md)

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png)

Unofficial package template and builds of [AyuGram Desktop](https://github.com/AyuGram/AyuGramDesktop) for **Void Linux**.

This repository is a fork of the Void Linux packaging template, not the client itself. AyuGram is developed by the [upstream project](https://github.com/AyuGram/AyuGramDesktop); this repository maintains the packaging and automated `.xbps` builds for x86_64 (glibc and musl).

## Add the repository (recommended)

Prebuilt packages are published to the `binaries` branch as a signed xbps repository. Publishing requires the `PRIV_KEY` signing key. Once added, `sudo xbps-install -Su` updates AyuGram along with the system whenever a newer package is available.

```bash
echo 'repository=https://raw.githubusercontent.com/guincalo/ayugram-template-void/binaries' | sudo tee /etc/xbps.d/20-ayugram.conf
sudo xbps-install -S   # verify the key fingerprint when first connecting
sudo xbps-install ayugram-desktop
```

## Install from Releases (manually)

1. Go to the [Releases](https://github.com/guincalo/ayugram-template-void/releases) page
2. Download the `.xbps` package for your system:
   - **x86_64-glibc** — for Void Linux with glibc
   - **x86_64-musl** — for Void Linux with musl
3. Install the package:

```bash
cd <directory_with_downloaded_file>
# Generate the repository index (required before installing)
xbps-rindex -a *.xbps
# Install the package
sudo xbps-install --repository="$PWD" ayugram-desktop
```

To update later, download the new release's `.xbps` into the same directory and run `xbps-rindex -a *.xbps && sudo xbps-install --repository="$PWD" -u ayugram-desktop`.

## Build it yourself

On Void Linux with `base-devel` installed:

```bash
# Clone the template
git clone https://github.com/guincalo/ayugram-template-void.git

# Clone the official void-packages repository
git clone https://github.com/void-linux/void-packages.git

# Copy the package template
cp -r ayugram-template-void/srcpkgs/* void-packages/srcpkgs/

# Enter the directory
cd void-packages

# Prepare the build environment and build the package
./xbps-src binary-bootstrap
./xbps-src pkg ayugram-desktop

# Install the built package
sudo xbps-install -R hostdir/binpkgs ayugram-desktop
```

## Automation

- **update.yml** runs on a schedule (daily at 06:00 UTC) or manually. It checks the template against the latest AyuGram release and records the exact Qt6 version from the Void repository in `qt6_build_version`. A Qt6 change increments the package revision; a new AyuGram version resets it to `1`. Committing changes and triggering the build requires a `BOT_PAT` with repository write access.
- **build.yml** runs on changes to `srcpkgs/**` on `main` or manually. It builds packages for glibc and musl, then publishes successful builds to `binaries` and Releases. Tags use the format `v<version>-r<revision>-<sha>`. Signing requires the `PRIV_KEY` secret.

An automatic template update does not guarantee a successful build or compatibility with a new release. The pre-build Qt6 check stops the build if the installed version differs from the marker or cannot be verified.

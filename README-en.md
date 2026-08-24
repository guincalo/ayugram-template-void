# AyuGram Desktop for Void Linux

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png)

Unofficial build of the [AyuGram](https://github.com/AyuGram/AyuGramDesktop) mod for **Void Linux**.

> **This is a fork.** It does not develop AyuGram — it only keeps the Void package template up to date with upstream [AyuGram releases](https://github.com/AyuGram/AyuGramDesktop/releases) and compiles it automatically: a daily bot bumps the template when a new version is tagged, and GitHub Actions builds glibc and musl `.xbps` packages on every bump.

## Install from Releases

1. Go to the [Releases](https://github.com/guincalo/ayugram-template-void/releases) page
2. Download the latest release for your architecture:
   - **x86_64-glibc** — for most systems
   - **x86_64-musl** — for musl-based Void Linux
3. Install the package:

```bash
cd <directory_with_downloaded_file>
# Generate the repository index (required before installing)
xbps-rindex -a *.xbps
# Install the package
sudo xbps-install --repository=$PWD ayugram-desktop
```

To update later, download the new release's `.xbps` into the same directory and run `xbps-rindex -a *.xbps && sudo xbps-install --repository=$PWD -u ayugram-desktop`.

## Build it yourself

```bash
# Clone the template
git clone https://github.com/guincalo/ayugram-template-void.git

# Clone the official void-packages repository
git clone https://github.com/void-linux/void-packages.git

# Copy our package sources
cp -r ayugram-template-void/srcpkgs/* void-packages/srcpkgs/

# Enter the directory
cd void-packages

# Build the package (takes ~10-40 minutes depending on your machine)
./xbps-src pkg ayugram-desktop

# Install the built package
sudo xbps-install -R hostdir/binpkgs ayugram-desktop
```

## Automation

- **update.yml** runs daily: compares the template version against the latest AyuGram tag, commits a version bump if there's a new one.
- **build.yml** builds `ayugram-desktop` for x86_64-glibc and x86_64-musl on every template change and attaches the packages to a GitHub Release.

# AyuGram Desktop for Void Linux

![AyuGram](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuGram.png) ![AyuChan](https://github.com/AyuGram/AyuGramDesktop/raw/dev/.github/AyuChan.png) ![VoidBTW](.forgejo/void-logo.png)

Unofficial build of the [AyuGram](https://github.com/AyuGram/AyuGramDesktop) mod for **Void Linux**.

## Two installation methods

### Method 1 — Pre-built binary package

1. Go to the [Releases](https://codeberg.org/OverLessArtem/ayugram-template-void/releases) page
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

### Method 2 — Build it yourself

```bash
# Clone the template
git clone https://codeberg.org/OverLessArtem/ayugram-template-void.git

# Clone the official void-packages repository
git clone https://github.com/void-linux/void-packages.git

# Copy our package sources
cp -r ayugram-template-void/srcpkgs/* void-packages/srcpkgs/

# Enter the directory
cd void-packages

# Build the package (takes ~10–40 minutes depending on your machine)
./xbps-src pkg ayugram-desktop

# Install the built package
sudo xbps-install -R hostdir/binpkgs ayugram-desktop
```
# 🌲 Treex

**Treex** is a modern, colorized, and feature-rich command-line tree viewer written in Python.  
It allows you to visualize directories, display file statistics, colorize file types, and export results — all in one command.

---

## 📦 Features

- 🖍️ Colorized directory and file tree (configurable via `~/.config/treex/treex.conf`)
- 📁 File and folder size display
- 📄 Count total lines in source files
- 🕒 Show last modification time
- 🧮 Summary statistics and extension distribution
- 🧰 Export tree output to a file (cleaned of ANSI codes)
- 🪶 Customizable color scheme for each file type
- 🧊 Works on **Arch Linux** and **Debian-based** systems (packages provided)

---

## ⚙️ Installation

### 🟢 Arch Linux (PKGBUILD)

Clone the repository and build the package:

```bash
git clone https://github.com/herdem09/treex.git
cd treex
makepkg -si
````

Then simply run:

```bash
treex
```

---

### 🟣 Debian / Ubuntu (.deb)

If you downloaded the `.deb` package from [Releases](https://github.com/herdem09/treex/releases):

```bash
sudo dpkg -i treex_1.0.0-1_all.deb
```

Then run:

```bash
treex
```

---

## 🧩 Configuration

Treex uses a configuration file located at:

```
~/.config/treex/treex.conf
```

Example structure:

```
~/.config/
└── treex/
    └── treex.conf
```

Example config content:

```ini
# Primary color (used if no specific color is defined)
primary = 37   # White

# Folder color
folder = 34    # Blue

# File type colors
.py = 32       # Green
.md = 36       # Cyan
.sh = 33       # Yellow
.txt = 37      # White
.log = 35      # Magenta
.conf = 36     # Cyan
```

---

## 🖥️ Usage

Run `treex` in any directory:

```bash
treex
```

Show hidden files:

```bash
treex -a
```

Show file sizes and number of lines:

```bash
treex --size --lines
```

Limit directory depth:

```bash
treex --depth 2
```

Export output (without color codes):

```bash
treex -ex output.txt
```

Show summary and extension distribution:

```bash
treex --summary --extdist
```

---

## 📊 Example Output

```
project/
├── main.py (12 KB) [340 lines]
├── README.md (2 KB)
└── data/
    ├── input.txt (8 KB)
    └── output.log (1 KB)
```

---

## 🧑‍💻 Maintainer

**herdem09**
📧 [herdem09@proton.me](mailto:herdem09@proton.me)
🔗 [https://github.com/herdem09/treex](https://github.com/herdem09/treex)

---

## 📜 License

Licensed under the **MIT License** — free to use, modify, and distribute.

---

## 🧱 Build Info

* **Version:** 1.0.0
* **Language:** Python 3
* **Platforms:** Arch Linux, Debian / Ubuntu
* **Dependencies:** Python ≥ 3.6

```

# yt-subtitle-translator

A tiny Python CLI that downloads subtitles for a video using **yt-dlp**, translates them to a target language via **deep-translator** (GoogleTranslator backend by default), and saves the translated `.srt` next to the original.

> **Use case:** Quick add-on for people who already use `yt-dlp` and want a one-shot way to get translated subtitles.

---

## ✨ Features

- Downloads subtitles (or auto-generated subs) with `yt-dlp`.
- Translates `.srt` subtitle text to your target language (e.g., `fa`, `en`, `de`, `ar`, ...).
- Preserves subtitle structure: timestamps, numbering, and spacing remain intact.
- Fallback-safe: if translation fails for a line, the original text is kept.

---

## 🚀 Quick Start

```bash
# 1) Clone the repo
git clone https://github.com/<your-username>/yt-subtitle-translator.git
cd yt-subtitle-translator

# 2) (Optional) Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run the tool
python yt_subtitle_translator.py "<video_url>" --target fa

# Example: translate English subs to Persian (fa)
python yt_subtitle_translator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --target fa --source en
```

> By default, the tool requests English (`en`) subtitles if you don’t pass `--source`. If those are missing, it also tries to fetch auto-generated captions.

---

## ⚙️ Command-line Options

| Option     | Required | Description                                           |
| ---------- | -------- | ----------------------------------------------------- |
| `url`      | ✅        | The video URL (YouTube or supported site).            |
| `--target` | ✅        | Target language code (e.g., `fa`, `en`, `de`).        |
| `--source` | ❌        | Source subtitle language code (default: auto-detect). |
| `--outdir` | ❌        | Directory for saving subtitles (default: `./subs`).   |

---

## 📂 Project Structure

```
yt-subtitle-translator/
├── yt_subtitle_translator.py   # main script
├── requirements.txt            # dependencies
└── README.md                   # documentation
```

---

## 🧪 Example

Translate a YouTube video’s auto-generated English subtitles into German:

```bash
python yt_subtitle_translator.py "https://youtu.be/abc123" --target de --source en
```

This will produce two `.srt` files in the `subs/` folder:

- `VideoTitle [videoId].en.srt` (original)
- `VideoTitle [videoId].translated.de.srt` (translated)

---

## 🔮 Future Ideas

- Add support for more translation providers (LibreTranslate, DeepL, etc.).
- Batch translation of multi-line segments to reduce API calls.
- Publish as a PyPI package with `pip install yt-subtitle-translator`.
- Optional GUI for non-CLI users.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

MIT — feel free to use and modify.


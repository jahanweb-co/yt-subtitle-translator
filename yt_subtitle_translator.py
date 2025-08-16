import argparse
import os
import re
import sys
from pathlib import Path

from deep_translator import GoogleTranslator
import yt_dlp

SRT_TIMESTAMP = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}")


def find_srt_file(outdir: Path) -> Path | None:
    srt_files = sorted(outdir.glob("*.srt"), key=lambda p: p.stat().st_mtime, reverse=True)
    return srt_files[0] if srt_files else None


def translate_srt(src_path: Path, target_lang: str, source_lang: str | None) -> Path:
    dst_path = src_path.with_suffix("")
    dst_path = dst_path.with_name(dst_path.name + f".translated.{target_lang}").with_suffix(".srt")

    translator = GoogleTranslator(source=source_lang or "auto", target=target_lang)

    def translate_line(line: str) -> str:
        if not line.strip():
            return line
        if line.strip().isdigit():
            return line
        if SRT_TIMESTAMP.match(line.strip()):
            return line
        try:
            return translator.translate(line.strip()) + "\n"
        except Exception as e:
            return line

    with src_path.open("r", encoding="utf-8", errors="ignore") as fin, dst_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(translate_line(line))

    return dst_path


def download_subtitles(url: str, outdir: Path, sub_lang: str | None) -> Path | None:
    ydl_opts = {
        "outtmpl": str(outdir / "%(title).90s [%(id)s].%(ext)s"),
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitlesformat": "srt",
    }

    if sub_lang:
        ydl_opts["subtitleslangs"] = [sub_lang]
    else:
        ydl_opts["subtitleslangs"] = ["en"]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
        except Exception as e:
            print(f"[error] yt-dlp failed: {e}")
            return None

    sub_path = None
    requested = info.get("requested_subtitles") or {}
    for lang, meta in requested.items():
        fp = meta.get("filepath")
        if fp and Path(fp).exists():
            sub_path = Path(fp)
            break

    if not sub_path:
        sub_path = find_srt_file(outdir)

    return sub_path


def main():
    parser = argparse.ArgumentParser(description="Download subtitles with yt-dlp and translate to target language.")
    parser.add_argument("url", help="Video URL (YouTube, etc.)")
    parser.add_argument("--target", required=True, help="Target language code (e.g., fa, en, de, ar)")
    parser.add_argument("--source", help="Source subtitle language code (e.g., en). If omitted, auto-detect.")
    parser.add_argument("--outdir", default="./subs", help="Output directory for subtitles")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("[info] downloading subtitles...")
    srt_path = download_subtitles(args.url, outdir, args.source)
    if not srt_path:
        print("[error] No .srt subtitle file found.")
        sys.exit(1)

    print(f"[info] translating '{srt_path.name}' -> {args.target} ...")
    dst = translate_srt(srt_path, args.target, args.source)
    print(f"[done] saved: {dst}")


if __name__ == "__main__":
    main()

import argparse
import subprocess
import sys
from pathlib import Path


def check_ffmpeg() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def convert_mp4_to_wav(src: Path, dst: Path, sample_rate: int | None, channels: int | None, overwrite: bool) -> tuple[bool, str]:
    dst.parent.mkdir(parents=True, exist_ok=True)

    if dst.exists() and not overwrite:
        return True, f"exists: {dst}"

    cmd = [
        "ffmpeg",
        "-y" if overwrite else "-n",
        "-i", str(src),
    ]

    if sample_rate:
        cmd += ["-ar", str(sample_rate)]
    if channels:
        cmd += ["-ac", str(channels)]

    # Use PCM signed 16-bit little-endian WAV
    cmd += ["-vn", "-acodec", "pcm_s16le", str(dst)]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ok = proc.returncode == 0
    msg = proc.stderr.strip().splitlines()[-1] if proc.stderr else ""
    return ok, msg


def gather_files(input_dir: Path, recursive: bool) -> list[Path]:
    pattern = "**/*.mp4" if recursive else "*.mp4"
    return sorted(p for p in input_dir.glob(pattern) if p.is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert all MP4 files in a folder to WAV using ffmpeg")
    parser.add_argument("input_dir", type=Path, help="Directory containing .mp4 files")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory to write .wav files (mirrors structure if recursive). Defaults to input_dir")
    parser.add_argument("--recursive", action="store_true", help="Recurse into subdirectories")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .wav files")
    parser.add_argument("--sample-rate", type=int, default=None, help="Audio sample rate (e.g., 16000, 44100)")
    parser.add_argument("--channels", type=int, default=None, choices=[1, 2], help="Number of audio channels (1=mono, 2=stereo)")

    args = parser.parse_args(argv)

    input_dir: Path = args.input_dir
    output_dir: Path | None = args.output_dir

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: input_dir not found or not a directory: {input_dir}", file=sys.stderr)
        return 2

    if not check_ffmpeg():
        print("Error: ffmpeg is not installed or not in PATH. Please install ffmpeg and try again.", file=sys.stderr)
        return 3

    files = gather_files(input_dir, args.recursive)
    if not files:
        print("No .mp4 files found.")
        return 0

    out_base = output_dir if output_dir is not None else input_dir

    successes = 0
    failures = 0

    for src in files:
        rel = src.relative_to(input_dir) if output_dir else src.name
        dst = (out_base / rel).with_suffix(".wav") if output_dir else (out_base / Path(rel)).with_suffix(".wav")

        ok, msg = convert_mp4_to_wav(src, dst, args.sample_rate, args.channels, args.overwrite)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {src} -> {dst} {('- ' + msg) if msg else ''}")
        if ok:
            successes += 1
        else:
            failures += 1

    print(f"Done. Converted: {successes}, Failed: {failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

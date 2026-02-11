#!/usr/bin/env python3
"""
Merge PDF files from input/ into a single PDF using PyMuPDF.

Usage:
    python merge_pdfs_pymupdf.py file1.pdf file2.pdf
    python merge_pdfs_pymupdf.py file1.pdf file2.pdf -o output/custom_name.pdf
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import fitz  # PyMuPDF


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files in the specified order using PyMuPDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python merge_pdfs_pymupdf.py a.pdf b.pdf\n"
            "  python merge_pdfs_pymupdf.py a.pdf b.pdf c.pdf -o output/merged_manual.pdf"
        ),
    )
    parser.add_argument(
        "pdf_files",
        nargs="*",
        help="PDF filenames located in input/ (for example: a.pdf b.pdf).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output path. If omitted, output/merged_YYYYMMDD_HHMMSS.pdf is used.",
    )

    args = parser.parse_args()
    if len(args.pdf_files) == 0:
        parser.print_usage(sys.stderr)
        print("Error: no input files were provided.", file=sys.stderr)
        raise SystemExit(1)
    if len(args.pdf_files) < 2:
        parser.print_usage(sys.stderr)
        print("Error: at least 2 PDF files are required for merging.", file=sys.stderr)
        raise SystemExit(1)

    return args


def validate_and_resolve_inputs(pdf_files: list[str], input_dir: Path) -> list[Path]:
    resolved: list[Path] = []

    for original_name in pdf_files:
        candidate = Path(original_name)

        # Only input/ direct children are allowed.
        if candidate.name != original_name:
            raise ValueError(
                f"Input must be a filename in input/ (no directory path allowed): {original_name}"
            )

        if candidate.suffix.lower() != ".pdf":
            raise ValueError(f"Only .pdf files are allowed: {original_name}")

        resolved_path = input_dir / candidate.name
        if not resolved_path.exists():
            raise FileNotFoundError(f"File not found in input/: {candidate.name}")
        if not resolved_path.is_file():
            raise FileNotFoundError(f"Not a file in input/: {candidate.name}")

        resolved.append(resolved_path)

    return resolved


def resolve_output_path(output_arg: str | None, output_dir: Path) -> Path:
    if output_arg:
        output_path = Path(output_arg)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"merged_{timestamp}.pdf"

    parent = output_path.parent if output_path.parent != Path("") else Path(".")
    parent.mkdir(parents=True, exist_ok=True)

    return output_path


def merge_pdfs(input_paths: list[Path], output_path: Path) -> None:
    merged_doc = fitz.open()
    inserted_count = 0

    try:
        for input_path in input_paths:
            try:
                with fitz.open(input_path) as src_doc:
                    merged_doc.insert_pdf(src_doc)
            except Exception as exc:  # pragma: no cover - defensive for fitz internals
                raise RuntimeError(f"Failed to read PDF '{input_path.name}': {exc}") from exc
            inserted_count += 1

        if inserted_count == 0:
            raise RuntimeError("No pages were added to the merged document.")

        try:
            merged_doc.save(output_path)
        except Exception as exc:  # pragma: no cover - defensive for fitz internals
            raise RuntimeError(f"Failed to save output PDF '{output_path}': {exc}") from exc
    finally:
        merged_doc.close()


def main() -> int:
    args = parse_args()
    base_dir = Path.cwd()
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    if not input_dir.exists() or not input_dir.is_dir():
        print("Error: input/ directory does not exist.", file=sys.stderr)
        return 1

    try:
        input_paths = validate_and_resolve_inputs(args.pdf_files, input_dir)
        output_path = resolve_output_path(args.output, output_dir)
        merge_pdfs(input_paths, output_path)
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Merged {len(input_paths)} files successfully.")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

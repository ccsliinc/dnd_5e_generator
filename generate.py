#!/usr/bin/env python3
"""
D&D 5e Sheet Generator

Generates HTML character sheets and item cards from JSON data files.
Supports PDF generation and compression via Chrome headless.

Usage:
    python3 generate.py <input.json> [options]

Options:
    --pdf           Generate PDF via Chrome headless
    --compress      Compress PDF for printing (implies --pdf)
    --dpi <value>   DPI for compression (default: 150)
    --open          Open output files when done
    --output <dir>  Custom output directory
    --bundle        Include character's items in output (character + items)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from lib import CharacterDocument, ItemDocument


# =============================================================================
# PDF GENERATION & COMPRESSION
# =============================================================================

CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
]


def find_chrome() -> Optional[str]:
    """Find Chrome executable on the system."""
    for path in CHROME_PATHS:
        if Path(path).exists():
            return path
    # Try 'which' on Unix
    try:
        result = subprocess.run(["which", "google-chrome"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def generate_pdf(html_path: Path, pdf_path: Path) -> bool:
    """Generate PDF from HTML using Chrome headless."""
    chrome = find_chrome()
    if not chrome:
        print("Error: Chrome not found. Install Google Chrome for PDF generation.")
        return False

    try:
        subprocess.run([
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            "--print-background",
            f"file://{html_path.absolute()}"
        ], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")
        return False


def compress_pdf(pdf_path: Path, output_path: Path, dpi: int = 150) -> bool:
    """Compress PDF by rasterizing and recombining."""
    if not shutil.which("pdftoppm"):
        print("Error: pdftoppm not found. Install poppler (brew install poppler)")
        return False
    if not shutil.which("img2pdf"):
        print("Error: img2pdf not found. Install img2pdf (brew install img2pdf)")
        return False

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Convert PDF to images
            subprocess.run([
                "pdftoppm", "-png", "-r", str(dpi),
                str(pdf_path), str(temp_path / "page")
            ], check=True, capture_output=True)

            # Get all generated images
            images = sorted(temp_path.glob("page*.png"))
            if not images:
                print("Error: No images generated from PDF")
                return False

            # Recombine into PDF
            subprocess.run([
                "img2pdf", *[str(img) for img in images],
                "-o", str(output_path)
            ], check=True, capture_output=True)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error compressing PDF: {e}")
        return False


def get_file_size(path: Path) -> str:
    """Get human-readable file size."""
    size = path.stat().st_size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def open_file(path: Path) -> None:
    """Open file with system default application."""
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)])
    elif sys.platform == "win32":
        os.startfile(str(path))
    else:
        subprocess.run(["xdg-open", str(path)])


# =============================================================================
# DOCUMENT FACTORY
# =============================================================================

def create_document(data: dict, base_path: str = ""):
    """Create appropriate document type based on data."""
    doc_type = data.get("type", "character")

    if doc_type == "item":
        return ItemDocument(data, base_path)
    else:
        return CharacterDocument(data, base_path)


# =============================================================================
# GENERATION PIPELINE
# =============================================================================

def generate(
    json_path: Path,
    output_dir: Optional[Path] = None,
    pdf: bool = False,
    compress: bool = False,
    dpi: int = 150,
    open_files: bool = False
) -> dict:
    """
    Unified generation pipeline for both characters and items.

    Returns dict with paths to generated files:
        {"html": Path, "pdf": Path|None, "compressed": Path|None}
    """
    base_dir = Path(__file__).parent
    if output_dir is None:
        output_dir = base_dir / "output"

    # Load JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    doc_type = data.get("type", "character")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # Create document and generate HTML
    if doc_type == "item":
        base_path = "../.."  # Relative path from output/items to project root
        document = ItemDocument(data, base_path)
        item_name = data.get("header", {}).get("name", "item")
        safe_name = item_name.replace(" ", "_").replace("'", "")
        doc_output_dir = output_dir / "items"
    else:
        document = CharacterDocument(data)
        char_name = data.get("header", {}).get("character_name", "character")
        safe_name = char_name.replace(" ", "_")
        doc_output_dir = output_dir / safe_name

    # Generate HTML
    html = document.build_html()

    # Ensure output directory exists
    doc_output_dir.mkdir(parents=True, exist_ok=True)

    # Write HTML
    html_path = doc_output_dir / f"{safe_name}_{timestamp}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    result = {"html": html_path, "pdf": None, "compressed": None}
    print(f"[HTML] {html_path}")

    # Copy to stable "latest" filename
    latest_html = doc_output_dir / f"{safe_name}.html"
    shutil.copy2(html_path, latest_html)

    # Generate PDF if requested
    if pdf or compress:
        pdf_path = doc_output_dir / f"{safe_name}_{timestamp}.pdf"
        if generate_pdf(html_path, pdf_path):
            result["pdf"] = pdf_path
            print(f"[PDF]  {pdf_path} ({get_file_size(pdf_path)})")

            # Compress if requested
            if compress and pdf_path.exists():
                compressed_path = doc_output_dir / f"{safe_name}_{timestamp}_print.pdf"
                if compress_pdf(pdf_path, compressed_path, dpi):
                    result["compressed"] = compressed_path
                    print(f"[PRINT] {compressed_path} ({get_file_size(compressed_path)})")

                    # Copy print version to stable "latest" filename
                    latest_pdf = doc_output_dir / f"{safe_name}.pdf"
                    shutil.copy2(compressed_path, latest_pdf)

    # Open files if requested
    if open_files:
        open_file(html_path)
        if result["compressed"]:
            open_file(result["compressed"])
        elif result["pdf"]:
            open_file(result["pdf"])

    return result


def find_json_file(input_arg: str) -> Optional[Path]:
    """Find JSON file from argument (supports multiple search locations)."""
    base_dir = Path(__file__).parent
    characters_dir = base_dir / "characters"

    # Try as absolute/relative path first
    path = Path(input_arg)
    if path.is_file():
        return path

    # Try in characters folder: "thorek" -> characters/thorek.json
    path = characters_dir / f"{input_arg}.json"
    if path.is_file():
        return path

    # Try with .json extension in characters folder
    path = characters_dir / input_arg
    if path.is_file():
        return path

    return None


def get_embedded_items(char_data: dict) -> list[dict]:
    """Get embedded items from character data."""
    return char_data.get("items", [])


def generate_bundle(
    json_path: Path,
    output_dir: Optional[Path] = None,
    pdf: bool = False,
    compress: bool = False,
    dpi: int = 150,
    open_files: bool = False
) -> dict:
    """
    Generate character sheet bundled with their items.

    Returns dict with paths to generated files:
        {"html": Path, "pdf": Path|None, "compressed": Path|None}
    """
    base_dir = Path(__file__).parent
    if output_dir is None:
        output_dir = base_dir / "output"

    # Load character data
    with open(json_path, 'r', encoding='utf-8') as f:
        char_data = json.load(f)

    char_name = char_data.get("header", {}).get("character_name", "character")
    safe_name = char_name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # Generate character HTML (with item CSS included for bundled items)
    char_doc = CharacterDocument(char_data)
    char_html = char_doc.build_html()

    # Get embedded items from character data
    embedded_items = get_embedded_items(char_data)

    # If we have items, inject the item CSS into the character HTML
    if embedded_items:
        item_css = char_doc.load_css("item.css")
        # Insert item CSS before </style>
        style_end = char_html.find("</style>")
        if style_end > 0:
            char_html = char_html[:style_end] + "\n" + item_css + "\n    " + char_html[style_end:]

    # Generate item HTML
    items_html_parts = []

    for item_data in embedded_items:
        base_path = "../.."  # Relative path from output/<char>/ to project root
        item_doc = ItemDocument(item_data, base_path)

        # Get just the body content (pages) from item HTML
        full_html = item_doc.build_html()
        # Extract body content between <body> and </body>
        body_start = full_html.find("<body>") + 6
        body_end = full_html.find("</body>")
        if body_start > 5 and body_end > body_start:
            items_html_parts.append(full_html[body_start:body_end])

    # Combine character and items into single HTML
    # Insert items after character pages but before </body>
    if items_html_parts:
        body_end = char_html.find("</body>")
        combined_html = (
            char_html[:body_end] +
            "\n    <!-- ITEMS -->" +
            "".join(items_html_parts) +
            "\n" +
            char_html[body_end:]
        )
    else:
        combined_html = char_html

    # Ensure output directory exists
    doc_output_dir = output_dir / safe_name
    doc_output_dir.mkdir(parents=True, exist_ok=True)

    # Write combined HTML
    html_path = doc_output_dir / f"{safe_name}_bundle_{timestamp}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(combined_html)

    result = {"html": html_path, "pdf": None, "compressed": None}
    print(f"[HTML] {html_path}")
    if embedded_items:
        print(f"       (includes {len(embedded_items)} item(s))")

    # Copy to stable "latest" filename
    latest_html = doc_output_dir / f"{safe_name}.html"
    shutil.copy2(html_path, latest_html)

    # Generate PDF if requested
    if pdf or compress:
        pdf_path = doc_output_dir / f"{safe_name}_bundle_{timestamp}.pdf"
        if generate_pdf(html_path, pdf_path):
            result["pdf"] = pdf_path
            print(f"[PDF]  {pdf_path} ({get_file_size(pdf_path)})")

            # Compress if requested
            if compress and pdf_path.exists():
                compressed_path = doc_output_dir / f"{safe_name}_bundle_{timestamp}_print.pdf"
                if compress_pdf(pdf_path, compressed_path, dpi):
                    result["compressed"] = compressed_path
                    print(f"[PRINT] {compressed_path} ({get_file_size(compressed_path)})")

                    # Copy print version to stable "latest" filename
                    latest_pdf = doc_output_dir / f"{safe_name}.pdf"
                    shutil.copy2(compressed_path, latest_pdf)

    # Open files if requested
    if open_files:
        open_file(html_path)
        if result["compressed"]:
            open_file(result["compressed"])
        elif result["pdf"]:
            open_file(result["pdf"])

    return result


# =============================================================================
# CLI
# =============================================================================

def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="D&D 5e Sheet Generator - Generate character sheets and item cards from JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 generate.py thorek.json                     # Generate HTML only
  python3 generate.py thorek.json --pdf               # Generate HTML + PDF
  python3 generate.py thorek.json --compress --open   # Full pipeline + open
  python3 generate.py thorek.json --bundle --compress # Character + all items
  python3 generate.py characters/thorek/items/ring_of_wild_hunt.json --compress
        """
    )
    parser.add_argument("input", nargs="?", help="JSON file (character or item)")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF via Chrome headless")
    parser.add_argument("--compress", action="store_true", help="Compress PDF for printing (implies --pdf)")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for compression (default: 150)")
    parser.add_argument("--open", action="store_true", help="Open output files when done")
    parser.add_argument("--output", type=Path, help="Custom output directory")
    parser.add_argument("--bundle", action="store_true", help="Include character's items in output")

    args = parser.parse_args()

    # Find input file
    if args.input:
        json_path = find_json_file(args.input)
        if not json_path:
            print(f"Error: Could not find {args.input}")
            sys.exit(1)
    else:
        # Default to first character JSON in characters/*.json
        base_dir = Path(__file__).parent
        characters_dir = base_dir / "characters"
        json_files = sorted(characters_dir.glob("*.json"))
        if json_files:
            json_path = json_files[0]
        else:
            print("Error: No character files found. Provide a JSON file path.")
            parser.print_help()
            sys.exit(1)

    # Compress implies PDF
    if args.compress:
        args.pdf = True

    # Run generation
    print("=== D&D Sheet Generator ===\n")

    if args.bundle:
        result = generate_bundle(
            json_path=json_path,
            output_dir=args.output,
            pdf=args.pdf,
            compress=args.compress,
            dpi=args.dpi,
            open_files=args.open
        )
    else:
        result = generate(
            json_path=json_path,
            output_dir=args.output,
            pdf=args.pdf,
            compress=args.compress,
            dpi=args.dpi,
            open_files=args.open
        )

    print("\n=== Done! ===")

    return result["html"]


if __name__ == "__main__":
    main()

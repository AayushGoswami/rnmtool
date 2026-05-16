"""
rnmtool.__main__ - Entry point for the rnmtool CLI.

Features:
  - Batch rename files in a directory
  - Add prefix or suffix to filenames
  - Find-and-replace text in filenames (with optional regex support)
  - Change file extensions
  - Convert filenames to lowercase, uppercase, or title case
  - Dry-run mode to preview changes before applying them

Usage:
  rnmtool --help
  python -m rnmtool --help
"""

import os
import re
import argparse
from pathlib import Path


# ── Helpers ────────────────────────────────────────────────────────────────────

def collect_files(directory: str, recursive: bool, pattern: str) -> list[Path]:
    """Return a sorted list of files matching *pattern* inside *directory*."""
    base = Path(directory)
    glob = "**/" + pattern if recursive else pattern
    return sorted(p for p in base.glob(glob) if p.is_file())


def apply_transformations(name: str, args: argparse.Namespace) -> str:
    """Apply all requested transformations to a bare filename (no directory)."""
    stem, suffix = os.path.splitext(name)

    # 1. Find-and-replace (plain text or regex)
    if args.find is not None:
        if args.regex:
            stem = re.sub(args.find, args.replace or "", stem)
        else:
            stem = stem.replace(args.find, args.replace or "")

    # 2. Case conversion
    if args.case == "lower":
        stem = stem.lower()
    elif args.case == "upper":
        stem = stem.upper()
    elif args.case == "title":
        stem = stem.title()

    # 3. Prefix / suffix
    if args.prefix:
        stem = args.prefix + stem
    if args.suffix:
        stem = stem + args.suffix

    # 4. Extension replacement
    if args.ext:
        ext = args.ext if args.ext.startswith(".") else "." + args.ext
    else:
        ext = suffix

    return stem + ext


def preview_table(pairs: list[tuple[Path, Path]]) -> None:
    """Print a formatted before/after table."""
    if not pairs:
        print("  (no files matched)")
        return

    col = max(len(p[0].name) for p in pairs)
    print(f"\n  {'BEFORE':<{col}}   AFTER")
    print("  " + "─" * col + "   " + "─" * 40)
    for old, new in pairs:
        changed = "✓" if old.name != new.name else " "
        print(f"  {old.name:<{col}}   {new.name}  {changed}")
    print()


# ── Core logic ─────────────────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> None:
    files = collect_files(args.directory, args.recursive, args.pattern)

    if not files:
        print(f"[rnmtool] No files matching '{args.pattern}' found in '{args.directory}'.")
        return

    pairs: list[tuple[Path, Path]] = []
    for old_path in files:
        new_name = apply_transformations(old_path.name, args)
        new_path = old_path.parent / new_name
        pairs.append((old_path, new_path))

    if args.dry_run:
        print("[rnmtool] DRY RUN - no files will be changed.")
        preview_table(pairs)
        return

    renamed, skipped, errors = 0, 0, 0
    for old_path, new_path in pairs:
        if old_path == new_path:
            skipped += 1
            continue
        if new_path.exists() and not args.overwrite:
            print(f"  [SKIP] '{new_path.name}' already exists. Use --overwrite to replace.")
            skipped += 1
            continue
        try:
            old_path.rename(new_path)
            print(f"  [OK]   '{old_path.name}'  →  '{new_path.name}'")
            renamed += 1
        except OSError as exc:
            print(f"  [ERR]  '{old_path.name}': {exc}")
            errors += 1

    print(f"\n[rnmtool] Done. Renamed: {renamed}, Skipped: {skipped}, Errors: {errors}")


# ── CLI ────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rnmtool",
        description="Flexible file renaming utility.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview renaming all .txt files in the current directory
  rnmtool --dry-run --pattern "*.txt"

  # Add a prefix to every JPEG
  rnmtool --pattern "*.jpg" --prefix "2025_"

  # Replace spaces with underscores in all filenames
  rnmtool --find " " --replace "_"

  # Convert all .mp3 filenames to lowercase
  rnmtool --pattern "*.mp3" --case lower

  # Change extension from .jpeg to .jpg
  rnmtool --pattern "*.jpeg" --ext .jpg

  # Regex: remove leading digits from filenames
  rnmtool --regex --find "^\\d+_?" --replace ""
""",
    )

    p.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Target directory (default: current directory).",
    )
    p.add_argument(
        "--pattern", "-p",
        default="*",
        metavar="GLOB",
        help="Glob pattern to filter files (default: '*').",
    )
    p.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Search for files recursively.",
    )
    p.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview changes without renaming anything.",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting existing files.",
    )

    # Transformation options
    t = p.add_argument_group("transformations")
    t.add_argument("--find", "-f", metavar="TEXT", help="Text (or regex) to search for in filenames.")
    t.add_argument("--replace", "-s", metavar="TEXT", default="", help="Replacement text (default: remove match).")
    t.add_argument("--regex", "-x", action="store_true", help="Treat --find as a regular expression.")
    t.add_argument("--prefix", metavar="TEXT", help="Prepend text to each filename.")
    t.add_argument("--suffix", metavar="TEXT", help="Append text to each filename (before extension).")
    t.add_argument("--ext", metavar="EXT", help="Replace the file extension (e.g. '.jpg').")
    t.add_argument(
        "--case", "-c",
        choices=["lower", "upper", "title"],
        help="Convert filename case.",
    )

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not Path(args.directory).is_dir():
        parser.error(f"Directory not found: '{args.directory}'")

    if args.find is None and args.prefix is None and args.suffix is None \
            and args.ext is None and args.case is None and not args.dry_run:
        parser.error("No transformation specified. Use --help for usage or --dry-run to preview files.")

    run(args)


if __name__ == "__main__":
    main()

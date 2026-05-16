"""
tests/test_rename.py - Unit tests for rnmtool core logic.

Run with:
    python -m pytest tests/ -v
"""

import sys
import types
import argparse
import pytest
from pathlib import Path

# Allow importing from src/ layout without installing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from rnmtool.__main__ import apply_transformations, collect_files


# ── Helpers ────────────────────────────────────────────────────────────────────

def make_args(**kwargs) -> argparse.Namespace:
    """Build a minimal Namespace with sensible defaults."""
    defaults = dict(find=None, replace="", regex=False,
                    prefix=None, suffix=None, ext=None, case=None)
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


# ── apply_transformations tests ────────────────────────────────────────────────

class TestPrefix:
    def test_adds_prefix(self):
        args = make_args(prefix="2025_")
        assert apply_transformations("report.txt", args) == "2025_report.txt"

    def test_prefix_preserves_extension(self):
        args = make_args(prefix="new_")
        assert apply_transformations("file.tar.gz", args) == "new_file.tar.gz"


class TestSuffix:
    def test_adds_suffix_before_extension(self):
        args = make_args(suffix="_backup")
        assert apply_transformations("notes.txt", args) == "notes_backup.txt"

    def test_suffix_with_no_extension(self):
        args = make_args(suffix="_v2")
        assert apply_transformations("Makefile", args) == "Makefile_v2"


class TestFindReplace:
    def test_replaces_spaces_with_underscores(self):
        args = make_args(find=" ", replace="_")
        assert apply_transformations("my file name.txt", args) == "my_file_name.txt"

    def test_removes_word_when_replace_empty(self):
        args = make_args(find=" draft", replace="")
        assert apply_transformations("README draft.md", args) == "README.md"

    def test_replace_word(self):
        args = make_args(find="ERROR", replace="error")
        assert apply_transformations("app ERROR log.log", args) == "app error log.log"


class TestRegex:
    def test_strips_leading_digits(self):
        args = make_args(find=r"^\d+\s", replace="", regex=True)
        assert apply_transformations("01 My Notes.txt", args) == "My Notes.txt"

    def test_removes_all_digits(self):
        args = make_args(find=r"\d+", replace="", regex=True)
        assert apply_transformations("report2024.csv", args) == "report.csv"

    def test_regex_replaces_multiple_spaces(self):
        args = make_args(find=r"\s+", replace="_", regex=True)
        assert apply_transformations("my  file  name.txt", args) == "my_file_name.txt"


class TestCase:
    def test_lowercase(self):
        args = make_args(case="lower")
        assert apply_transformations("HELLO WORLD.TXT", args) == "hello world.TXT"

    def test_uppercase(self):
        args = make_args(case="upper")
        assert apply_transformations("hello world.txt", args) == "HELLO WORLD.txt"

    def test_titlecase(self):
        args = make_args(case="title")
        assert apply_transformations("app error log.log", args) == "App Error Log.log"


class TestExtension:
    def test_changes_extension_with_dot(self):
        args = make_args(ext=".jpg")
        assert apply_transformations("photo.jpeg", args) == "photo.jpg"

    def test_changes_extension_without_dot(self):
        args = make_args(ext="yml")
        assert apply_transformations("docker-compose.yaml", args) == "docker-compose.yml"

    def test_normalizes_uppercase_extension(self):
        args = make_args(ext=".xml")
        assert apply_transformations("settings.XML", args) == "settings.xml"


class TestCombined:
    def test_prefix_and_lowercase(self):
        args = make_args(prefix="2025_", case="lower")
        assert apply_transformations("My NOTES.TXT", args) == "2025_my notes.TXT"

    def test_find_replace_and_suffix(self):
        args = make_args(find=" ", replace="_", suffix="_final")
        assert apply_transformations("my file.txt", args) == "my_file_final.txt"

    def test_all_transformations(self):
        args = make_args(find=" ", replace="_", case="lower",
                         prefix="pre_", suffix="_suf", ext=".md")
        assert apply_transformations("Hello World.txt", args) == "pre_hello_world_suf.md"

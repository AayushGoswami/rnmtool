# Changelog

All notable changes to `rnmtool` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-05-16

### Added
- Initial public release
- Batch rename files in any directory
- `--prefix` / `--suffix` - prepend or append text to filenames
- `--find` / `--replace` - plain-text find and replace in filenames
- `--regex` - enable regular expression support for `--find`
- `--case lower|upper|title` - convert filename case
- `--ext` - swap file extensions across matched files
- `--pattern` - glob filter to target specific file types
- `--recursive` - rename files inside subdirectories
- `--dry-run` - safe preview mode, no files are changed
- `--overwrite` - allow overwriting if new name already exists
- Cross-platform support: Windows, macOS, Linux
- Zero external dependencies (uses Python stdlib only)
- Included `test_files/` folder with 12 dummy files for experimentation

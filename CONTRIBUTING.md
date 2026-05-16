# Contributing to rnmtool

Thank you for your interest in contributing! Bug reports, feature requests, and pull requests are all welcome.

---

## Reporting Bugs

Before opening an issue, please:
1. Search [existing issues](https://github.com/AayushGoswami/rnmtool/issues) to avoid duplicates.
2. Include your OS, Python version, and the exact command you ran.
3. Paste the full error output.

---

## Suggesting Features

Open a [GitHub Issue](https://github.com/AayushGoswami/rnmtool/issues/new) with the label `enhancement`.
Describe the problem you're trying to solve, not just the solution - this helps us find the best approach together.

---

## Submitting a Pull Request

1. **Fork** the repository and clone your fork:
   ```bash
   git clone https://github.com/AayushGoswami/rnmtool.git
   cd rnmtool
   ```

2. **Create a branch** for your change:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install in dev mode** (so your changes are reflected immediately):
   ```bash
   pip install -e .
   ```

4. **Make your changes.** Keep them focused - one feature or fix per PR.

5. **Add or update tests** in `tests/test_rename.py` if applicable.

6. **Run tests** before submitting:
   ```bash
   python -m pytest tests/ -v
   ```

7. **Commit** with a clear, descriptive message:
   ```bash
   git commit -m "feat: add --pad flag to zero-pad numeric prefixes"
   ```

8. **Push** your branch and open a Pull Request against `main`.

---

## Code Style

- Follow [PEP 8](https://pep8.org/) conventions.
- Keep functions small and focused.
- Add a docstring to any new public function.
- No external dependencies - this tool uses Python stdlib only.

---

## Questions?

Open a [Discussion](https://github.com/AayushGoswami/rnmtool/discussions) if you're unsure about anything. We're happy to help!

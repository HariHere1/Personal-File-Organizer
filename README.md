# File Organizer CLI

A safety-first Python command-line tool that organizes files into category folders. It plans every move before changing the filesystem, so users can review the exact outcome first.

## Why this is different

Most file organizers move files as soon as they find them. This project separates planning from execution:

- **Dry-run blueprint:** calculates folder creation, moves, and rename decisions in memory before writing anything.
- **Collision-safe:** checks both existing files and destinations reserved during the same run. A duplicate such as `report.pdf` becomes `report (1).pdf` rather than overwriting data.
- **User-controlled:** previews the plan and asks for confirmation; `--dry-run` never changes files.
- **Custom categories:** file types live in `categories.json`, so categories can be changed without editing Python code.
- **Resilient by default:** skips hidden files and folders, and reports locked or inaccessible files without stopping the complete run.

## Requirements

Python 3.6 or newer. No external packages are required.

## Quick start

```bash
python main.py "C:\\path\\to\\folder" --dry-run
```

After reviewing the preview, run without `--dry-run` to confirm interactively:

```bash
python main.py "C:\\path\\to\\folder"
```

For scripts or scheduled tasks, skip confirmation with `-y`:

```bash
python main.py "C:\\path\\to\\folder" -y
```

Running without a path starts interactive mode:

```bash
python main.py
```

## Customizing categories

Edit `categories.json`. Each key becomes a destination folder and its list contains file extensions. Extensions are case-insensitive, and the leading dot is optional.

```json
{
  "Design": [".fig", ".psd", ".ai"],
  "Ebooks": [".epub", ".mobi"]
}
```

Use another configuration file when needed:

```bash
python main.py "C:\\path\\to\\folder" --config my-categories.json --dry-run
```

Extensions not present in the config are moved to `Others`.

## Command-line options

| Argument | Description |
| --- | --- |
| `path` | Optional target folder path. |
| `--dry-run` | Preview planned moves without modifying files. |
| `-y`, `--yes` | Apply the plan without asking for confirmation. |
| `--config PATH` | Use a custom JSON category configuration. |
| `-h`, `--help` | Show command help. |

## How it works

1. Validates the target directory.
2. Loads extension categories from JSON.
3. Scans only files in the chosen directory and builds a collision-free move plan.
4. Shows the plan for review.
5. Executes the approved plan and reports files moved per category.

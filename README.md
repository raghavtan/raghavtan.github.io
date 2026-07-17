# raghavtan.github.io

Static résumé site generator. [`resume_data.py`](resume_data.py) is the **single
source of truth**; running the generator renders it to HTML (the published site),
Markdown, and PDF. Generated files are **not** committed — CI builds and deploys
them on every push to `master`.

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python is managed by uv — see `.python-version`)
- `make`

## Setup

```bash
make setup
```

This syncs the virtual environment from `pyproject.toml` / `uv.lock` and installs
the git pre-commit hooks.

## Everyday commands

| Command         | What it does                                              |
| --------------- | -------------------------------------------------------- |
| `make generate` | Render the résumé into `public/` (index.html, resume.md, resume.pdf) |
| `make serve`    | Generate, then serve `public/` at http://localhost:8000  |
| `make lint`     | Ruff lint                                                |
| `make fmt`      | Ruff format (writes changes)                             |
| `make test`     | Run the pytest suite                                     |
| `make ci`       | Everything CI runs: lint + format-check + tests          |
| `make build`    | `ci` then `generate`                                     |
| `make clean`    | Remove `public/` and caches                              |

Run `make help` for the full list.

## Editing the résumé

1. Edit [`resume_data.py`](resume_data.py).
2. `make serve` to preview locally.
3. Commit — the pre-commit hook runs ruff + tests automatically.
4. Push to `master` — CI regenerates and deploys.

You never edit or commit `index.html` / `resume.*` by hand; they are build output.

## Pre-commit hooks

Installed by `make setup` (config: [`.pre-commit-config.yaml`](.pre-commit-config.yaml)).
On each commit it runs ruff (lint + format) and the test suite. Run manually with:

```bash
uv run pre-commit run --all-files
```

## Deployment

[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) runs on every push
to `master`: it installs deps with uv, runs `make ci`, generates `public/`, and
deploys it to GitHub Pages via GitHub Actions.

The same run publishes the rendered Markdown and PDF to a rolling `latest`
GitHub Release, so there are stable download URLs:

- PDF: `https://github.com/raghavtan/raghavtan.github.io/releases/latest/download/resume.pdf`
- Markdown: `https://github.com/raghavtan/raghavtan.github.io/releases/latest/download/resume.md`

> **One-time setup:** In the repo, go to **Settings → Pages → Build and
> deployment → Source** and select **GitHub Actions** (not "Deploy from a
> branch"). Otherwise Pages keeps serving stale files from the branch instead of
> the freshly built `public/`.

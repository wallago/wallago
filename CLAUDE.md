# wallago

GitHub profile README for [wallago](https://github.com/wallago).

## Layout

- `TEMPLATE.md`: the source of the profile. Edit this, not `README.md`.
- `README.md`: generated from `TEMPLATE.md` by `.github/workflows/stats.yaml`
  (daily and on every push to `main`), which fills the `{{ … }}` stats
  placeholders and commits the result. A hand edit to it is overwritten.
- `assets/`: the logo and its spinning gif; `scripts/spin.py` renders the gif
  frames in Blender, driven by the `gif` recipes in `just/gif.just`.
- `flake.nix`: dev shell (`nix develop`) and the lean CI shell
  (`nix develop .#ci`). Tools the checks run go in `ciTools`.
- `.github/workflows/ci.yml`: one job per `just ci` recipe, each run in the
  flake's CI shell, plus the Nix flake check and the commit-format check.

## Rules

Standalone rules live in `.claude/rules/` and are imported here. Only files
reachable from `CLAUDE.md` get loaded, so a new rule needs a line below.

@.claude/rules/nix.md

## Commands

`just` is the entry point, not the raw toolchain; `just --list` shows every
recipe.

- `just ci`: the gate. It runs every check CI runs, recipe by recipe, so a
  green `just ci` is a green CI. Run it before calling a change done.
- `just all`: re-render the spinning logo gif (needs Blender, so not in CI).

## Constraints

- `editorconfig-checker` holds every file to `.editorconfig`: indentation, final newline, no trailing spaces.
- `typos` runs over the repo. Add a real term to `typos.toml` rather than rewording around it.
- Every link in Markdown is checked. A placeholder URL fails the gate.
- Commit messages are Conventional Commits (`type(scope): subject`); CI checks every commit of a PR with `committed`, and the stats workflow commits as `chore(stats): …`.

## Verifying a change

`just ci` green is the bar. Say which recipes ran when reporting a change.

The gate can't judge how the profile looks: check a `TEMPLATE.md` change in
GitHub's Markdown preview, and the gif by opening it.

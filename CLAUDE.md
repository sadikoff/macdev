# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup & Installation

```bash
pip install -e .
```

Requires Homebrew with `nginx`, at least one `php@X.Y` formula, and `mkcert` installed.

## Commands

```bash
macdev --help
macdev vhost create myapp.test
macdev vhost create myapp.test ~/workspace/myapp --php 8.2
macdev vhost list
macdev vhost remove myapp.test
macdev vhost info myapp.test
macdev php list
macdev php switch 8.4
macdev php switch 8.2 --domain myapp.test
macdev ssl create myapp.test
macdev nginx reload | restart | stop | start | test
```

## Architecture

`macdev` is a Click-based CLI with four command groups, each in its own module:

- **`cli.py`** — entry point; assembles the four groups into the `macdev` root command
- **`config.py`** — derives all paths from `brew --prefix` at import time; nothing is hardcoded
- **`vhost.py`** — creates/removes/lists nginx server block configs; auto-detects `public/` subdirs; calls into `ssl.py` for cert generation and `php.py` for FPM socket lookup
- **`php.py`** — discovers Homebrew PHP installs, reads `php-fpm.d/www.conf` to get the actual FPM listen socket, and handles global PHP switching (stop all → start target → relink)
- **`ssl.py`** — thin wrapper around `mkcert`; certs stored at `~/.macdev/certs/<domain_with_underscores>.pem`
- **`nginx.py`** — runs `nginx -t` before every reload to prevent broken configs from being applied
- **`utils.py`** — shared `console`/`err_console` (Rich), `run()` helper that prints commands before executing, and `brew_service_action()`

### Key design decisions

- All paths flow from `config.BREW` (the result of `brew --prefix`), so Apple Silicon (`/opt/homebrew`) and Intel (`/usr/local`) macs are handled transparently.
- PHP FPM socket is always read from the actual `www.conf` rather than assumed; this handles both TCP (`127.0.0.1:9082`) and unix socket configurations.
- `vhost list` / `vhost info` parse existing nginx conf files with regex rather than storing metadata separately.
- The "head" PHP formula (installed as `php`, not `php@X.Y`) is detected by running `brew --prefix/bin/php -r 'echo PHP_MAJOR_VERSION...'`.

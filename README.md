# macdev

A CLI for managing local macOS development servers — nginx virtual hosts, PHP-FPM versions, and trusted SSL certificates — all backed by Homebrew.

## Requirements

- macOS with [Homebrew](https://brew.sh)
- `nginx` installed via Homebrew
- At least one `php@X.Y` (or `php`) formula installed
- [`mkcert`](https://github.com/FiloSottile/mkcert) installed via Homebrew

```bash
brew install nginx php@8.3 mkcert
```

## Installation

```bash
pip install -e .
```

## Usage

### Virtual hosts

```bash
# Create a vhost for the current directory (auto-detects public/ subdir)
macdev vhost create myapp.test

# Create with explicit root and PHP version
macdev vhost create myapp.test ~/workspace/myapp --php 8.2

# Create with a pre-existing certificate
macdev vhost create myapp.test --cert ~/certs/myapp.pem --key ~/certs/myapp-key.pem

# List all configured vhosts
macdev vhost list

# Show details for a vhost
macdev vhost info myapp.test

# Remove a vhost
macdev vhost remove myapp.test
macdev vhost remove myapp.test --yes   # skip confirmation
```

`vhost create` will:
1. Auto-detect a `public/` subdirectory (for Laravel, Symfony, etc.) and use it as the root
2. Detect the active PHP version if `--php` is not specified
3. Generate a trusted local SSL cert via `mkcert`
4. Write an nginx server block config and reload nginx

### PHP

```bash
# List installed PHP versions, their FPM sockets, and service status
macdev php list

# Switch the vhost for the current directory to PHP 8.4
macdev php switch 8.4

# Switch a specific vhost
macdev php switch 8.2 --domain myapp.test

# Switch all vhosts at once
macdev php switch 8.4 --all
```

`php switch` updates `fastcgi_pass` in the nginx vhost config(s). Run `macdev nginx reload` after switching to apply the change.

### SSL

```bash
# Generate a trusted cert for a domain
macdev ssl create myapp.test

# Generate certs for multiple domains at once
macdev ssl create one.test two.test

# Generate into a custom directory
macdev ssl create myapp.test --out-dir ~/certs

# Inspect a certificate
macdev ssl info ~/.macdev/certs/myapp_test.pem
```

Certificates are stored at `~/.macdev/certs/<domain_with_underscores>.pem` by default.

### nginx

```bash
macdev nginx reload    # test config, then reload without dropping connections
macdev nginx restart   # full restart
macdev nginx start
macdev nginx stop
macdev nginx test      # test config only
```

`reload` always runs `nginx -t` first and aborts if the config has errors.

## How it works

- All paths are derived from `brew --prefix` at startup, so both Apple Silicon (`/opt/homebrew`) and Intel (`/usr/local`) Macs are supported without any configuration.
- The PHP-FPM socket (`fastcgi_pass`) is read directly from `php-fpm.d/www.conf` rather than hardcoded, handling both TCP (`127.0.0.1:9082`) and Unix socket configurations.
- `vhost list` and `vhost info` parse existing nginx conf files — no separate metadata store.
- The "head" PHP formula (installed as `php`, not `php@X.Y`) is detected by running the binary and checking `PHP_MAJOR_VERSION.PHP_MINOR_VERSION`.
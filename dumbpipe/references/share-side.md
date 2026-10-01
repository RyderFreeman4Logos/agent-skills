# Share-side workflows

Read this file when the machine owns an existing service and must make it reachable through a dumbpipe ticket.

## Select the local backend

Ask or infer one of these exact intents:

- **TCP backend:** an application already listens at a host and port such as `127.0.0.1:3000`.
- **Unix backend:** an application already owns an absolute Unix socket such as `/run/user/$(id -u)/app/api.sock`.

The share-side dumbpipe command does not open the backend service. It accepts remote Iroh connections and creates a new local connection to the backend for each stream.

Use a persistent share profile unless the user explicitly wants an ephemeral one-time tunnel. Create it with [persistent-profiles-and-tickets.md](persistent-profiles-and-tickets.md).

## Verify the backend first

TCP examples:

```bash
ss -ltn
# For HTTP-like services, also perform an application-level check:
curl --fail --show-error --silent http://127.0.0.1:3000/ >/dev/null
```

Adapt the health request to the actual protocol. Do not require `curl` for a non-HTTP service.

Unix example:

```bash
test -S /absolute/backend.sock
stat /absolute/backend.sock
```

A listener cannot repair a missing, unready, or permission-denied backend.

## Share a TCP backend

```bash
profile="example"
backend="127.0.0.1:3000"
profile_dir="${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/shares/$profile"

(
  set -a
  . "$profile_dir/identity.env"
  set +a
  exec "$HOME/.local/share/mise/shims/dumbpipe" \
    listen-tcp --host "$backend"
)
```

The persistent ticket to distribute is:

```bash
cat "$profile_dir/ticket"
```

Use the saved short ticket, not a newly scraped listener message.

## Share a Unix backend

```bash
profile="example"
backend_socket="/absolute/backend.sock"
profile_dir="${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/shares/$profile"

(
  set -a
  . "$profile_dir/identity.env"
  set +a
  exec "$HOME/.local/share/mise/shims/dumbpipe" \
    listen-unix --socket-path "$backend_socket"
)
```

Verify that the dumbpipe process's user has permission to connect to the backend socket.

## Optional endpoint bind controls

Dumbpipe normally chooses a random local UDP endpoint port. Only specify `--ipv4-addr` or `--ipv6-addr` when the user has a concrete firewall or network requirement. These options control dumbpipe's Iroh endpoint bind, not the TCP/Unix application backend.

Inspect current syntax first:

```bash
dumbpipe listen-tcp --help
dumbpipe listen-unix --help
```

## Multi-receiver behavior

A single `listen-tcp` or `listen-unix` process accepts multiple endpoint connections and streams, so the same profile ticket may be copied to several receiver devices and used concurrently. Each TCP stream becomes a separate local TCP backend connection; Unix streams likewise become separate Unix backend connections.

This does not provide per-device ACLs or per-device revocation. Use separate share profiles when those properties are required.

Do not substitute stdio `listen` for these commands. Stdio `listen` intentionally exits after its first successful session.

## Foreground validation

Validate at least one real application request from a receive side. A process merely staying alive does not prove that the backend, remote route, or application protocol works.

After validation, ask unless already decided:

> Should I install and enable this share as `dumbpipe-share-<profile>.service` using `systemctl --user enable --now`?

If accepted, continue with [systemd-user-services.md](systemd-user-services.md).

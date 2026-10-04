# Persistent profiles and tickets

Read this file before creating, verifying, repairing, or rotating a reusable share identity.

## Why the secret must persist

Dumbpipe identifies an endpoint with a secret key. If `IROH_SECRET` is absent, dumbpipe generates a random key. `generate-ticket` derives a short reusable endpoint ticket from that identity. A listener started later with the same `IROH_SECRET` is reachable through the same short ticket.

Therefore, the persistent object is the pair:

1. Private `IROH_SECRET` — never distribute it.
2. Public-ish connection ticket — distribute only to intended receivers.

Do not treat a listener's one-time stderr output as the identity store. Generate the short ticket from a saved secret and verify that it can be reproduced.

## XDG layout

Use one identity per independently managed shared service:

```text
${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/
├── install/
│   └── source-build-required           # optional local convention
├── shares/
│   └── <profile>/
│       ├── identity.env                 # IROH_SECRET=...; mode 0600
│       └── ticket                       # one-line short ticket; mode 0600
└── receivers/
    └── <profile>/
        ├── ticket                       # received one-line ticket; mode 0600
        └── ticket.env                   # optional systemd form; mode 0600
```

Use profile names matching `^[A-Za-z0-9_.-]+$`. This keeps file paths and systemd unit names predictable.

## Create a new share profile safely

The following Bash procedure is intentionally refusal-to-overwrite and verifies that the ticket is reproducible. Replace `example` only.

```bash
set -euo pipefail

profile="example"
case "$profile" in
  ""|*[!A-Za-z0-9_.-]*)
    printf 'Invalid dumbpipe profile name: %s\n' "$profile" >&2
    exit 2
    ;;
esac

config_home="${XDG_CONFIG_HOME:-$HOME/.config}"
profile_dir="$config_home/dumbpipe/shares/$profile"
dumbpipe_bin="${DUMBPIPE_BIN:-$HOME/.local/share/mise/shims/dumbpipe}"

umask 077
install -d -m 700 "$profile_dir"

if [[ -e "$profile_dir/identity.env" || -e "$profile_dir/ticket" ]]; then
  printf 'Refusing to overwrite existing profile: %s\n' "$profile_dir" >&2
  exit 3
fi

ticket_tmp="$(mktemp "$profile_dir/.ticket.XXXXXX")"
stderr_tmp="$(mktemp "$profile_dir/.stderr.XXXXXX")"
identity_tmp="$(mktemp "$profile_dir/.identity.env.XXXXXX")"
cleanup() { rm -f -- "$ticket_tmp" "$stderr_tmp" "$identity_tmp"; }
trap cleanup EXIT

if ! "$dumbpipe_bin" generate-ticket >"$ticket_tmp" 2>"$stderr_tmp"; then
  cat "$stderr_tmp" >&2
  exit 4
fi

secret="$(
  sed -n 's/^using secret key \([0-9a-f]\{64\}\)$/\1/p' "$stderr_tmp" \
    | tail -n 1
)"
ticket="$(tr -d '\r\n' <"$ticket_tmp")"

if [[ ! "$secret" =~ ^[0-9a-f]{64}$ ]]; then
  printf 'Could not extract the generated 32-byte IROH secret.\n' >&2
  exit 5
fi
if [[ -z "$ticket" ]]; then
  printf 'dumbpipe generated an empty ticket.\n' >&2
  exit 6
fi

printf 'IROH_SECRET=%s\n' "$secret" >"$identity_tmp"
chmod 600 "$identity_tmp" "$ticket_tmp"
mv -f -- "$identity_tmp" "$profile_dir/identity.env"
mv -f -- "$ticket_tmp" "$profile_dir/ticket"
chmod 600 "$profile_dir/identity.env" "$profile_dir/ticket"

rederived="$(
  IROH_SECRET="$secret" "$dumbpipe_bin" generate-ticket 2>/dev/null \
    | tr -d '\r\n'
)"
if [[ "$rederived" != "$ticket" ]]; then
  printf 'Ticket verification failed; preserving profile for inspection.\n' >&2
  exit 7
fi

printf 'Created persistent dumbpipe profile: %s\n' "$profile_dir"
printf 'Ticket path: %s\n' "$profile_dir/ticket"
```

The current dumbpipe implementation emits a generated secret on stderr as `using secret key <64 lowercase hex characters>`. If a future release changes that output, stop and inspect current source/`--help`; do not guess or create a malformed identity file.

## Verify an existing share profile

```bash
set -euo pipefail
profile="example"
profile_dir="${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/shares/$profile"
dumbpipe_bin="$HOME/.local/share/mise/shims/dumbpipe"

set -a
# This file was created locally with mode 0600.
. "$profile_dir/identity.env"
set +a

derived="$("$dumbpipe_bin" generate-ticket 2>/dev/null | tr -d '\r\n')"
stored="$(tr -d '\r\n' <"$profile_dir/ticket")"
[[ "$derived" == "$stored" ]]
printf 'Profile identity and ticket match.\n'
```

Do not print `IROH_SECRET` during verification.

## Start a listener with the saved identity

Use a subshell so `IROH_SECRET` does not remain exported in the caller's shell:

```bash
(
  set -a
  . "${XDG_CONFIG_HOME:-$HOME/.config}/dumbpipe/shares/example/identity.env"
  set +a
  exec "$HOME/.local/share/mise/shims/dumbpipe" \
    listen-tcp --host 127.0.0.1:3000
)
```

Use `listen-unix --socket-path /absolute/backend.sock` for a Unix backend.

## Rotation and revocation

Rotation changes the endpoint identity and invalidates the old ticket once the old identity is no longer running.

1. Stop the profile's listener/service.
2. Preserve the old profile as a permission-protected backup only when rollback is needed; otherwise securely remove it according to the user's policy.
3. Create a new profile identity and ticket.
4. Start and test the new listener.
5. Distribute the new ticket to authorized receivers.
6. Remove the old ticket from receiver profiles.

Never rotate silently. Every receiver using that shared ticket will lose access.

For independent per-device revocation, create a separate share profile/listener per receiver or trust group from the beginning. Dumbpipe itself does not encode per-receiver ACLs in one ticket.

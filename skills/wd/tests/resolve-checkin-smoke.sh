#!/bin/sh
set -eu

skillcfg_bin=${1:?pass the freshly built skillcfg executable}
case "$skillcfg_bin" in
  /*) ;;
  *) printf 'skillcfg executable path must be absolute\n' >&2; exit 2 ;;
esac
[ -x "$skillcfg_bin" ] || { printf 'skillcfg executable is not executable\n' >&2; exit 2; }
script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
resolver="$script_dir/../scripts/resolve-checkin.sh"
tmp=$(mktemp -d "${TMPDIR:-/tmp}/skillcfg-wd.XXXXXX")
original_path=$PATH
cleanup() {
  PATH=$original_path
  export PATH
  /bin/rm -rf "$tmp"
}
trap cleanup 0 HUP INT TERM
mkdir "$tmp/bin"
ln -s "$skillcfg_bin" "$tmp/bin/skillcfg"
PATH=$tmp/bin
export PATH
HOME=$tmp/home
export HOME
unset XDG_CONFIG_HOME || :

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
checks=0
expect_value() {
  provider=$1
  config=$2
  expected=$3
  actual=$(ACTIVE_PROVIDER="$provider" SKILLCFG_CONFIG="$tmp/$config" "$resolver") || fail "$provider unexpectedly failed"
  [ "$actual" = "$expected" ] || fail "$provider returned '$actual', expected '$expected'"
  checks=$((checks + 1))
}
expect_error() {
  provider=$1
  config=$2
  expected=$3
  set +e
  output=$(ACTIVE_PROVIDER="$provider" SKILLCFG_CONFIG="$tmp/$config" "$resolver" 2>&1)
  status=$?
  set -e
  [ "$status" -eq 2 ] || fail "$provider exited $status, expected 2: $output"
  case "$output" in *"$expected"*) ;; *) fail "$provider error omitted '$expected': $output" ;; esac
  checks=$((checks + 1))
}

if command -v csa >/dev/null 2>&1; then
  fail 'csa is present in the isolated PATH'
fi
checks=$((checks + 1))

printf '%s\n' 'schema_version = 1' '' '[kv_cache.provider_ttls]' 'openai-codex = 101' 'codex = 102' 'openai = 103' 'gpt = 104' 'deepseek = 105' 'grok = 106' 'localrouter = 107' 'pm = 108' > "$tmp/exact.toml"
printf '%s\n' 'schema_version = 1' '' '[kv_cache.provider_ttls]' 'codex = 202' 'openai = 203' 'gpt = 204' 'deepseek = 205' 'grok = 206' > "$tmp/aliases.toml"
printf '%s\n' 'schema_version = 1' '' '[kv_cache.provider_ttls]' 'gpt = 304' > "$tmp/gpt.toml"
printf '%s\n' 'schema_version = 1' '' '[kv_cache.provider_ttls]' 'grok-chat = 0' 'grok = 999' > "$tmp/nonpositive.toml"
printf '%s\n' 'schema_version = 1' '' '[kv_cache.provider_ttls]' 'grok = "3s"' > "$tmp/nonnumeric.toml"
printf '%s\n' 'schema_version = "1"' > "$tmp/bad-schema.toml"
printf '%s\n' 'schema_version = 1' '' '[kv_cache.provider_ttls]' 'openai = 808' > "$tmp/openai.toml"

expect_value openai-codex exact.toml 101
expect_value openai-codex aliases.toml 202
expect_value openai-enterprise aliases.toml 203
expect_value gpt-4.1 aliases.toml 203
expect_value deepseek-chat aliases.toml 205
expect_value grok-4 aliases.toml 206
expect_value xai-chat aliases.toml 206
expect_value localrouter aliases.toml 206
expect_value pm openai.toml 808
expect_value pm gpt.toml 304
expect_error grok-chat nonpositive.toml 'non-positive TTL for provider key grok-chat'
expect_error grok-chat nonnumeric.toml 'invalid TTL for provider key grok'
expect_error unknown aliases.toml 'unsupported active provider: unknown'
expect_error grok missing.toml 'skillcfg could not load its selected schema_version=1 configuration'
expect_error grok bad-schema.toml 'skillcfg could not load its selected schema_version=1 configuration'
expect_error grok openai.toml 'no configured KV-cache TTL for active provider grok'

printf 'ok: %s resolver checks; isolated skillcfg TOML and CSA-absent PATH\n' "$checks"

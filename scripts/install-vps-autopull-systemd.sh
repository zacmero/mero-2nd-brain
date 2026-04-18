#!/usr/bin/env bash

set -euo pipefail

show_help() {
    cat <<'EOF'
Usage: scripts/install-vps-autopull-systemd.sh [--interval MINUTES] [--linger]

Installs a user-level systemd timer that keeps this repo up to date on a VPS
and refreshes the Syncthing compose stack after a successful fast-forward pull.

Options:
  --interval MINUTES  Pull interval in minutes. Default: 5
  --linger            Enable user lingering for this account if sudo is available.
                      This lets the user service run without an active login session.
EOF
}

INTERVAL_MINUTES=5
ENABLE_LINGER=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --interval)
            INTERVAL_MINUTES="${2:-}"
            shift 2
            ;;
        --linger)
            ENABLE_LINGER=1
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            show_help >&2
            exit 1
            ;;
    esac
done

if ! [[ "$INTERVAL_MINUTES" =~ ^[0-9]+$ ]] || [[ "$INTERVAL_MINUTES" -lt 1 ]]; then
    echo "[!] --interval must be a positive integer number of minutes." >&2
    exit 1
fi

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if ! git -C "$REPO_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "[!] $REPO_DIR is not a git repository." >&2
    exit 1
fi

BRANCH="$(git -C "$REPO_DIR" branch --show-current || true)"
if [[ -z "$BRANCH" ]]; then
    BRANCH="master"
fi

REMOTE="${REMOTE:-origin}"
STATE_DIR="$HOME/.local/share/mero-2nd-brain-vps-autopull"
BIN_DIR="$HOME/.local/bin"
SYSTEMD_DIR="$HOME/.config/systemd/user"
PULL_SCRIPT="$STATE_DIR/pull-and-reload.sh"
SERVICE_FILE="$SYSTEMD_DIR/mero-2nd-brain-vps-autopull.service"
TIMER_FILE="$SYSTEMD_DIR/mero-2nd-brain-vps-autopull.timer"

mkdir -p "$STATE_DIR" "$BIN_DIR" "$SYSTEMD_DIR"

cat > "$PULL_SCRIPT" <<EOF
#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$REPO_DIR"
REMOTE="$REMOTE"
BRANCH="$BRANCH"

reload_vps_stack() {
    local infra_dir="\$REPO_DIR/vps-infra"

    if [[ ! -f "\$infra_dir/docker-compose.yml" ]]; then
        echo "[vps-autopull] no vps-infra docker-compose.yml found, skipping reload"
        return 0
    fi

    if ! command -v docker >/dev/null 2>&1; then
        echo "[vps-autopull] docker not available, cannot reload vps stack" >&2
        return 1
    fi

    echo "[vps-autopull] refreshing Syncthing stack in \$infra_dir"
    docker compose -f "\$infra_dir/docker-compose.yml" --project-directory "\$infra_dir" up -d --remove-orphans
}

if [[ ! -d "\$REPO_DIR/.git" ]]; then
    echo "[vps-autopull] repo missing: \$REPO_DIR" >&2
    exit 1
fi

if [[ -n "\$(git -C "\$REPO_DIR" status --porcelain --untracked-files=all)" ]]; then
    echo "[vps-autopull] dirty worktree, skipping pull for \$REPO_DIR"
    exit 0
fi

before_head="\$(git -C "\$REPO_DIR" rev-parse HEAD)"
git -C "\$REPO_DIR" fetch "\$REMOTE" "\$BRANCH"
git -C "\$REPO_DIR" pull --ff-only "\$REMOTE" "\$BRANCH"
after_head="\$(git -C "\$REPO_DIR" rev-parse HEAD)"

if [[ "\$before_head" != "\$after_head" ]]; then
    reload_vps_stack
else
    echo "[vps-autopull] no new commit, no stack reload needed"
fi
EOF

chmod 0755 "$PULL_SCRIPT"

ln -sf "$PULL_SCRIPT" "$BIN_DIR/mero-2nd-brain-vps-autopull"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Mero 2nd Brain VPS repo autopull
Documentation=file://$REPO_DIR/vps-infra/INFRA-README.md

[Service]
Type=oneshot
ExecStart=%h/.local/share/mero-2nd-brain-vps-autopull/pull-and-reload.sh

[Install]
WantedBy=default.target
EOF

cat > "$TIMER_FILE" <<EOF
[Unit]
Description=Periodic VPS autopull for Mero 2nd Brain

[Timer]
OnBootSec=2min
OnUnitActiveSec=${INTERVAL_MINUTES}min
RandomizedDelaySec=45s
Persistent=true
Unit=mero-2nd-brain-vps-autopull.service

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now mero-2nd-brain-vps-autopull.timer

if [[ "$ENABLE_LINGER" -eq 1 ]]; then
    if command -v sudo >/dev/null 2>&1; then
        sudo loginctl enable-linger "$USER"
        echo "[+] Enabled lingering for $USER."
    else
        echo "[!] sudo not found; skipping linger enable."
    fi
fi

cat <<EOF
[+] Installed VPS user timer.
[+] Repo: $REPO_DIR
[+] Branch: $BRANCH
[+] Interval: every ${INTERVAL_MINUTES} minutes
[+] Timer: systemctl --user status mero-2nd-brain-vps-autopull.timer
[+] Logs: journalctl --user -u mero-2nd-brain-vps-autopull.service -f
EOF

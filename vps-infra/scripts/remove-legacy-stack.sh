#!/usr/bin/env bash

set -euo pipefail

INFRA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." &> /dev/null && pwd)"

owns_container() {
    local name="$1"
    local working_dir

    working_dir="$(sudo docker inspect -f '{{ index .Config.Labels "com.docker.compose.project.working_dir" }}' "$name" 2>/dev/null || true)"

    if [[ "$working_dir" == "$INFRA_DIR" ]]; then
        return 0
    fi

    sudo docker inspect "$name" --format '{{ range .Mounts }}{{ println .Source }}{{ end }}' 2>/dev/null \
        | grep -Fxq "$INFRA_DIR/dbdata"
}

remove_if_owned() {
    local name="$1"

    if ! sudo docker ps -a --format '{{.Names}}' | grep -Fxq "$name"; then
        echo "[i] Container '$name' not present. Skipping."
        return 0
    fi

    if owns_container "$name"; then
        echo "[+] Removing legacy container '$name' managed from $INFRA_DIR"
        sudo docker rm -f "$name"
    else
        echo "[!] Refusing to remove '$name' because it is not clearly owned by $INFRA_DIR"
    fi
}

echo "============================================="
echo " Remove Legacy LiveSync Stack "
echo "============================================="
echo "This removes only the old sync stack created by this repo."
echo "It does NOT wipe the VM or touch unrelated services."

remove_if_owned couchdb
remove_if_owned caddy

for path in "$INFRA_DIR/.env" "$INFRA_DIR/Caddyfile"; do
    if [[ -e "$path" ]]; then
        echo "[+] Deleting $path"
        rm -f "$path"
    fi
done

if [[ -d "$INFRA_DIR/dbdata" ]]; then
    echo "[+] Deleting $INFRA_DIR/dbdata"
    rm -rf "$INFRA_DIR/dbdata"
fi

echo "[+] Legacy CouchDB files removed from $INFRA_DIR"
echo "============================================="

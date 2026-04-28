import paramiko
import sys

def run_ssh_command(host, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username='root', password=password, timeout=10)
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        ssh.close()
        return out, err
    except Exception as e:
        return "", str(e)

host = '192.168.15.244'
password = 'kindle'

# 1. Find clippings
out, err = run_ssh_command(host, password, 'find /mnt/us/documents -iname "*clippings*.txt"')
if err:
    print(f"Error finding clippings: {err}")
    sys.exit(1)

clippings_path = out.strip()
print(f"Found clippings at: {clippings_path}")

if not clippings_path:
    print("Could not find clippings path!")
    sys.exit(1)

# 2. Setup KUAL Extension
kual_menu = """{
  "items": [
    {
      "name": "Sync Clippings to VPS",
      "priority": 1,
      "action": "bin/sync.sh"
    }
  ]
}"""

sync_script = f"""#!/bin/sh
VPS_USER="ubuntu"
VPS_IP="204.216.172.41"
VPS_TARGET_DIR="/mero-2nd-brain/"
CLIPPINGS_PATH="{clippings_path}"
KEY_SOURCE="/mnt/us/usbnet/id_ed25519"
KEY_TMP="/tmp/id_ed25519"
SSH_BIN="/mnt/us/usbnet/bin/ssh"
SCP_BIN="/mnt/us/usbnet/bin/scp"

cp $KEY_SOURCE $KEY_TMP
chmod 600 $KEY_TMP

$SCP_BIN -i $KEY_TMP -o StrictHostKeyChecking=accept-new "$CLIPPINGS_PATH" ${{VPS_USER}}@${{VPS_IP}}:${{VPS_TARGET_DIR}}My_Clippings.txt
"""

setup_commands = f"""
mkdir -p /mnt/us/extensions/sync_clippings/bin
cat << 'EOF' > /mnt/us/extensions/sync_clippings/menu.json
{kual_menu}
EOF
cat << 'EOF' > /mnt/us/extensions/sync_clippings/bin/sync.sh
{sync_script}
EOF
chmod +x /mnt/us/extensions/sync_clippings/bin/sync.sh
"""

out, err = run_ssh_command(host, password, setup_commands)
if err:
    print(f"Error setting up KUAL extension: {err}")
else:
    print("KUAL extension set up successfully!")

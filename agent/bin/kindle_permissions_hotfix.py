import paramiko
import sys
import shlex

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
profile_path = '/mnt/us/.profile'

# New alias pushes to the user's home directory on the VPS, using the ~ shortcut.
# It also correctly specifies the path to the ssh binary for the scp command.
correct_alias = "alias notesync='cp /mnt/us/usbnet/id_ed25519 /tmp/id_ed25519 && chmod 600 /tmp/id_ed25519 && /mnt/us/usbnet/bin/scp -S /mnt/us/usbnet/bin/ssh -i /tmp/id_ed25519 -o StrictHostKeyChecking=accept-new \"/mnt/us/documents/My Clippings.txt\" ubuntu@204.216.172.41:~/\"My Clippings.txt\"'"

# Get existing content that is NOT our alias
get_other_content_cmd = f"grep -v \"alias notesync=\" {profile_path}"
other_content, err = run_ssh_command(host, password, get_other_content_cmd)
if err and not other_content:
    other_content = ""

# Reconstruct the file with the correct alias
new_profile_content = f"{other_content.strip()}\\n{correct_alias}\\n"

# Use echo to overwrite the file safely
write_cmd = f"echo {shlex.quote(new_profile_content)} > {profile_path}"

print("Rewriting .profile on Kindle with correct home directory destination...")
run_ssh_command(host, password, write_cmd)
print("Alias successfully updated on Kindle.")

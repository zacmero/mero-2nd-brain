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

# The final, atomic, one-command alias.
# 1. SCP the file to the VPS home directory.
# 2. On success (&&), SSH to the VPS and execute the python parser script.
final_alias = "alias notesync='cp /mnt/us/usbnet/id_ed25519 /tmp/id_ed25519 && chmod 600 /tmp/id_ed25519 && /mnt/us/usbnet/bin/scp -S /mnt/us/usbnet/bin/ssh -i /tmp/id_ed25519 -o StrictHostKeyChecking=accept-new \"/mnt/us/documents/My Clippings.txt\" ubuntu@204.216.172.41:~/\"My_Clippings.txt\" && /mnt/us/usbnet/bin/ssh -i /tmp/id_ed25519 ubuntu@204.216.172.41 \"python3 /mero-2nd-brain/scripts/parse_clippings.py\"'"

# Get existing content that is NOT our alias
get_other_content_cmd = f"grep -v \"alias notesync=\" {profile_path}"
other_content, err = run_ssh_command(host, password, get_other_content_cmd)
if err and not other_content:
    other_content = ""

# Reconstruct the file with the correct alias
new_profile_content = f"{other_content.strip()}\\n{final_alias}\\n"

# Use echo to overwrite the file safely
write_cmd = f"echo {shlex.quote(new_profile_content)} > {profile_path}"

print("Deploying final 'notesync' alias to Kindle...")
run_ssh_command(host, password, write_cmd)
print("Alias successfully deployed.")

# Verify
print("\nVerifying final content:")
out, err = run_ssh_command(host, password, f"cat {profile_path}")
print(out)

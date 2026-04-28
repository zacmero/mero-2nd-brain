#!/bin/sh

# This script is meant to be run on the Kindle, e.g., via KUAL or KTerm.
# It syncs the "My Clippings.txt" file to the VPS where the processing script runs.

VPS_USER="ubuntu"
VPS_IP="204.216.172.41"

# Adjust this path if mero-2nd-brain is located elsewhere on the VPS
# For example, if it's in the home directory, use: ~/mero-2nd-brain/
VPS_TARGET_DIR="/mero-2nd-brain/"

CLIPPINGS_PATH="/mnt/us/documents/My Clippings.txt"
KEY_SOURCE="/mnt/us/usbnet/id_ed25519"
KEY_TMP="/tmp/id_ed25519"
SSH_BIN="/mnt/us/usbnet/bin/ssh"
SCP_BIN="/mnt/us/usbnet/bin/scp"

echo "Setting up SSH key..."
cp $KEY_SOURCE $KEY_TMP
chmod 600 $KEY_TMP

echo "Pushing My Clippings.txt to VPS..."
# Using scp to push the file to the VPS
$SCP_BIN -i $KEY_TMP -o StrictHostKeyChecking=accept-new "$CLIPPINGS_PATH" ${VPS_USER}@${VPS_IP}:${VPS_TARGET_DIR}My_Clippings.txt

if [ $? -eq 0 ]; then
    echo "Successfully pushed clippings to VPS!"
    
    # Optional: trigger the parsing script on the VPS remotely
    # echo "Triggering processing script on VPS..."
    # $SSH_BIN -i $KEY_TMP -o StrictHostKeyChecking=accept-new ${VPS_USER}@${VPS_IP} "cd ${VPS_TARGET_DIR} && python3 scripts/parse_clippings.py"
else
    echo "Error pushing clippings. Please check network and paths."
fi

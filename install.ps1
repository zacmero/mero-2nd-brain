# Obsidian Vault Git Environment Setup Script (Windows)

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host " Setting up Obsidian Environment (Windows)" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

$DefaultVault = "$env:USERPROFILE\Documents\mero-vault"
$VaultInput = Read-Host "Enter path to your vault [default: $DefaultVault]"
if ([string]::IsNullOrWhiteSpace($VaultInput)) {
    $VaultDir = $DefaultVault
} else {
    $VaultDir = $VaultInput
}

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigSource = "$RepoDir\obsidian-config"

if (!(Test-Path $VaultDir)) {
    Write-Host "[+] Creating vault directory at $VaultDir..."
    New-Item -ItemType Directory -Force -Path $VaultDir | Out-Null
}

$ObsidianFolder = "$VaultDir\.obsidian"

if (Test-Path $ObsidianFolder) {
    $Item = Get-Item $ObsidianFolder
    if ($Item.Attributes -match "ReparsePoint") {
        Write-Host "[+] Symlink already exists. Re-creating to ensure correct path..."
        Remove-Item $ObsidianFolder
    } else {
        Write-Host "[!] Found physical .obsidian folder. Backing it up to .obsidian.bak..." -ForegroundColor Yellow
        Rename-Item -Path $ObsidianFolder -NewName ".obsidian.bak"
    }
}

Write-Host "[+] Linking $ConfigSource -> $ObsidianFolder"
try {
    New-Item -ItemType SymbolicLink -Path $ObsidianFolder -Target $ConfigSource | Out-Null
    Write-Host "===============================================" -ForegroundColor Green
    Write-Host " Setup Complete! " -ForegroundColor Green
    Write-Host " Remember to configure Syncthing to sync: $VaultDir" -ForegroundColor Green
    Write-Host "===============================================" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to create symlink." -ForegroundColor Red
    Write-Host "On Windows, creating symbolic links requires you to either:" -ForegroundColor Red
    Write-Host "1. Run PowerShell as Administrator." -ForegroundColor Red
    Write-Host "2. Enable 'Developer Mode' in Windows Settings." -ForegroundColor Red
}

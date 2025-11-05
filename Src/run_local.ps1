Write-Host "== Step 1: Running Moltemplate =="

if (Test-Path "system.data") {
    Remove-Item "system.data" -Force
}

# This uses bash to run moltemplate.sh inside the cloned folder
bash "../moltemplate/scrits/moltemplate.sh" -atomstyle atomic system.lt

if (!(Test-Path "system.data")) {
    Write-Host "ERROR: system.data was not created. Check system.lt and loop.lt." -ForegroundColor Red
    exit 1
}

Write-Host "`nSUCCESS: system.data generated."

# Find LAMMPS binary
$lmp = "lmp_serial"
if (!(Get-Command $lmp -ErrorAction SilentlyContinue)) {
    $lmp = "lmp"
}
if (!(Get-Command $lmp -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: LAMMPS not found. Install or add lmp/lmp_serial to PATH." -ForegroundColor Red
    exit 1
}

Write-Host "`n== Step 2: Running LAMMPS =="
& $lmp -in in.lammps

if (Test-Path "log.lammps") {
    Write-Host "`n== Step 3: Sample Output from log.lammps =="
    Get-Content log.lammps -TotalCount 20
} else {
    Write-Host "WARNING: log.lammps not found. LAMMPS may have failed to run." -ForegroundColor Yellow
}

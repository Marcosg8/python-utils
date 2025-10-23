# Script para crear un entorno virtual y instalar dependencias (PowerShell)
# Uso: abrir PowerShell en la carpeta del proyecto y ejecutar:
# .\setup_env.ps1

param(
    [switch]$Force
)

$venvDir = ".venv"

Write-Host "Comprobando versión de Python..."
try {
    python --version | Out-Null
} catch {
    Write-Error "No se encontró 'python' en PATH. Asegúrate de tener Python instalado."
    exit 1
}

# Manejo robusto de existencia y recreación del venv
if (Test-Path $venvDir) {
    if ($Force) {
        Write-Host "El directorio $venvDir existe y se forzará su recreación..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $venvDir
        Write-Host "Creando entorno virtual en $venvDir..."
        python -m venv $venvDir
    } else {
        Write-Host "El directorio $venvDir ya existe. Use -Force para recrearlo." -ForegroundColor Cyan
    }
} else {
    Write-Host "Creando entorno virtual en $venvDir..."
    python -m venv $venvDir
}

$activateScript = Join-Path $venvDir 'Scripts\Activate.ps1'
if (Test-Path $activateScript) {
    Write-Host "Para activar el entorno, ejecute:" -ForegroundColor Green
    Write-Host "    .\\$venvDir\\Scripts\\Activate.ps1" -ForegroundColor Yellow
} else {
    Write-Warning "No se encontró el script de activación en $activateScript"
}

Write-Host "Instalando dependencias desde requirements.txt..."
# Usar el ejecutable python del venv si existe, evitando problemas con rutas con espacios
$pipExe = Join-Path $venvDir 'Scripts\python.exe'
if (Test-Path $pipExe) {
    Write-Host "Instalando con: $pipExe -m pip install -r requirements.txt"
    & "$pipExe" -m pip install -r requirements.txt
} else {
    Write-Warning "No se encontró $pipExe; se intentará usar el pip del sistema."
    python -m pip install -r requirements.txt
}

Write-Host "Listo. Si la política de ejecución bloquea scripts, ejecute como administrador:`nSet-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan

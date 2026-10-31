# Build the frontend, then start Universum at http://127.0.0.1:8000
$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
    Set-Location frontend
    npm run build
    if ($LASTEXITCODE -ne 0) { throw "Frontend build failed" }

    Set-Location ..\backend
    .\.venv\Scripts\fastapi.exe run main.py --host 127.0.0.1 --port 8000
}
finally {
    Pop-Location
}

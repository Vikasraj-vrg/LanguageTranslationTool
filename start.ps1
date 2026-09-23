Set-Location "C:\Users\vg362\Desktop\LanguageTranslationTool"

& ".\.venv\Scripts\Activate.ps1"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\vg362\Desktop\LanguageTranslationTool'; & '.\.venv\Scripts\Activate.ps1'; libretranslate --load-only en,hi"

Write-Host ""
Write-Host "Starting LibreTranslate..."
Write-Host "Waiting for LibreTranslate on port 5000..."
Write-Host ""

$ready = $false

for ($i = 1; $i -le 30; $i++) {
    Start-Sleep -Seconds 2

    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            $ready = $true
            break
        }
    }
    catch {
        Write-Host "Waiting... ($i/30)"
    }
}

if (-not $ready) {
    Write-Host ""
    Write-Host "LibreTranslate did not start correctly."
    Write-Host "Please check the LibreTranslate window."
    Read-Host "Press Enter to exit"
    exit
}

Write-Host ""
Write-Host "LibreTranslate is ready!"
Write-Host "Starting website on port 5001..."
Write-Host ""

python app.py
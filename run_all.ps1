# -----------------------------
# run_all.ps1
# -----------------------------

# Paths
$projectRoot = "C:\Users\marya\Attendance-tracker"
$backendDir = "$projectRoot\Backend"
$pythonApp = "$backendDir\app.py"

# Start Python backend
Write-Host "Starting Python backend..."
$pyProcess = Start-Process python -ArgumentList $pythonApp -PassThru

# Wait until backend is ready (retry for max 30 seconds)
$maxRetries = 30
$retry = 0
$backendReady = $false

while (-not $backendReady -and $retry -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            Write-Host "Backend is ready!"
        }
    } catch {
        Start-Sleep -Seconds 1
        $retry++
    }
}

if (-not $backendReady) {
    Write-Host "Backend did not start in time." -ForegroundColor Red
    try {
        if ($pyProcess -and !$pyProcess.HasExited) {
            $pyProcess.Kill()
            Write-Host "Killed the backend process."
        }
    } catch {
        Write-Host "Backend process already exited, skipping Kill()."
    }
    exit 1
}

# Open default browser to home page
Write-Host "Opening browser to http://127.0.0.1:5000/"
Start-Process "http://127.0.0.1:5000/"

# Keep the script running until user presses Ctrl+C
Write-Host "Press Ctrl+C to stop the script and backend."
try {
    while ($true) {
        Start-Sleep -Seconds 1
        if ($pyProcess.HasExited) {
            Write-Host "Backend process exited."
            break
        }
    }
} catch {
    Write-Host "Stopping script..."
    try {
        if ($pyProcess -and !$pyProcess.HasExited) {
            $pyProcess.Kill()
        }
    } catch {}
}

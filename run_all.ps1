$projectRoot = "C:\Users\marya\Attendance-Tracker"
$backendScript = "$projectRoot\Backend\app.py"
$frontendDir = "$projectRoot\Frontend"
$mainJava = "$frontendDir\Main.java"

# -----------------------------
# Start Python backend
# -----------------------------
Write-Host "Starting Python backend..."
$pyProcess = Start-Process python -ArgumentList $backendScript -PassThru

# -----------------------------
# Wait until backend responds
# -----------------------------
$backendReady = $false
$maxRetries = 15
$retry = 0

while (-not $backendReady -and $retry -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/attendance/list" -UseBasicParsing
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
    $pyProcess.Kill()
    exit 1
}

# -----------------------------
# Compile Java frontend
# -----------------------------
Write-Host "Compiling Java frontend..."
javac -d "$frontendDir" $mainJava
if ($LASTEXITCODE -ne 0) {
    Write-Host "Compilation failed!" -ForegroundColor Red
    $pyProcess.Kill()
    exit 1
}

# -----------------------------
# Run Java frontend
# -----------------------------
Write-Host "Running Java frontend..."
java -cp "$frontendDir" Frontend.Main

# -----------------------------
# Stop Python backend
# -----------------------------
$pyProcess.Kill()
Write-Host "Python backend stopped."

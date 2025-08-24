# -----------------------------
# run_all.ps1
# -----------------------------
# Paths
$projectRoot = "C:\Users\marya\Attendance-tracker"
$frontendDir = "$projectRoot\Frontend"
$backendDir = "$projectRoot\Backend"
$jsonJar = "$frontendDir\json-20210307.jar"
$mainJava = "$frontendDir\Main.java"
$pythonApp = "$backendDir\app.py"

# -----------------------------
# Download JSON library if missing
# -----------------------------
if (-not (Test-Path $jsonJar)) {
    Write-Host "Downloading org.json library..."
    Invoke-WebRequest -Uri "https://repo1.maven.org/maven2/org/json/json/20210307/json-20210307.jar" -OutFile $jsonJar
}

# -----------------------------
# Start Python backend
# -----------------------------
Write-Host "Starting Python backend..."
$pythonProcess = Start-Process python -ArgumentList $pythonApp -PassThru

# -----------------------------
# Wait until backend is ready
# -----------------------------
$maxRetries = 15
$retry = 0
$backendReady = $false

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
    $pythonProcess.Kill()
    exit 1
}

# -----------------------------
# Compile Java frontend
# -----------------------------
Write-Host "Compiling Frontend/Main.java..."
javac -cp ".;$jsonJar" $mainJava
if ($LASTEXITCODE -ne 0) {
    Write-Host "Compilation failed!" -ForegroundColor Red
    $pythonProcess.Kill()
    exit 1
}

# -----------------------------
# Run Java frontend and wait until it exits
# -----------------------------
Write-Host "Running Frontend.Main..."
$javaProcess = Start-Process java -ArgumentList "-cp", ".;$jsonJar", "Frontend.Main" -PassThru
$javaProcess.WaitForExit()

# -----------------------------
# Stop Python backend
# -----------------------------
if (-not $pythonProcess.HasExited) {
    $pythonProcess.Kill()
}
Write-Host "Python backend stopped."

# run_attendance.ps1

# -----------------------------
# Paths
# -----------------------------
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

# Wait a few seconds for the Flask server to start
Start-Sleep -Seconds 5

# -----------------------------
# Compile Java frontend
# -----------------------------
Write-Host "Compiling Frontend/Main.java..."
javac -cp ".;$jsonJar" $mainJava
if ($LASTEXITCODE -ne 0) {
    Write-Host "Compilation failed!" -ForegroundColor Red
    # Stop Python backend before exiting
    $pythonProcess.Kill()
    exit 1
}

# -----------------------------
# Run Java frontend
# -----------------------------
Write-Host "Running Frontend.Main..."
java -cp ".;$jsonJar" Frontend.Main

# -----------------------------
# Optional: Stop Python backend after Java closes
# -----------------------------
$pythonProcess.Kill()
Write-Host "Python backend stopped."

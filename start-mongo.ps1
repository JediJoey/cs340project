# Starts the portable MongoDB (auth enabled) used by this project.
# Run: ./start-mongo.ps1
$base = Join-Path $env:LOCALAPPDATA 'mongodb'
$bin  = Join-Path $base 'bin'
$data = Join-Path $base 'data'
$log  = Join-Path $base 'log\mongod.log'

if (Get-Process mongod -ErrorAction SilentlyContinue) {
    Write-Host 'mongod is already running.'
    return
}

Start-Process -FilePath (Join-Path $bin 'mongod.exe') `
    -ArgumentList @('--auth', '--dbpath', "`"$data`"", '--port', '27017',
                    '--bind_ip', '127.0.0.1', '--logpath', "`"$log`"") `
    -WindowStyle Hidden

Start-Sleep -Seconds 4
if ((Test-NetConnection -ComputerName 127.0.0.1 -Port 27017 -WarningAction SilentlyContinue).TcpTestSucceeded) {
    Write-Host 'mongod started and listening on 127.0.0.1:27017.'
} else {
    Write-Host 'mongod did not start; check the log:' $log
}

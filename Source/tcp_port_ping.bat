@echo off
setlocal

set /p HOSTNAME=Enter the IP or hostname: 
set /p PORT=Enter the port number: 

echo Pinging %HOSTNAME% on port %PORT%...

:loop
powershell -Command "$tcpClient = New-Object System.Net.Sockets.TcpClient; $timeout = 1000; $stopwatch = [System.Diagnostics.Stopwatch]::StartNew(); $asyncResult = $tcpClient.BeginConnect('%HOSTNAME%', %PORT%, $null, $null); if ($asyncResult.AsyncWaitHandle.WaitOne($timeout)) { $tcpClient.EndConnect($asyncResult); $stopwatch.Stop(); Write-Host 'Connection succeeded to %HOSTNAME%:%PORT% (Response Time: ' $stopwatch.ElapsedMilliseconds 'ms)' -ForegroundColor Green; $tcpClient.Close() } else { $tcpClient.Close(); Write-Host 'Connection timed out' -ForegroundColor Red }"
timeout /T 1 > nul
goto loop

endlocal
exit /b 0

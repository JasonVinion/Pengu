@echo off
setlocal

set /p HOSTNAME=Enter the IP or hostname: 

echo Pinging %HOSTNAME%...

:loop
powershell -Command "$ping = New-Object System.Net.NetworkInformation.Ping; $timeout = 1000; $pingReply = $ping.Send('%HOSTNAME%', $timeout); if ($pingReply.Status -eq 'Success') { Write-Host 'Ping succeeded to %HOSTNAME% (Response Time: ' $pingReply.RoundtripTime 'ms)' -ForegroundColor Green } else { Write-Host 'Ping timed out' -ForegroundColor Red }"
timeout /T 1 > nul
goto loop

endlocal
exit /b 0

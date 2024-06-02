@echo off
setlocal

set /p HOSTNAME=Enter the URL (e.g., http://example.com or https://example.com): 

echo Checking HTTP(S) connection to %HOSTNAME%...

:loop
powershell -Command "$timeout = 1000; $stopwatch = [System.Diagnostics.Stopwatch]::StartNew(); try { $response = Invoke-WebRequest -Uri '%HOSTNAME%' -TimeoutSec ($timeout / 1000); if ($response.StatusCode -eq 200) { $stopwatch.Stop(); Write-Host 'HTTP(S) connection succeeded to %HOSTNAME% (Response Time: ' $stopwatch.ElapsedMilliseconds 'ms)' -ForegroundColor Green } else { Write-Host 'HTTP(S) connection failed with status code: ' $response.StatusCode -ForegroundColor Red } } catch { Write-Host 'HTTP(S) connection timed out or failed' -ForegroundColor Red }"
timeout /T 1 > nul
goto loop

endlocal
exit /b 0

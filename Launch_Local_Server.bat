@echo off
title QuantRisk Enterprise™ Local Server
echo ================================================================
echo   Starting QuantRisk Enterprise Server & Opening Browser...
echo ================================================================
start "" http://localhost:5000
py -m http.server 5000
pause

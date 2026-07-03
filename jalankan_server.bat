@echo off
title SIM-MPP Local Server Runner
cls
python run.py
if %errorlevel% neq 0 (
    echo.
    echo Gagal menjalankan server. Pastikan Python sudah terinstal dan berada di path system.
    pause
)

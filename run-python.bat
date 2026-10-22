@echo off
setlocal
if defined STUDY_PYTHON (
    set "project_python=%STUDY_PYTHON%"
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set "project_python=%~dp0.venv\Scripts\python.exe"
) else (
    set "project_python=%USERPROFILE%\.venvs\study-py312\Scripts\python.exe"
)
if not exist "%project_python%" (
    echo Python environment was not found: "%project_python%"
    echo See readme.md for setup instructions.
    exit /b 1
)
if "%~1"=="" (
    echo Usage: run-python.bat script.py [arguments]
    exit /b 2
)
pushd "%~dp0"
"%project_python%" %*
set "run_result=%errorlevel%"
popd
exit /b %run_result%

@echo off

echo Removing __pycache__ directories...
for /d /r %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)

echo Removing .mypy_cache...
if exist .mypy_cache rd /s /q .mypy_cache

echo Removing .pytest_cache...
if exist .pytest_cache rd /s /q .pytest_cache

echo.
echo ============================
echo Clean complete!
echo ============================

@echo off

echo Running mypy...
mypy --strict calculus
if errorlevel 1 goto :fail

echo.
echo Running pyflakes...
pyflakes calculus
if errorlevel 1 goto :fail

echo.
echo Running pydocstyle...
pydocstyle calculus
if errorlevel 1 goto :fail

echo.
echo Running pytest...
pytest
if errorlevel 1 goto :fail

echo.
echo Checking trailing whitespaces...
git diff --cached --check
if errorlevel 1 goto :fail

echo.
echo Running pymarkdown...
pymarkdown scan -r . --respect-gitignore
if errorlevel 1 goto :fail

echo Running examples...
echo --- constants_approximation ---
python -m examples.constants_approximation
if errorlevel 1 goto :fail
echo.
echo --- power_series ---
python -m examples.power_series
if errorlevel 1 goto :fail
echo.
echo --- rademacher_sequence ---
python -m examples.rademacher_sequence
if errorlevel 1 goto :fail
echo.
echo --- integral_approximation ---
python -m examples.integral_approximation
if errorlevel 1 goto :fail
echo.

echo.
echo ============================
echo All checks passed!
echo ============================
exit /b 0

:fail
echo.
echo ============================
echo Checks failed.
echo ============================
exit /b 1

@echo off
REM ─────────────────────────────────────────────────────────────────────────────
REM build.bat — Build the Cookie Cutter Generator into a single .exe
REM Usage: double-click build.bat, or run from command prompt
REM ─────────────────────────────────────────────────────────────────────────────

setlocal
set APP_NAME=CookieCutterGenerator

echo ============================================
echo      Cookie Cutter Generator -- Build
echo ============================================
echo.

REM ── Check Python ─────────────────────────────────────────────────────────────
echo ^> Checking Python...
python --version 2>NUL
if errorlevel 1 (
    echo   X Python not found. Install from https://python.org
    pause & exit /b 1
)

REM ── Check dependencies ────────────────────────────────────────────────────────
echo.
echo ^> Checking dependencies...

python -c "import cadquery" 2>NUL
if errorlevel 1 ( echo   X cadquery missing. Run: conda install -c conda-forge cadquery & pause & exit /b 1 )

python -c "import cv2" 2>NUL
if errorlevel 1 ( echo   X opencv-python missing. Run: pip install opencv-python & pause & exit /b 1 )

python -c "import skimage" 2>NUL
if errorlevel 1 ( echo   X scikit-image missing. Run: pip install scikit-image & pause & exit /b 1 )

python -c "import scipy" 2>NUL
if errorlevel 1 ( echo   X scipy missing. Run: pip install scipy & pause & exit /b 1 )

python -c "import shapely" 2>NUL
if errorlevel 1 ( echo   X shapely missing. Run: pip install shapely & pause & exit /b 1 )

python -c "import PyInstaller" 2>NUL
if errorlevel 1 ( echo   X pyinstaller missing. Run: pip install pyinstaller & pause & exit /b 1 )

echo   All dependencies found

REM ── Clean previous build ──────────────────────────────────────────────────────
echo.
echo ^> Cleaning previous build...
if exist build   rmdir /s /q build
if exist dist    rmdir /s /q dist
if exist *.spec  del *.spec
echo   Clean

REM ── Run PyInstaller ───────────────────────────────────────────────────────────
echo.
echo ^> Building .exe (this takes 2-5 minutes)...
echo.

pyinstaller ^
  --onefile ^
  --windowed ^
  --name %APP_NAME% ^
  --collect-all cadquery ^
  --collect-all OCC ^
  --collect-all cadquery_occ ^
  --hidden-import skimage.morphology ^
  --hidden-import skimage.filters ^
  --hidden-import skimage.util ^
  --hidden-import scipy.interpolate ^
  --hidden-import scipy.spatial.distance ^
  --hidden-import shapely ^
  --hidden-import shapely.geometry ^
  --hidden-import shapely.ops ^
  main.py

REM ── Done ──────────────────────────────────────────────────────────────────────
echo.
if exist "dist\%APP_NAME%.exe" (
    echo ============================================
    echo           Build complete!
    echo ============================================
    echo.
    echo   Output:  dist\%APP_NAME%.exe
    echo.
    echo   NOTE: Windows Defender may flag the .exe
    echo   as suspicious -- this is a known false
    echo   positive with PyInstaller. Click "More info"
    echo   then "Run anyway" to proceed.
    echo.
) else (
    echo X Build failed -- check output above for errors
)

pause

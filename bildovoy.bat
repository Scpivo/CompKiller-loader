@echo off
chcp 65001 > nul
title CompKiller Loader Builder
color 0A

echo ============================================
echo    CompKiller Loader Build Script
echo ============================================
echo.

REM Проверяем Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не установлен!
    echo Установите Python с сайта python.org
    echo Убедитесь что добавили Python в PATH при установке
    pause
    exit /b 1
)

REM Проверяем pip
pip --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip не найден!
    echo Установите pip: python -m ensurepip
    pause
    exit /b 1
)

echo [1/5] Установка зависимостей...
echo.

pip install pymem pyinstaller > "install_log.txt" 2>&1
if errorlevel 1 (
    echo [ERROR] Не удалось установить зависимости!
    echo Проверьте файл install_log.txt для деталей
    pause
    exit /b 1
)

echo [OK] Зависимости установлены!
echo.

REM Проверяем нужные файлы
echo [2/5] Проверка файлов...
echo.

if not exist "injector.py" (
    echo [ERROR] Файл injector.py не найден!
    echo Положите этот .bat файл в папку с injector.py
    pause
    exit /b 1
)

if not exist "autizm.dll" (
    echo [WARNING] Файл autizm.dll не найден!
    echo Билд будет создан, но для работы нужен autizm.dll
    echo Положите autizm.dll в папку с EXE после сборки
    pause
)

echo [OK] Файлы проверены!
echo.

REM Создаем папки для сборки
echo [3/5] Подготовка к сборке...
echo.

if exist "build" (
    echo Удаляю старую папку build...
    rmdir /s /q build > nul 2>&1
)

if exist "dist" (
    echo Удаляю старую папку dist...
    rmdir /s /q dist > nul 2>&1
)

if exist "compkiller.spec" (
    echo Удаляю старый spec файл...
    del compkiller.spec > nul 2>&1
)

echo [OK] Папки очищены!
echo.

REM Сборка EXE
echo [4/5] Сборка EXE файла...
echo.

REM Если есть иконка - используем её
if exist "icon.ico" (
    echo Использую иконку icon.ico
    pyinstaller --onefile --windowed --icon=icon.ico --name="CompKiller_Loader" --add-data "autizm.dll;." injector.py > "build_log.txt" 2>&1
) else (
    echo Иконка не найдена, собираю без неё
    pyinstaller --onefile --windowed --name="CompKiller_Loader" --add-data "autizm.dll;." injector.py > "build_log.txt" 2>&1
)

if errorlevel 1 (
    echo [ERROR] Ошибка при сборке!
    echo Проверьте файл build_log.txt для деталей
    pause
    exit /b 1
)

echo [OK] Сборка завершена!
echo.

REM Проверяем результат
echo [5/5] Проверка результата...
echo.

if exist "dist\CompKiller_Loader.exe" (
    echo [SUCCESS] EXE файл успешно создан!
    echo.
    echo Путь: %cd%\dist\CompKiller_Loader.exe
    echo Размер: 
    for %%F in (dist\CompKiller_Loader.exe) do echo        %%~zF байт
    echo.
    echo Что нужно сделать дальше:
    echo 1. Положите autizm.dll в папку с EXE
    echo 2. Запустите CompKiller_Loader.exe от имени Администратора
    echo 3. Нажмите START INJECTION
    echo.
) else (
    echo [ERROR] EXE файл не создан!
    echo Проверьте build_log.txt для деталей
)

REM Создаем README файл
echo Создаю README файл...
(
echo CompKiller Loader - Инструкция
echo ==============================
echo.
echo 1. ТРЕБОВАНИЯ:
echo    - Windows 10/11
echo    - Запуск от имени Администратора
echo    - Выключенный антивирус
echo.
echo 2. УСТАНОВКА:
echo    Положите файлы в одну папку:
echo      CompKiller_Loader.exe
echo      autizm.dll
echo.
echo 3. ИСПОЛЬЗОВАНИЕ:
echo    1. Удалите -insecure из параметров запуска CS2
echo    2. Запустите CompKiller_Loader.exe от Администратора
echo    3. Нажмите START INJECTION
echo    4. Дождитесь сообщения об успехе
echo.
echo 4. ЕСЛИ НЕ РАБОТАЕТ:
echo    - Запустите от Администратора
echo    - Выключите антивирус
echo    - Удалите все параметры запуска CS2
echo    - Проверьте что autizm.dll в той же папке
echo.
echo Сборка создана: %date% %time%
) > "dist\README.txt"

echo.
echo ============================================
echo          СБОРКА ЗАВЕРШЕНА!
echo ============================================
echo.
echo Файлы для распространения:
echo   dist\CompKiller_Loader.exe  - Загрузчик
echo   dist\README.txt             - Инструкция
echo.
echo Нажмите любую клавишу для открытия папки...
pause > nul

REM Открываем папку с результатом
explorer "dist"

REM Опционально: удаляем временные файлы
echo.
set /p cleanup="Удалить временные файлы? (y/n): "
if /i "%cleanup%"=="y" (
    if exist "__pycache__" rmdir /s /q __pycache__
    if exist "install_log.txt" del install_log.txt
    if exist "build_log.txt" del build_log.txt
    echo Временные файлы удалены!
)
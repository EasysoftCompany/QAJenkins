@echo off
:: =============================================================================
:: setup_jenkins.bat
:: Construye la imagen personalizada de Jenkins y levanta el contenedor.
:: Uso: setup_jenkins.bat
:: =============================================================================

set IMAGE_NAME=jenkins-qa
set CONTAINER_NAME=jenkins-qa
set JENKINS_PORT=8080
set JENKINS_VOLUME=jenkins_qa_home

echo.
echo ========================================
echo   Jenkins QA Automation Setup
echo ========================================
echo.

:: -- 1. Detener y eliminar contenedor anterior si existe ----------------------
docker ps -aq -f name=%CONTAINER_NAME% > tmp.txt
set /p CONTAINER_ID=<tmp.txt
del tmp.txt

if not "%CONTAINER_ID%"=="" (
    echo Deteniendo contenedor anterior...
    docker stop %CONTAINER_NAME%
    docker rm %CONTAINER_NAME%
    echo Contenedor eliminado
)

:: -- 2. Construir la imagen personalizada -------------------------------------
echo.
echo Construyendo imagen Docker personalizada...
docker build -t %IMAGE_NAME% ./docker/

if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo al construir la imagen. Revisa el Dockerfile.
    exit /b 1
)
echo Imagen '%IMAGE_NAME%' construida correctamente

:: -- 3. Levantar el contenedor ------------------------------------------------
echo.
echo Levantando contenedor Jenkins...
docker run -d ^
    -p %JENKINS_PORT%:8080 ^
    -u root ^
    -v %JENKINS_VOLUME%:/var/jenkins_home ^
    -v //var/run/docker.sock:/var/run/docker.sock ^
    --name %CONTAINER_NAME% ^
    --restart unless-stopped ^
    %IMAGE_NAME%

if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo al levantar el contenedor.
    exit /b 1
)

:: -- 4. Esperar a que Jenkins arranque ----------------------------------------
echo.
echo Esperando que Jenkins inicie ^(esto puede tomar 1-2 minutos^)...
timeout /t 20 /nobreak > nul

:: -- 5. Mostrar info ----------------------------------------------------------
echo.
echo ========================================
echo   Jenkins listo!
echo ========================================
echo.
echo   URL: http://localhost:%JENKINS_PORT%
echo.
echo   Contrasena inicial de admin:
docker exec %CONTAINER_NAME% cat /var/jenkins_home/secrets/initialAdminPassword
echo.
echo   Versiones instaladas:
docker exec %CONTAINER_NAME% python3 --version
docker exec %CONTAINER_NAME% chromium --version
echo.

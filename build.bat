@echo off

REM BERT Sentiment Analysis App Build Script for Windows
REM This script builds the Docker image for the sentiment analysis application

echo 🚀 Building BERT Sentiment Analysis Docker Image...
echo ==============================================

REM Set image name and tag
set IMAGE_NAME=bert-sentiment-app
set IMAGE_TAG=latest
set FULL_IMAGE_NAME=%IMAGE_NAME%:%IMAGE_TAG%

REM Build the Docker image
echo 📦 Building Docker image: %FULL_IMAGE_NAME%
docker build -t %FULL_IMAGE_NAME% .

REM Check if build was successful
if %errorlevel%==0 (
    echo ✅ Docker image built successfully!
    echo 📝 Image details:
    docker images | findstr %IMAGE_NAME%
    
    echo.
    echo 🔧 Available commands:
    echo   Run container:           docker run -p 5000:5000 %FULL_IMAGE_NAME%
    echo   Run with Docker Compose: docker-compose up
    echo   Deploy to Kubernetes:    kubectl apply -f deployment.yaml
    echo   View logs:              docker logs ^<container_id^>
    echo.
    echo 🌐 Access the application at: http://localhost:5000
) else (
    echo ❌ Failed to build Docker image
    exit /b 1
)

pause

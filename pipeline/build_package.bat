@echo off
echo ==========================================
echo Building NLP Sentiment Pipeline Package
echo ==========================================
echo.

echo Step 1: Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist nlp_sentiment_pipeline.egg-info rmdir /s /q nlp_sentiment_pipeline.egg-info
echo Done!
echo.

echo Step 2: Building the package...
python -m build
echo.

echo ==========================================
echo Build process complete!
echo ==========================================
echo.

echo Check the dist\ folder for:
echo - nlp-sentiment-pipeline-0.1.0.tar.gz
echo - nlp_sentiment_pipeline-0.1.0-py3-none-any.whl
echo.

pause


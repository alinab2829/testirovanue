@echo off
echo ========================================
echo Running tests on Selenium Grid...
echo ========================================
echo Make sure Selenium Server is running in another window!
echo.

pytest tests/ --grid --browser=chrome --alluredir=allure-results -v

echo.
echo ========================================
echo Generating Allure report...
echo ========================================
allure serve allure-results

echo.
pause
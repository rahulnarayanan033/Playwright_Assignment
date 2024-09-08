# Playwright_Assignment

How to set up
1. Clone the repository
2. Install python from https://www.python.org/downloads/ if not installed
3. Install Pycharm if not installed
4. Install playwright for python and required browsers using below commands
   1. pip install pytest-playwright
   2. playwright install
5. Install allure for python for generating reports after execution using below command
   1. pip install allure-pytest
   2. Install allure pytest package from Pycharm by following below step
      1. Go To File
      2. Tap on Settings
      3. Expand project Name, for eg: Project:ProjectName
      4. Select Python Interpreter
      5. Click on + icon
      6. Search for allure pytest and tap on install package
   3. Inorder to generate report allure has to be installed in machine
      1. Open windows powershell
      2. Type command: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
      3. Then type command: irm get.scoop.sh | iex
      4. The install allure using command: scoop install allure
6. Install playwright jsonschema package for respons structure validation
   1. pip install playwright jsonschema
7. Type below commands in terminal for execution
   1. Navigate to tests folder: cd tests 
   2. Then type: pytest -v -s --alluredir=report test_user_login.py --headed
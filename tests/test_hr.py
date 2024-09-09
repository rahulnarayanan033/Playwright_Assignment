import pytest
import sys
sys.path.append("..")
from playwright.sync_api import Playwright, expect
from utils import methods
import  json
import allure

# will run the page below before and after all test cases
@pytest.fixture(scope="class")
def page(playwright: Playwright):
    browser = playwright.chromium.launch()
    yield browser
    # closes the browser
    browser.close()

def test_user_login(browser):
    # creates new browser context and page object
    context = browser.new_context()
    page = context.new_page()

    # reads the json file of web elements for login page
    data = methods.readJson("../data/webelements/loginPage.json")
    with allure.step('the user lands on login page'):
        # navigates to the application under test and logs a custom message to allure report
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        allure.attach("Landed on login page", attachment_type=allure.attachment_type.TEXT)

    with allure.step('the user enters username and password'):
        methods.type(page,data['txtUserName'],"Admin")
        methods.type(page,data['txtPassword'],"admin123")

    with allure.step('the user clicks on login button'):
        methods.click(page,data['btnLogin'])
        allure.attach("Login completed successfully", attachment_type=allure.attachment_type.TEXT)

    with allure.step('verify user is logged in'):
        # stores the state of the web page in auth.json file which will be created at run time.
        # This file will be used in other test cases to bypass login
        context.storage_state(path="auth.json")
        # verifies if provided element is visible or not
        methods.isElementVisible(page,data["profilePicture"])

    context.close()
    page.close()

def test_user_search(browser):
    # provides the file name in which state of the page is stored and passes it into another browser context to bypass login
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()
    data = methods.readJson("../data/webelements/usermanagement.json")
    loginElements = methods.readJson("../data/webelements/loginPage.json")

    with allure.step("Verify user is logged in"):
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        methods.isElementVisible(page,loginElements["profilePicture"])
        allure.attach("User is logged in",attachment_type=allure.attachment_type.TEXT)

    with allure.step('navigate to user management page'):
        methods.click(page,data["lblAdmin"])
        methods.isElementVisible(page,data["lblSystemUser"])
        allure.attach("user landed on user management page", attachment_type=allure.attachment_type.TEXT)

    with allure.step("user searches for username"):
        methods.type(page,data["txtUserName"],"FMLName")
        methods.click(page,data["btnSearch"])

    with allure.step('verify user is present'):
        methods.isElementVisible(page,data["lblUserName"])
        allure.attach("user is present", attachment_type=allure.attachment_type.TEXT)

    with allure.step('navigate to user details page'):
        methods.click(page,data["btnEdit"])
        methods.isElementVisible(page,data["lblEditUser"])
        allure.attach("landed on user details page", attachment_type=allure.attachment_type.TEXT)
    context.close()
    page.close()

def test_add_user(browser):
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()
    loginElements = methods.readJson("../data/webelements/loginPage.json")
    searchUser = methods.readJson("../data/webelements/usermanagement.json")
    data = methods.readJson("../data/webelements/addUser.json")
    with allure.step("Verify user is logged in"):
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        methods.isElementVisible(page, loginElements["profilePicture"])
        allure.attach("User is logged in", attachment_type=allure.attachment_type.TEXT)

    with allure.step('Tap on Add User button in user management page'):
        methods.click(page, searchUser["lblAdmin"])
        methods.click(page,data["btnAdd"])
        methods.isElementVisible(page,data['lblAddUser'])
        allure.attach('landed on add user page')

    with allure.step('Provide required details and add user'):
        methods.type(page,data["txtEmployeeName"],"sww test")
        methods.click(page,data["lblEmployeeName"])
        username = methods.generateRandomUserName()
        methods.type(page,data["txtUserName"],username)
        methods.click(page,data["cboUserRole"])
        methods.click(page,data["lblUserRole"])
        methods.click(page,data["cboStatus"])
        methods.click(page,data["lblStatus"])
        methods.type(page,data["txtPassword"],'Qwerty@123')
        methods.type(page,data["txtConfirmPassword"],'Qwerty@123')
        methods.click(page,data["btnSave"])
        methods.isElementVisible(page,data["lblSystemUser"])
        allure.attach("User is added as Admin")

    with allure.step('verify user is added'):
        methods.type(page, searchUser["txtUserName"], username)
        methods.click(page,searchUser["btnSearch"])
        expect(page.locator("//*[@id='app']/descendant::div[text()='"+username+"']")).to_be_visible(timeout=30000)
        allure.attach('User is added')
    context.close()
    page.close()

def test_request(browser):
    context = browser.new_context(storage_state="auth.json")
    with allure.step('send a GET request and veirify if its successfull'):
        # sends a GET request using playwright's GET method
        request = context.request
        response = request.get("https://opensource-demo.orangehrmlive.com/web/index.php/api/v2/admin/users?limit=50&offset=0&sortField=u.userName&sortOrder=ASC",headers={
        "Cookie": "orangehrm=3356521747e3679fe7e28f5240083e84"
        })
        # verifies whether the response is successfull
        expect(response).to_be_ok()
        allure.attach("request sent successfully")

    with allure.step('validate status code is 200'):
        # validates the status code is 200
        methods.validateStatusCode(str(response.status),"200")

    with allure.step('validate response structure'):
        response = response.json()
        schema = methods.readJson("../data/schema/apiSchema.json")
        # verifies the structure of the API response received
        methods.validateJsonSchema(response,schema)

    with allure.step("Launch the page and verify user is logged in"):
        page = context.new_page()
        loginElements = methods.readJson("../data/webelements/loginPage.json")
        data = methods.readJson("../data/webelements/addUser.json")
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        methods.isElementVisible(page, loginElements["profilePicture"])
        allure.attach("User is logged in", attachment_type=allure.attachment_type.TEXT)

    with allure.step('navigate to user management page'):
        methods.click(page,data["lblAdmin"])
        methods.isElementVisible(page,data["lblSystemUser"])

    with allure.step('fetch all the usernames from UI and API response'):
        # fetches the usernames from UI using below locator
        usernameUI = page.locator('(//*[@role="table"]/div/following-sibling::div/div/div/div[2])').all_text_contents()
        # fetches the usernames from API response using below locator
        usernameApi = [i['userName'] for i in response['data']]

    with allure.step('validate if correct usernames from API responses are displayed in UI'):
        for i in usernameApi:
            if i in usernameUI:
                allure.attach(i + ' is dispyed in UI')
            else:
                raise AssertionError(i + ' is not dispyed in UI')
    page.close()
    context.close()
import  json
from playwright.sync_api import Page, expect
import random
import allure
from jsonschema import validate,ValidationError

def readJson(fileName):
    # opens the file
    file = open(fileName)
    # reads the content of the file
    file = file.read()
    # converts the data into dictionary
    data = json.loads(file)
    return data

def type(page,locator,value):
    try:
        # types the data into text field
        page.locator(locator).fill(value)
        allure.attach("The value is enetered in the textfield with locator: " + locator,attachment_type=allure.attachment_type.TEXT)
    except:
        # raises the error if element is not found
        allure.attach("Element " + locator + " is not found")
        raise TimeoutError("Element " + locator + " is not found")
    finally:
        # takes the screenshot and attaches it to allure report irrespective of the result of the assertion
        page.screenshot(path="screenshot.png")
        allure.attach.file("screenshot.png",attachment_type=allure.attachment_type.PNG)

def click(page,locator):
    try:
        # clicks on the element
        page.locator(locator).click()
        allure.attach("The element with locator:" + locator + " is clicked",attachment_type=allure.attachment_type.TEXT)
    except:
        # raises the error if element is not found
        allure.attach("Element " + locator + " is not found")
        raise TimeoutError("Element " + locator + " is not found")
    finally:
        # takes the screenshot and attaches it to allure report irrespective of the result of the assertion
        page.screenshot(path="screenshot.png")
        allure.attach.file("screenshot.png",attachment_type=allure.attachment_type.PNG)

def generateRandomUserName():
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','q','r','s','t','u','v','w','x','y','z']
    nums = ['1','2','3','4','5','6','7','8','9','0']
    username = ''
    # fetched random characters from char list and random numbers from nums list and generates random username
    for i in range(4):
        username = username + random.choice(chars)
    for i in range(2):
        username = username + random.choice(nums)
    return username

def isElementVisible(page,locator):
    try:
        # verifies if element is visible or not. It will wait for 30 seconds before throwing error
        expect(page.locator(locator)).to_be_visible(timeout=30000)
        allure.attach("Element with locator: " + locator + " is visible")
    except:
        # raise error if element is not visible
        allure.attach("Element with locator: " + locator + " is not visible")
        raise AssertionError("Element with locator: " + locator + " is not visible")
    finally:
        page.screenshot(path="screenshot.png")
        allure.attach.file("screenshot.png",attachment_type=allure.attachment_type.PNG)

def validateStatusCode(actualStatus, expectedStatus):
    # checks if status code from actual response and expected response are same
    if actualStatus == expectedStatus:
        allure.attach("Expected and actual status code is " + str(expectedStatus))
    else:
        # if status code is not correct throws an error
        allure.attach('Expected status code is ' + str(expectedStatus) + ' but actual status code is ' + actualStatus,)
        raise AssertionError('Expected status code is ' + str(expectedStatus) + ' but actual status code is ' + actualStatus)

def validateJsonSchema(actualResponse, jsonSchema):
    try:
        # validates the structure of response against the schema template
        validate(instance=actualResponse,schema=jsonSchema)
        allure.attach('the structure of response is valid')
    except ValidationError as error:
        # throws error if the structure of actual response doesn't match with schema template
        raise AssertionError("The structure of response is not valid due to: ",error.message)

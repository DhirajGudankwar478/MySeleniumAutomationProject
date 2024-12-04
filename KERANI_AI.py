import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Set up the WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)


# Helper function to log in
def login():
    driver.get("https://app.karini.ai/signin")
    driver.maximize_window()

    input_field_1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Email']"))
    )
    input_field_1.send_keys("dhirajgudankwar1998@gmail.com")
    input_field_2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@aria-label="Password"]'))
    )
    input_field_2.send_keys("Dhiraj@123")
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[2]/div/div/div[1]/div/button").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Dashboards']")))

def navigate_to_model_hub():
    # Navigate to the Model Hub.com
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sidebar"]/div/div[2]/div[1]/a[2]')))
    link = driver.find_element(By.XPATH, '//*[@id="sidebar"]/div/div[2]/div[1]/a[2]')
    href_value = link.get_attribute("href")
    driver.get(href_value)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Large language model endpoints (LLM)']")))
    element = driver.find_element(By.XPATH, "//div[text()='Large language model endpoints (LLM)']")
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()


def create_and_test_model_1(model_nm, model_provider, model_id):
    # Click "ADD" button to create a new model
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Add new']")))
    element = driver.find_element(By.XPATH, "//button[@aria-label='Add new']")
    element.click()

    # Enter model name
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Model name']")))
    input_element_1 = driver.find_element(By.XPATH, "//input[@aria-label='Model name']")
    input_element_1.send_keys(model_nm)

    # Select "OpenAI" as the model provider
    span_element_1 = driver.find_element(By.XPATH, "//span[text()='Amazon Bedrock']")
    actions = ActionChains(driver)
    actions.move_to_element(span_element_1).click().perform()
    span_element_2 = driver.find_element(By.XPATH, "//span[text()='" + model_provider + "']")
    span_element_2.click()

    # Choose the model ID
    span_element_1 = driver.find_element(By.XPATH, "//span[text()='o1 preview']")
    actions = ActionChains(driver)
    actions.move_to_element(span_element_1).click().perform()
    span_element_2 = driver.find_element(By.XPATH, "//span[text()='" + model_id + "']")
    span_element_2.click()

    # Save the model
    save_btn = driver.find_element(By.XPATH, "//*[text()='Save']")
    actions = ActionChains(driver)
    actions.move_to_element(save_btn).click().perform()

    # Open the newly created model
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='View model']")))
    view_button = (driver.find_element(By.XPATH, "//*[text()='View model']"))
    view_button.click()

    # Test the model using "Test Endpoint"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Test endpoint']")))
    driver.find_element(By.XPATH, "//*[text()='Test endpoint']").click()

    # Input "Hello" in the request field
    textarea = driver.find_element(By.CSS_SELECTOR, 'textarea[data-slot="input"]')
    # Submit the request
    textarea.send_keys('hello')

    # Wait for the response field
    driver.find_element(By.XPATH, "//button[text()='Send request']").click()

    # Get the response from the response field
    response = driver.find_element(By.CSS_SELECTOR, 'textarea[readonly]')
    time.sleep(2)
    response_1 = driver.execute_script("return arguments[0].value;", response)
    print(response_1)

    #Close Testpoint
    svg_element = driver.find_element(By.CSS_SELECTOR,
                                      'svg[aria-hidden="true"][role="presentation"][stroke="currentColor"][viewBox="0 0 24 24"]')
    actions = ActionChains(driver)
    actions.move_to_element(svg_element).click().perform()
    driver.find_element(By.XPATH, "//button[text()='Delete']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Ok']")))
    driver.find_element(By.XPATH, "//button[text()='Ok']").click()
    return response_1


try:
    login()
    navigate_to_model_hub()
    response_1 = create_and_test_model_1("Model_1", "OpenAI", "GPT 4O Mini")
    response_2 = create_and_test_model_1("Model_2", "OpenAI", "GPT 4O")
    print("Model_1:" + response_1)
    print("Model_2:" + response_2)

    save_path = r'C:\Users\Lenovo\OneDrive\Desktop\KERANI_AI\model_responses.csv'

    with open(save_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Model Name", "Response"])  # Writing header
        writer.writerow(["Model_1", response_1])  # Writing model 1's data
        writer.writerow(["Model_2", response_2])  # Writing model 2's data

    print("Model responses saved to model_responses.csv")

finally:
    print("Quitting Dashboard")

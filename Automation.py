from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
import random
import string
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime


# Function to save user data
def save_user_data(data, file_name="user_data.json"):
    # Check if the file already exists
    if os.path.exists(file_name):
        # Read the existing data
        with open(file_name, "r") as file:
            all_data = json.load(file)
    else:
        # Start with an empty list if the file doesn't exist
        all_data = []
    
    # Append the new data
    all_data.append(data)
    
    # Write the updated data back to the file
    with open(file_name, "w") as file:
        json.dump(all_data, file, indent=4)


# Function to generate a semi-complex username
def generate_username(base="TestUser"):
    # Appends a random 4-digit number to the base username
    return f"{base}{random.randint(1000, 9999)}"


# Function to generate a strong password
def generate_password(length=12):
    # Includes uppercase, lowercase, numbers, and special characters
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))


# Start the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Step 1: Open the temp mail website
driver.get("https://tempmail.so/")

# Wait for the email address to appear
email_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[@id='inbox-name']"))
)

# Retrieve the email address
email_address = email_field.text
print(f"Generated Email: {email_address}")

# Simulate a click on the email field
driver.execute_script("arguments[0].click();", email_field)


################################################
# Step 2: Go to Discord registration page
driver.execute_script("window.open('https://discord.com/register', '_blank');")
driver.switch_to.window(driver.window_handles[1])

# Fill in the email field
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email_address)

# Generate a display name and fill it
display_name = generate_username("DisplayName")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "global_name"))).send_keys(display_name)

# Retry mechanism for unavailable usernames
username = display_name
username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

while True:
    # Clear the username field and input a new username
    username_field.clear()
    username_field.send_keys(username)

    # Check if the error message is displayed
    time.sleep(1)  # Allow some time for the error to load
    try:
        error_message = driver.find_element(By.XPATH, "//div[contains(text(), 'Username is unavailable')]")
        print(f"Username '{username}' is unavailable. Retrying...")
        username = generate_username()  # Generate a new username
    except:
        # If no error message is found, the username is available
        break

# Generate and fill a strong password
password = generate_password()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)

# Calculate the current year
current_year = datetime.now().year

# Ensure the year makes the user at least 18 years old
valid_year = current_year - 18

# Update the birth_date dictionary dynamically
birth_date = {
    "month": "March",  # Change this if needed
    "day": "3",        # Change this if needed
    "year": str(valid_year)
}

# Function to click and select dropdown values by targeting the <span> element
def select_by_span_text(field_name, value):
    # Mapping for dropdown field names to their <span> text
    field_map = {
        "month": "Month",
        "day": "Day",
        "year": "Year"
    }
    
    # Click the dropdown using the <span> text
    dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//span[text()='{field_map[field_name]}']"))
    )
    dropdown.click()
    
    # Select the value from the dropdown
    option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[text()='{value}']"))
    )
    option.click()

# Select Month, Day, and Year
select_by_span_text("month", birth_date["month"])
select_by_span_text("day", birth_date["day"])
select_by_span_text("year", birth_date["year"])


# Save the user data
user_data = {
    "email": email_address,
    "username": username,
    "display_name": display_name,
    "date_of_birth": f"{birth_date['year']}-{birth_date['month']}-{birth_date['day']}",
    "password": password
}
# Click the "Continue" button (div element)
continue_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[text()='Continue' and contains(@class, 'contents_dd4f85')]"))
)
continue_button.click()
save_user_data(user_data)

# Keep the browser open for further manual actions
print("Browser will remain open. Press Ctrl+C to terminate manually if needed.")
try:
    while True:
        time.sleep(1)  # Keeps the script running without doing anything
except KeyboardInterrupt:
    print("Exiting script. Browser will remain open.")

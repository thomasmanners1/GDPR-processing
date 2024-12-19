import time
import json
import re
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Streamlit UI
st.title("Email Extraction Tool")

# Input credentials
email = st.text_input("Enter your email:", type="default")
password = st.text_input("Enter your password:", type="password")
run_process = st.button("Run Email Extraction")

# Regex pattern to extract emails
email_extraction_regex = re.compile(r'DELETE-(.*?)-\d{2}-\d{2}-\d{4}')
email_list = {"emails": []}  # Store extracted emails

# Process emails function
def process_emails(driver):
    def get_table_rows():
        return driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/section/div[1]/div[2]/div/div[2]/div[2]/table/tbody/tr')

    rows = get_table_rows()
    for i, row in enumerate(rows):
        try:
            email_div = row.find_element(By.XPATH, f'./td[4]/div/div')
            email_title = email_div.get_attribute('title')

            if "DELETE-" in email_title:
                match = email_extraction_regex.search(email_title)
                if match:
                    email = match.group(1)
                    size_field = row.find_element(By.XPATH, './td[5]/span').text
                    if size_field != '0 B':
                        email_list["emails"].append(email)
        except Exception as e:
            st.warning(f"Error processing row {i}: {str(e)}")

# Main processing
if run_process and email and password:
    try:
        # Set up Selenium Edge WebDriver
        driver = webdriver.Edge(executable_path=r'C:\Users\thoma\Downloads\edgedriver_win64 (3)\msedgedriver.exe')

        # Load website
        driver.get('https://g-star.sharefile.eu/home/shared/fo6089f6-96d2-48bf-b790-90f1995aadca')
        time.sleep(7)

        # Log in with credentials
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div/div/main/div/form/div[1]/div/div[2]/div/div/span/input'))
        )
        email_field.send_keys(email)
        email_field.send_keys(Keys.ENTER)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div/div/main/div/form/div[2]/div/div[2]/div/div/span/input'))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)

        time.sleep(20)  # Wait for the page to load
        st.info("Logged in successfully. Processing emails...")

        # Process emails
        process_emails(driver)

        # Show extracted emails
        if email_list["emails"]:
            st.success("Emails extracted successfully:")
            st.json(email_list)
        else:
            st.warning("No emails found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()
            st.write("Driver closed successfully!")

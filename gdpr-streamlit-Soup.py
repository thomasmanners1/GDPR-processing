import time
import json
import re
import requests
from bs4 import BeautifulSoup

# Streamlit UI
import streamlit as st
st.title("Email Extraction Tool")

# Input credentials
email = st.text_input("Enter your email:", type="default")
password = st.text_input("Enter your password:", type="password")
run_process = st.button("Run Email Extraction")

# Regex pattern to extract emails
email_extraction_regex = re.compile(r'DELETE-(.*?)-\d{2}-\d{2}-\d{4}')
email_list = {"emails": []}  # Store extracted emails

# Process emails function
def process_emails(soup):
    rows = soup.find_all('tr')  # Extract rows from the table
    for i, row in enumerate(rows):
        try:
            email_div = row.find('div', {'class': 'email-class'})  # Example class for emails
            email_title = email_div.get('title')  # Get email title attribute

            if "DELETE-" in email_title:
                match = email_extraction_regex.search(email_title)
                if match:
                    email = match.group(1)
                    size_field = row.find('span', {'class': 'size-class'}).text  # Example class for file size
                    if size_field != '0 B':
                        email_list["emails"].append(email)
        except Exception as e:
            st.warning(f"Error processing row {i}: {str(e)}")

# Main processing
if run_process and email and password:
    try:
        # Create a session to manage cookies and login
        session = requests.Session()

        # Log in with credentials (simulate login)
        login_url = "https://g-star.sharefile.eu/home/shared/fo6089f6-96d2-48bf-b790-90f1995aadca"
        login_data = {'email': email, 'password': password}

        # Post the login data
        login_response = session.post(login_url, data=login_data)

        if login_response.status_code == 200:
            st.info("Logged in successfully. Processing emails...")

            # Fetch the page content after login
            page_content = session.get(login_url)
            soup = BeautifulSoup(page_content.content, 'html.parser')

            # Process emails from the page
            process_emails(soup)

            # Show extracted emails
            if email_list["emails"]:
                st.success("Emails extracted successfully:")
                st.json(email_list)
            else:
                st.warning("No emails found.")
        else:
            st.error("Login failed. Please check your credentials.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

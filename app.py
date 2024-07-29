from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import os
from flask import Flask, jsonify

# Configure WebDriver options if needed
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode if you don't need a visible browser

# Initialize WebDriver
def getCFData(username):
    driver = webdriver.Chrome(options=chrome_options)  # Make sure chromedriver is in your PATH
    driver.get(f"https://codeforces.com/profile/{username}")
    data = driver.page_source

    with open ("data.txt", "w", encoding="utf-8") as f:
        f.write(data)

    data1 = None
    with open("data.txt", "r", encoding="utf-8") as f:
        data1 = f.read()

    time.sleep(2)

    cf_data = {}

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(data1, 'html.parser')

    # Extract relevant data
    username_element = soup.find('a', class_="rated-user user-gray")
    username = username_element.text if username_element else "N/A"

    rating_element = soup.find_all('span', class_='user-gray')
    rating = rating_element[1].text if len(rating_element) > 1 else "N/A"

    problem_element = soup.find('div', class_="_UserActivityFrame_counterValue")
    problems = problem_element.text if problem_element else "N/A"

    days = soup.find_all('div', class_="_UserActivityFrame_counterValue")
    solved_for_all_time = days[0].text if len(days) > 0 else "N/A"
    solved_for_the_last_year = days[1].text if len(days) > 1 else "N/A"
    solved_for_the_last_month = days[2].text if len(days) > 2 else "N/A"
    rows_in_max = days[3].text if len(days) > 3 else "N/A"
    in_a_row_for_last_year = days[4].text if len(days) > 4 else "N/A"
    in_a_row_for_last_month = days[5].text if len(days) > 5 else "N/A"

    # Populate the dictionary with the extracted data
    cf_data['username'] = username
    cf_data['rating'] = rating
    cf_data['solved_for_all_time'] = solved_for_all_time
    cf_data['solved_for_the_last_year'] = solved_for_the_last_year
    cf_data['solved_for_the_last_month'] = solved_for_the_last_month
    cf_data['rows_in_max'] = rows_in_max
    cf_data['in_a_row_for_last_year'] = in_a_row_for_last_year
    cf_data['in_a_row_for_last_month'] = in_a_row_for_last_month

    # Convert the dictionary to a JSON string
    return cf_data
    driver.quit()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to Codeforces API</h1><p>use /api/codeforces/your username</p>"

@app.route('/api/codeforces/<username>', methods=['GET'])
def get(username):
    cf_data = getCFData(username)
    cf_data['username'] = username
    return jsonify(cf_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Ensure you use the PORT variable
    app.run(host="0.0.0.0", port=port)

# Close the WebDriver

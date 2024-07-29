from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, jsonify

# Configure WebDriver options if needed
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode if you don't need a visible browser

# Initialize WebDriver
def getCFData(username):
    driver = webdriver.Chrome(options=chrome_options)  # Make sure chromedriver is in your PATH
    driver.get(f"https://codeforces.com/profile/{username}")
    data = driver.page_source

    with open ("codeforces.txt", "w", encoding="utf-8") as f:
        f.write(data)

    data1 = None
    with open("codeforces.txt", "r", encoding="utf-8") as f:
        datacf = f.read()

    cf_data = {}

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(datacf, 'html.parser')

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
def getLCData(username):
    LCData = {}
    driver = webdriver.Chrome()  # Make sure chromedriver is in your PATH
    driver.get(f"https://leetcode.com/{username}")
    time.sleep(3)
    data = driver.page_source
    with open ("leetcode.txt", "w", encoding="utf-8") as f:
        f.write(data)
    soup = BeautifulSoup(data, 'html.parser')
    problems = soup.find_all('span', class_="text-[30px] font-semibold leading-[32px]")[0].text
    try:
        rating = soup.find_all('div', class_="text-label-1 dark:text-dark-label-1 flex items-center text-2xl")[0].text
    except:
        rating = "N/A"
    total_active_days = soup.find_all('span', class_="font-medium text-label-2 dark:text-dark-label-2")[0].text
    max_streak = soup.find_all('span', class_="font-medium text-label-2 dark:text-dark-label-2")[1].text
    images = soup.find_all('img')
    images = images[2:-1]
    badges = []
    for img in images:
        badges.append(img['alt'])
    types = soup.find_all('div', class_="text-sd-foreground text-xs font-medium");
    easy = types[0].text
    medium = types[1].text
    hard = types[2].text
    rank = soup.find('span', class_="ttext-label-1 dark:text-dark-label-1 font-medium").text
    rank = rank.replace(",", "")
    # print(problems, rating, total_active_days, max_streak)
    # print(badges)
    # print(easy, medium, hard, rank)
    LCData['username'] = username
    LCData['problems'] = problems
    LCData['rating'] = rating
    LCData['total_active_days'] = total_active_days
    LCData['max_streak'] = max_streak
    LCData['badges'] = badges
    LCData['easy'] = easy
    LCData['medium'] = medium
    LCData['hard'] = hard
    LCData['rank'] = rank
    return LCData
    driver.quit()

    

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to Code API</h1><h3>use /api/codeforces/&lt;username&gt; for Codeforces</h3><h3>use /api/leetcode/&lt;username&gt; for Leetcode</h3>"

@app.route('/api/codeforces/<username>', methods=['GET'])
def getCF(username):
    cf_data = getCFData(username)
    cf_data['username'] = username
    return jsonify(cf_data)

@app.route('/api/leetcode/<username>', methods=['GET'])
def getLC(username):
    LCData = getLCData(username)
    LCData['username'] = username
    return jsonify(LCData)

if __name__ == "__main__":
    app.run(debug=True)


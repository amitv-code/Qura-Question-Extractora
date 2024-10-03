from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')


search_query = input("Enter Your Search Key: ")

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open Google
driver.get('https://www.google.com')

# Locate the search box
search_box = driver.find_element(By.NAME, 'q')

# Enter the search query "surgical instruments quora.com" and hit ENTER

search_box.send_keys("site:quora.com " + search_query)  # Added a space after "site:quora.com "
search_box.send_keys(Keys.RETURN)

# Create or open the CSV file for writing
with open('search_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Current URL', 'Inner Text'])

    # Function to process search results on the current page
    def process_results():
        # Wait for the results to load
        time.sleep(3)

        # Find all elements with the class "LC20lb" (these are the result titles)
        results = driver.find_elements(By.CLASS_NAME, 'LC20lb')

        # Iterate through each search result and click on them one by one
        for index, result in enumerate(results):
            try:
                # Print the title of the result before clicking (for debugging)
                print(f"Clicking on result {index + 1}: {result.text}")

                # Click the result
                result.click()

                # Wait for the page to load after the click
                time.sleep(3)

                # Print the current URL after clicking
                current_url = driver.current_url
                print(f"Current URL after click {index + 1}: {current_url}")

                # Use BeautifulSoup to extract the required span element from the page source
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                element = soup.find('span', class_='q-box qu-userSelect--text')

                inner_text = element.get_text(strip=True) if element else "Element not found"
                print(f"Inner Text: {inner_text}")

                # Write the extracted data to the CSV file
                writer.writerow([current_url, inner_text])

                # Print the index with "done" message
                print(f"{index + 1} done")

                # Go back to the search results page
                driver.back()

                # Wait for the search results page to reload
                time.sleep(3)

                # Re-find all results after going back, as the previous ones are stale
                results = driver.find_elements(By.CLASS_NAME, 'LC20lb')

            except Exception as e:
                print(f"Error at index {index}: {e}")
                break

    # Loop through multiple result pages
    while True:
        process_results()

        try:
            # Click on the "Next" button with id 'pnnext' to go to the next page
            next_button = driver.find_element(By.ID, 'pnnext')
            next_button.click()

            # Wait for the next page to load
            time.sleep(3)

        except Exception as e:
            print(f"No more pages or error navigating: {e}")
            break

# Close the browser when done
driver.quit()

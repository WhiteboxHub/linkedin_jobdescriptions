# import json
# import time
# import os
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# # Define your credentials here
# EMAIL = 'srikanth9948sri@gmail.com'
# PASSWORD = 'Rajan@91'

# # Initialize the global index
# global_index = 1

# def load_search_data():
#     try:
#         with open('fixtures/test-data.json', 'r') as f:
#             content = f.read().strip()
#             if not content:
#                 print("Error: File is empty.")
#                 return []
#             return json.loads(content)
#     except FileNotFoundError:
#         print("Error: 'test-data.json' file not found.")
#         return []
#     except json.JSONDecodeError as e:
#         print("JSON Decode Error:", e)
#         return []
#     except Exception as e:
#         print("Unexpected error:", e)
#         return []

# def save_job_details(title, company, location, description, index, folder_name='job_details'):
#     try:
#         # Create the folder if it doesn't exist
#         if not os.path.exists(folder_name):
#             os.makedirs(folder_name)
        
#         # Define the file name for each job description
#         file_name = f"job_details_{index}.txt"
#         file_path = os.path.join(folder_name, file_name)
        
#         # Save the details to the individual file
#         with open(file_path, 'w') as f:
#             f.write(f"Job Title: {title}\n")
#             f.write(f"Company Name: {company}\n")
#             f.write(f"Location: {location}\n")
#             f.write(f"Description:\n{description}\n")
        
#         print(f"Job details {index} saved to {os.path.abspath(file_path)}")
#     except Exception as e:
#         print(f"Failed to save job details {index}: {e}")

# def get_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     return driver

# def login(driver):
#     try:
#         driver.get('https://www.linkedin.com/login')
#         print("Navigated to login page.")
#         time.sleep(5)

#         email_input = driver.find_element(By.ID, 'username')
#         password_input = driver.find_element(By.ID, 'password')

#         email_input.send_keys(EMAIL)
#         password_input.send_keys(PASSWORD + Keys.ENTER)
#         time.sleep(10)
#         print("Logged in successfully.")
#     except Exception as e:
#         print("Login failed:", e)
#         driver.quit()
#         exit()

# def capture_and_write_job_ids(driver, seen_jobs):
#     global global_index
#     jobs = driver.find_elements(By.CSS_SELECTOR, '.job-card-container__link.job-card-list__title')
#     print(f"Found {len(jobs)} job postings on this page.")
    
#     for job in jobs:
#         job_url = job.get_attribute("href")
#         if job_url not in seen_jobs:
#             seen_jobs.add(job_url)
#             try:
#                 job.click()
#                 time.sleep(5)
                
#                 # Fetch job title
#                 title_element = driver.find_element(By.CLASS_NAME, 't-24.t-bold.inline')
#                 job_title = title_element.text if title_element else "N/A"
                
#                 # Fetch company name
#                 company_name = "N/A"
#                 try:
#                     company_element = driver.find_element(By.CSS_SELECTOR, '.job-details-jobs-unified-top-card__company-name a')
#                     company_name = company_element.text
#                 except Exception as e:
#                     print(f"Error fetching company name: {e}")

#                 # Fetch job location
#                 job_location = "N/A"
#                 try:
#                     location_element = driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__primary-description-container')
#                     job_location = location_element.text
#                 except Exception as e:
#                     print(f"Error fetching job location: {e}")
                
#                 # Fetch job description
#                 description_elements = driver.find_elements(By.CSS_SELECTOR, 
#                     '.jobs-box__html-content.jobs-description-content__text.t-14.t-normal, '
#                     '.jobs-description-content__text--stretch')
                
#                 if description_elements:
#                     for description_element in description_elements:
#                         job_description = description_element.text
#                         if job_description:
#                             save_job_details(job_title, company_name, job_location, job_description, global_index)
#                             print(f"Extracted job details {global_index}: {job_title} at {company_name} in {job_location}...")
#                             global_index += 1
#             except Exception as e:
#                 print(f"Error extracting job details: {e}")


# def go_to_next_page(driver, keyword):
#     seen_jobs = set()
#     try:
#         while True:
#             # Scroll to the bottom of the job search results list
#             jobs_list = driver.find_element(By.CSS_SELECTOR, '.jobs-search-results-list')
#             driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", jobs_list)
#             time.sleep(5)  # Wait for 5 seconds for the new content to load
#             print("Scrolled to the bottom of the page and waited for new content to load.")

#             # Capture and write job IDs
#             capture_and_write_job_ids(driver, seen_jobs)
#             print(f"Captured and wrote job IDs. Current global index: {global_index}")

#             # Find pagination buttons
#             buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Page"], .artdeco-pagination__indicator--number')
#             print(f"Found {len(buttons)} pagination buttons.")

#             if not buttons:
#                 print("No pagination buttons found.")
#                 break

#             current_page_button = next(
#                 (button for button in buttons if button.get_attribute('aria-current') == 'true'),
#                 None
#             )

#             if current_page_button:
#                 current_page_number = int(current_page_button.get_attribute('aria-label').split(' ')[1])
#                 next_page_number = current_page_number + 1
#                 print(f"Current page number: {current_page_number}, looking for next page number: {next_page_number}")

#                 next_page_button = next(
#                     (button for button in buttons if button.find_element(By.TAG_NAME, 'span').text == str(next_page_number)),
#                     None
#                 )

#                 if not next_page_button:
#                     # If the next page button is not found, click the ellipsis (dots) button to reveal more pages
#                     ellipsis_button = next(
#                         (button for button in buttons if '...' in button.find_element(By.TAG_NAME, 'span').text),
#                         None
#                     )
#                     if ellipsis_button:
#                         print("Ellipsis button found. Clicking it to reveal more page buttons.")
#                         ellipsis_button.click()
#                         time.sleep(2)  # Wait for the new page buttons to load
#                         buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Page"], .artdeco-pagination__indicator--number')
#                         next_page_button = next(
#                             (button for button in buttons if button.find_element(By.TAG_NAME, 'span').text == str(next_page_number)),
#                             None
#                         )

#                 if next_page_button:
#                     print(f"Next page button found: {next_page_number}. Clicking it.")
#                     next_page_button.click()

#                     # Wait for the aria-label of the current page button to update
#                     WebDriverWait(driver, 10).until(
#                         EC.text_to_be_present_in_element(
#                             (By.CSS_SELECTOR, 'button[aria-current="true"] span'),
#                             str(next_page_number)
#                         )
#                     )

#                     time.sleep(5)  # Wait for new content to load
#                     print("Page changed. Waiting for new content to load.")
#                 else:
#                     print(f"No button found for next page number: {next_page_number}")
#                     break
#             else:
#                 print("Current page button not found.")
#                 break
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         driver.save_screenshot('error_screenshot.png')
#         print("Screenshot saved as 'error_screenshot.png' for debugging.")

# def search_jobs(driver, keyword):
#     try:
#         driver.get('https://www.linkedin.com/jobs')
#         print(f"Searching for jobs: Keyword: {keyword}")
#         time.sleep(5)

#         search_box = driver.find_element(By.CSS_SELECTOR, '.jobs-search-box__text-input')
#         search_box.click()
#         search_box.clear()
#         search_box.send_keys(keyword + Keys.ENTER)
#         time.sleep(6)

#         go_to_next_page(driver, keyword)
#         print(f"Saved job descriptions for keyword '{keyword}'.")
#     except Exception as e:
#         print("Error during job search:", e)

# def main():
#     search_data = load_search_data()
#     if not search_data:
#         print("No search data to process.")
#         return

#     print("Starting driver.")   
#     driver = get_driver()
#     login(driver)

#     for data in search_data:
#         keyword = data['keyword']
#         search_jobs(driver, keyword)

#     driver.quit()
#     print("Driver quit successfully.")

# if __name__ == '__main__':
#     main()




import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException


# Define your credentials here
EMAIL = 'srikanth9948sri@gmail.com'
PASSWORD = 'Rajan@91'

# Initialize the global index
global_index = 1

def load_search_data():
    try:
        with open('fixtures/test-data.json', 'r') as f:
            content = f.read().strip()
            if not content:
                print("Error: File is empty.")
                return []
            return json.loads(content)
    except FileNotFoundError:
        print("Error: 'test-data.json' file not found.")
        return []
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return []
    except Exception as e:
        print("Unexpected error:", e)
        return []

def save_job_details(title, company, location, description, index, folder_name='job_details'):
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        # Define the file name for each job description
        file_name = f"job_details_{index}.txt"
        file_path = os.path.join(folder_name, file_name)
        
        # Save the details to the individual file
        with open(file_path, 'w') as f:
            f.write(f"Job Title: {title}\n")
            f.write(f"Company Name: {company}\n")
            f.write(f"Location: {location}\n")
            f.write(f"Description:\n{description}\n")
        
        print(f"Job details {index} saved to {os.path.abspath(file_path)}")
    except Exception as e:
        print(f"Failed to save job details {index}: {e}")

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login(driver):
    try:
        driver.get('https://www.linkedin.com/login')
        print("Navigated to login page.")
        time.sleep(5)

        email_input = driver.find_element(By.ID, 'username')
        password_input = driver.find_element(By.ID, 'password')

        email_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD + Keys.ENTER)
        time.sleep(10)
        print("Logged in successfully.")
    except Exception as e:
        print("Login failed:", e)
        driver.quit()
        exit()

from selenium.common.exceptions import StaleElementReferenceException

def capture_and_write_job_ids(driver, seen_jobs):
    global global_index
    jobs = driver.find_elements(By.CSS_SELECTOR, '.job-card-container__link.job-card-list__title')
    print(f"Found {len(jobs)} job postings on this page.")
    
    for job in jobs:
        job_url = job.get_attribute("href")
        if job_url not in seen_jobs:
            seen_jobs.add(job_url)
            attempt = 0
            max_attempts = 3  # Number of retries
            while attempt < max_attempts:
                try:
                    job.click()
                    time.sleep(5)
                    
                    # Fetch job title
                    title_element = driver.find_element(By.CLASS_NAME, 't-24.t-bold.inline')
                    job_title = title_element.text if title_element else "N/A"
                    
                    # Fetch company name
                    company_name = "N/A"
                    try:
                        company_element = driver.find_element(By.CSS_SELECTOR, '.job-details-jobs-unified-top-card__company-name a')
                        company_name = company_element.text
                    except Exception as e:
                        print(f"Error fetching company name: {e}")

                    # Fetch job location
                    job_location = "N/A"
                    try:
                        location_element = driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__primary-description-container')
                        job_location = location_element.text
                    except Exception as e:
                        print(f"Error fetching job location: {e}")
                    
                    # Fetch job description
                    description_elements = driver.find_elements(By.CSS_SELECTOR, 
                        '.jobs-box__html-content.jobs-description-content__text.t-14.t-normal, '
                        '.jobs-description-content__text--stretch')
                    
                    if description_elements:
                        for description_element in description_elements:
                            job_description = description_element.text
                            if job_description:
                                save_job_details(job_title, company_name, job_location, job_description, global_index)
                                print(f"Extracted job details {global_index}: {job_title} at {company_name} in {job_location}...")
                                global_index += 1
                    break  # Exit the retry loop after successful extraction
                except StaleElementReferenceException:
                    attempt += 1
                    print(f"StaleElementReferenceException encountered, retrying {attempt}/{max_attempts}...")
                    if attempt == max_attempts:
                        print("Max retry attempts reached, moving to the next job.")
                except Exception as e:
                    print(f"Error extracting job details: {e}")
                    break  # Skip to the next job after an unknown error





def go_to_next_page(driver, keyword):
    seen_jobs = set()
    try:
        while True:
            # Scroll to the bottom of the job search results list
            jobs_list = driver.find_element(By.CSS_SELECTOR, '.jobs-search-results-list')
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", jobs_list)
            time.sleep(5)  # Wait for 5 seconds for the new content to load
            print("Scrolled to the bottom of the page and waited for new content to load.")

            # Capture and write job IDs
            capture_and_write_job_ids(driver, seen_jobs)
            print(f"Captured and wrote job IDs. Current global index: {global_index}")

            # Find pagination buttons
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Page"], .artdeco-pagination__indicator--number')
            print(f"Found {len(buttons)} pagination buttons.")

            if not buttons:
                print("No pagination buttons found.")
                break

            current_page_button = next(
                (button for button in buttons if button.get_attribute('aria-current') == 'true'),
                None
            )

            if current_page_button:
                current_page_number = int(current_page_button.get_attribute('aria-label').split(' ')[1])
                next_page_number = current_page_number + 1
                print(f"Current page number: {current_page_number}, looking for next page number: {next_page_number}")

                next_page_button = next(
                    (button for button in buttons if button.find_element(By.TAG_NAME, 'span').text == str(next_page_number)),
                    None
                )

                if not next_page_button:
                    # If the next page button is not found, click the ellipsis (dots) button to reveal more pages
                    ellipsis_button = next(
                        (button for button in buttons if '...' in button.find_element(By.TAG_NAME, 'span').text),
                        None
                    )
                    if ellipsis_button:
                        print("Ellipsis button found. Clicking it to reveal more page buttons.")
                        ellipsis_button.click()
                        time.sleep(2)  # Wait for the new page buttons to load
                        buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Page"], .artdeco-pagination__indicator--number')
                        next_page_button = next(
                            (button for button in buttons if button.find_element(By.TAG_NAME, 'span').text == str(next_page_number)),
                            None
                        )

                if next_page_button:
                    print(f"Next page button found: {next_page_number}. Clicking it.")
                    next_page_button.click()

                    # Wait for the aria-label of the current page button to update
                    WebDriverWait(driver, 10).until(
                        EC.text_to_be_present_in_element(
                            (By.CSS_SELECTOR, 'button[aria-current="true"] span'),
                            str(next_page_number)
                        )
                    )

                    time.sleep(5)  # Wait for new content to load
                    print("Page changed. Waiting for new content to load.")
                else:
                    print(f"No button found for next page number: {next_page_number}")
                    break
            else:
                print("Current page button not found.")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')
        print("Screenshot saved as 'error_screenshot.png' for debugging.")

def search_jobs(driver, keyword):
    try:
        driver.get('https://www.linkedin.com/jobs')
        print(f"Searching for jobs: Keyword: {keyword}")
        time.sleep(5)

        search_box = driver.find_element(By.CSS_SELECTOR, '.jobs-search-box__text-input')
        search_box.click()
        search_box.clear()
        search_box.send_keys(keyword + Keys.ENTER)
        time.sleep(6)

        go_to_next_page(driver, keyword)
        print(f"Saved job descriptions for keyword '{keyword}'.")
    except Exception as e:
        print("Error during job search:", e)

def main():
    search_data = load_search_data()
    if not search_data:
        print("No search data to process.")
        return

    print("Starting driver.")   
    driver = get_driver()
    login(driver)

    for data in search_data:
        keyword = data['keyword']
        search_jobs(driver, keyword)

    driver.quit()
    print("Driver quit successfully.")

if __name__ == '__main__':
    main()

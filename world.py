import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # To run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Function to scrape job listings
def scrape_freshersworld_jobs(position, location):
    # Format position and location for URL
    position_formatted = position.replace(" ", "-").lower()
    location_formatted = location.replace(" ", "-").lower()
    
    url = f"https://www.freshersworld.com/jobs/jobsearch/{position_formatted}-jobs-in-{location_formatted}"
    
    # Initialize Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Adding a sleep time to ensure the page loads completely

    try:
        # Getting job listings
        job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-container")

        jobs_data = []

        for job_element in job_elements:
            try:
                title = job_element.find_element(By.CSS_SELECTOR, ".job-title").text.strip()
                company = job_element.find_element(By.CSS_SELECTOR, ".company-name").text.strip()
                location = job_element.find_element(By.CSS_SELECTOR, ".location").text.strip()
                contract = job_element.find_element(By.CSS_SELECTOR, ".job-type").text.strip()
                description = job_element.find_element(By.CSS_SELECTOR, ".desc").text.strip()
                apply_url = job_element.find_element(By.CSS_SELECTOR, ".job-title a").get_attribute("href")

                job_info = {
                    "Position": title,
                    "Company": company,
                    "Location": location,
                    "Contract": contract,
                    "Description": description,
                    "ApplyURL": apply_url,
                }

                jobs_data.append(job_info)

            except Exception as e:
                print(f"Error extracting job details: {str(e)}")

        return jobs_data

    except Exception as e:
        print(f"Error accessing job listings page: {str(e)}")

    finally:
        driver.quit()


# Example usage:
if __name__ == "__main__":
    position = input("Enter the position you are looking for: ")
    location = input("Enter the primary location: ")
    
    scraped_jobs = scrape_freshersworld_jobs(position, location)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(scraped_jobs)
    df.to_csv("Freshersworld_jobs.csv", index=False)

    print(f"Scraped {len(scraped_jobs)} job listings from Freshersworld.")

# Startup Profile Scraper Assignment

This project is a web scraping solution to extract detailed information about startups from the Startup India Showcase platform. The assignment involves scraping startup profiles, processing the data, and saving it in a structured format. The provided solution fulfills the requirements with additional features for error handling and optimization.

---

## Deliverables

### 1. Source Code
The complete source code is provided in `main.py`. This includes all the logic for data extraction, parallel processing, and output generation.

### 2. Output Data
The final dataset is saved in `startups.json`, containing all extracted startup details in a JSON format.

---

## Features

- **Dynamic Content Handling**: Utilizes Selenium to interact with dynamic web elements.
- **Parallel Processing**: Leverages Python's `ThreadPoolExecutor` to scrape multiple profiles concurrently.
- **Retry Mechanism**: Implements retry logic to handle intermittent issues during scraping.
- **Structured Data Output**: Extracted data is saved in a clean and readable JSON format.
- **Modular Design**: Functions are well-defined for scalability and maintainability.

---

## Installation and Execution

make sure to have chromedrivers installed 

Step 1: Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>

Step 2: Install Dependencies
Install the required Python packages using:

pip install -r requirements.txt


Step 3: Run the Scraper
Execute the scraper to extract startup profiles:

python3 main.py

Step 4: Access the Output
The scraped data will be saved in a file named startups.json in the project directory.


Extracted Data Fields -

url: URL of the startup profile.
company_name: Name of the startup.
city: City of operation.
dipp_number: Startup's DIPP registration number.
startup_bio: Description of the startup.
team_details: Information about founders and co-founders.
other_details: Additional details such as industry and stage.
awards_and_certificates: List of awards and certifications.
metadata: Additional metadata such as page title.


Optional Enhancements - 
1. Enhanced Error Handling
Gracefully handles unexpected scenarios and logs errors for debugging.
2. Metadata Extraction
Includes page titles and other metadata for improved context.
3. Configurable Scraping Range
Allows users to specify the number of profiles to scrape (max_profiles).

# Startup Profile Scraper Assignment

This project provides a comprehensive web scraping solution to extract detailed information about startups from the Startup India Showcase platform. The scraper collects data, processes it efficiently, and saves the results in a structured JSON format. 

The solution is designed with enhanced features like parallel processing, robust error handling, and dynamic content scraping using Selenium.

---

## **Deliverables**

### 1. Source Code
The complete source code is provided in `main.py`. It includes logic for:
- Scraping startup profiles
- Parallel data processing
- Saving the extracted data in JSON format

### 2. Output Data
The final dataset is saved as `startups.json`, containing detailed information about each startup profile.

---

## **Features**

### Core Features
- **Dynamic Content Handling**: Uses Selenium to scrape content that requires JavaScript execution.
- **Parallel Processing**: Scrapes multiple profiles concurrently to save time and improve efficiency.
- **Retry Mechanism**: Automatically retries failed profile scrapes to handle intermittent issues.
- **Structured Output**: Saves data in a clean and readable JSON format.

### Optional Enhancements
1. **Enhanced Error Handling**: Gracefully manages unexpected scenarios and logs errors for debugging.
2. **Metadata Extraction**: Includes page titles and additional metadata for improved context.
3. **Configurable Scraping Range**: Allows users to specify the number of profiles to scrape using the `max_profiles` parameter.

---

## **Installation and Setup**

### Step 1: Clone the Repository
Clone the repository and navigate to the project directory:
```bash
git clone <repository-url>
cd <repository-name>
```

### Step 2: Install Python Dependencies
Install the required packages listed in the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Step 3: Install Google Chrome and ChromeDriver
1. **Google Chrome**: Download and install the latest version of [Google Chrome](https://www.google.com/chrome/).  
2. **ChromeDriver**: Install ChromeDriver. You can:
   - Use `webdriver-manager` for automated installation (already included in the code).
   - Alternatively, download the correct version of ChromeDriver from the [ChromeDriver Downloads page](https://chromedriver.chromium.org/downloads) and ensure it matches your Chrome version.

### Step 4: Run the Scraper
Execute the script to start scraping startup profiles:
```bash
python3 main.py
```

### Step 5: Access the Output
After running the script, the extracted data will be saved in the `startups.json` file in the project directory.

---

## **Extracted Data Fields**

The scraper extracts the following data points for each startup:

| **Field**               | **Description**                                                |
|-------------------------|----------------------------------------------------------------|
| `url`                   | URL of the startup profile.                                   |
| `company_name`          | Name of the startup.                                          |
| `city`                  | City of operation.                                            |
| `dipp_number`           | Startup's DIPP registration number.                           |
| `startup_bio`           | Brief description of the startup.                             |
| `team_details`          | Information about founders and co-founders.                  |
| `other_details`         | Additional details such as industry and stage of growth.      |
| `awards_and_certificates` | List of awards and certifications achieved by the startup.   |
| `metadata`              | Extra metadata, such as the page title.                       |

---

## **Output Example**
Here’s an example of the generated JSON data:
```json
[
  {
    "url": "https://www.startupindia.gov.in/startup-india-showcase#/profile/1",
    "company_name": "Example Startup",
    "city": "New Delhi",
    "dipp_number": "123456",
    "startup_bio": "An innovative company solving real-world problems.",
    "team_details": {
      "founder": "John Doe",
      "cofounder": "Jane Doe"
    },
    "other_details": {
      "industry": "Technology",
      "stage": "Growth"
    },
    "awards_and_certificates": {
      "certifications": ["ISO 9001"],
      "awards": ["Best Startup 2024"]
    },
    "metadata": {
      "page_title": "Startup Profile - Example Startup"
    }
  }
]
```

---

## **Additional Notes**
- **Retry Mechanism**: If a profile fails to scrape, the script retries up to 3 times before skipping.
- **Dynamic Range**: Modify the `max_profiles` parameter in the script to change the number of profiles scraped.

---

## **Project Structure**

```
.
├── main.py             # Main script for scraping
├── requirements.txt    # Python dependencies
├── startups.json       # Output file containing scraped data
├── README.md           # Documentation
```

---

## **Review Metrics**

1. **Functionality**: Accurate and complete extraction of all startup data points.
2. **Code Quality**: Clean, modular, and well-documented code.
3. **Efficiency**: Optimized data extraction using parallel processing.
4. **Error Handling**: Robust handling of dynamic content and unexpected scenarios.
5. **Completeness**: All deliverables are provided, and instructions are clear and easy to follow.
6. **Innovation**: Additional features like metadata extraction and enhanced error handling.

---

## **Contact**
For any questions or assistance, feel free to reach out to [yogesh7k.2002@gmail.com].

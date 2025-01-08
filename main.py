import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------------------------------------------------------
# SECTION: Configuration and Setup
# ------------------------------------------------------------------------------
def configure_driver():
    """
    Configures and returns a Selenium WebDriver instance with the necessary options.

    Returns:
        WebDriver: Configured Chrome WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    return driver

# ------------------------------------------------------------------------------
# SECTION: Scraping Logic
# ------------------------------------------------------------------------------
def scrape_startup_profile(profile_number):
    """
    Scrapes data for a specific startup profile.

    Args:
        profile_number (int): Profile number to scrape.

    Returns:
        dict: Dictionary containing profile data, or None if scraping fails.
    """
    # Configure Chrome options for headless operation
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )

    url = f"https://www.startupindia.gov.in/startup-india-showcase#/profile/{profile_number}"

    try:
        driver.get(url)
        time.sleep(10)  # Allow page to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Allow dynamic content to load

        # Parse the page source with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract profile data
        profile_data = {
            "url": url,
            "company_name": extract_startup_name(soup),
            "city": extract_city(soup),
            "dipp_number": _extract_dipp_number(soup),
            "startup_bio": _extract_startup_bio(soup),
            "team_details": _extract_team_details(soup),
            "other_details": _extract_other_details(soup),
        }

        # Add awards and certificates
        awards_and_certificates = _extract_awards_and_certificates(soup)
        profile_data.update(awards_and_certificates)

        return profile_data

    except Exception as e:
        print(f"Error scraping profile {profile_number}: {e}")
        return None

    finally:
        driver.quit()

# ------------------------------------------------------------------------------
# SECTION: Helper Functions for Data Extraction
# ------------------------------------------------------------------------------
def extract_startup_name(soup):
    """
    Extracts the startup name from the page.

    Args:
        soup (BeautifulSoup): Parsed HTML soup.

    Returns:
        str: Startup name, or None if not found.
    """
    startup_name_element = soup.find('h3', class_='startup-name')
    return startup_name_element.text.strip() if startup_name_element else None

def extract_city(soup):
    """
    Extracts the city information from the profile.

    Args:
        soup (BeautifulSoup): Parsed HTML soup.

    Returns:
        str: City name, or None if not found.
    """
    profile_details = soup.find_all('div', class_='d-flex flex-column profile-details')
    
    for div in profile_details:
        city_label_div = div.find('div', string='City')
        if city_label_div:
            city_value_div = city_label_div.find_next_sibling('div')
            return city_value_div.text.strip() if city_value_div else None
    return None

def _extract_dipp_number(soup):
    """
    Extracts the DIPP number from the profile.

    Args:
        soup (BeautifulSoup): Parsed HTML soup.

    Returns:
        str: DIPP number, or None if not found.
    """
    profile_details = soup.find_all('div', class_='d-flex flex-column profile-details')
    for div in profile_details:
        dip = div.find('div', string='DIPP Number')
        if dip:
            dips = dip.find_next_sibling('div')
            return dips.text.strip() if dips else None
    return None

def _extract_startup_bio(soup):
    """
    Extracts the startup bio/description.

    Args:
        soup (BeautifulSoup): Parsed HTML soup.

    Returns:
        str: Startup bio, or None if not found.
    """
    startup_bio = soup.find('div', class_='professional-bio-description')
    return startup_bio.text.strip() if startup_bio else None

def _extract_team_details(soup):
    """
    Extracts team details such as founder and cofounder names.

    Args:
        soup (BeautifulSoup): Parsed HTML soup.

    Returns:
        dict: Dictionary with founder and cofounder names.
    """
    team_details = {}

    # Extract founder details
    founder_section = soup.find('div', class_='row-one no-gutters d-flex')
    if founder_section:
        founder_name_elem = founder_section.find('div', class_='founder-name')
        if founder_name_elem:
            team_details['founder'] = founder_name_elem.text.strip()

    # Extract cofounder details
    cofounder_section = soup.find('div', class_='card border-0 co-founders clearfix')
    if cofounder_section:
        cofounder_name_elem = cofounder_section.find('div', class_='co-founder-name')
        if cofounder_name_elem:
            team_details['cofounder'] = cofounder_name_elem.text.strip()
    
    return team_details

def _extract_other_details(soup):
    """
    Extracts other relevant details about the startup.

    Args:
        soup (BeautifulSoup): Parsed HTML soup.

    Returns:
        dict: Dictionary of additional details.
    """
    dimensions = {}
    others = soup.find('article', class_='article article-border-radius other-detail-article')
    
    if not others:
        return dimensions

    cols = others.find_all('div', class_='col-md-4 d-flex startup-info py-4')
    
    for col in cols:
        header_elem = col.find('div', class_='heading')
        value_elem = col.find('div', class_='text')
        
        if header_elem and value_elem:
            header = header_elem.text.strip()
            value = value_elem.text.strip()
            dimensions[header.lower()] = value
    
    return dimensions

def _extract_awards_and_certificates(soup):
    """
    Extracts awards and certificates from the profile page.

    Args:
        soup (BeautifulSoup): Parsed HTML soup.

    Returns:
        dict: Dictionary containing awards and certificates.
    """
    awards_and_certificates = {}

    container = soup.find('article', class_='award-certificate-wrapper')
    if container:
        sections = container.find_all('div', class_='sub-box')

        for section in sections:
            title_elem = section.find('h4', class_='award-ttl')
            if not title_elem:
                continue

            title = title_elem.text.strip()
            list_elem = section.find('ul', class_='award-certificate-list')
            if list_elem:
                items = [li.text.strip() for li in list_elem.find_all('li')]
                if title == 'Awards':
                    awards_and_certificates['awards'] = items
                elif title == 'Certificates':
                    awards_and_certificates['certificates'] = items

    return awards_and_certificates

# ------------------------------------------------------------------------------
# SECTION: Main Script to Scrape All Profiles
# ------------------------------------------------------------------------------
def scrape_all_profiles(max_profiles=219):
    """
    Scrapes all startup profiles up to a given limit and saves the data in a JSON file.

    Args:
        max_profiles (int): Maximum number of profiles to scrape.

    Returns:
        list: List of dictionaries containing scraped data for all profiles.
    """
    all_profiles = []

    for profile_num in range(1, max_profiles + 1):
        profile_data = scrape_startup_profile(profile_num)

        if profile_data:
            all_profiles.append(profile_data)

        time.sleep(2)  # To avoid overloading the server

        print(f"Scraped profile {profile_num}")

    # Save the scraped data to a JSON file
    with open('startup_profiles.json', 'w', encoding='utf-8') as f:
        json.dump(all_profiles, f, ensure_ascii=False, indent=4)

    return all_profiles

# Run the scraper
if __name__ == "__main__":
    print("Starting the scraping process...")
    scraped_profiles = scrape_all_profiles()
    print("Scraping completed. Data saved to 'startup_profiles.json'.")

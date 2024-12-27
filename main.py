import requests
from bs4 import BeautifulSoup
import json
import time
from concurrent.futures import ThreadPoolExecutor
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
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# ------------------------------------------------------------------------------
# SECTION: Scraping Logic
# ------------------------------------------------------------------------------
def scrape_startup_profile(profile_number, retries=3):
    """
    Scrapes data for a specific startup profile with retry logic.
    """
    url = f"https://www.startupindia.gov.in/startup-india-showcase#/profile/{profile_number}"
    for attempt in range(retries):
        try:
            driver = configure_driver()
            driver.get(url)
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            profile_data = {
                "url": url,
                "company_name": extract_startup_name(soup),
                "city": extract_city(soup),
                "dipp_number": _extract_dipp_number(soup),
                "startup_bio": _extract_startup_bio(soup),
                "team_details": _extract_team_details(soup),
                "other_details": _extract_other_details(soup),
                "metadata": _extract_metadata(soup),  # Metadata
            }
            profile_data.update(_extract_awards_and_certificates(soup))
            return profile_data
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for profile {profile_number}: {e}")
            time.sleep(5)
        finally:
            driver.quit()
    return None

# ------------------------------------------------------------------------------
# SECTION: Helper Functions
# ------------------------------------------------------------------------------
def extract_startup_name(soup):
    """Extracts the startup name."""
    elem = soup.find('h3', class_='startup-name')
    return elem.text.strip() if elem else None

def extract_city(soup):
    """Extracts the city information."""
    profile_details = soup.find_all('div', class_='d-flex flex-column profile-details')
    for div in profile_details:
        city_label_div = div.find('div', string='City')
        if city_label_div:
            city_value_div = city_label_div.find_next_sibling('div')
            return city_value_div.text.strip() if city_value_div else None
    return None

def _extract_dipp_number(soup):
    """Extracts the DIPP number."""
    profile_details = soup.find_all('div', class_='d-flex flex-column profile-details')
    for div in profile_details:
        dip = div.find('div', string='DIPP Number')
        if dip:
            dips = dip.find_next_sibling('div')
            return dips.text.strip() if dips else None
    return None

def _extract_startup_bio(soup):
    """Extracts the startup bio."""
    bio = soup.find('div', class_='professional-bio-description')
    return bio.text.strip() if bio else None

def _extract_team_details(soup):
    """Extracts team details."""
    details = {}
    founder_section = soup.find('div', class_='row-one no-gutters d-flex')
    if founder_section:
        founder_name = founder_section.find('div', class_='founder-name')
        details['founder'] = founder_name.text.strip() if founder_name else None
    cofounder_section = soup.find('div', class_='card border-0 co-founders clearfix')
    if cofounder_section:
        cofounder_name = cofounder_section.find('div', class_='co-founder-name')
        details['cofounder'] = cofounder_name.text.strip() if cofounder_name else None
    return details

def _extract_other_details(soup):
    """Extracts other details."""
    details = {}
    others = soup.find('article', class_='article article-border-radius other-detail-article')
    if others:
        cols = others.find_all('div', class_='col-md-4 d-flex startup-info py-4')
        for col in cols:
            header = col.find('div', class_='heading')
            value = col.find('div', class_='text')
            if header and value:
                details[header.text.strip().lower()] = value.text.strip()
    return details

def _extract_awards_and_certificates(soup):
    """Extracts awards and certificates."""
    awards = {}
    container = soup.find('article', class_='award-certificate-wrapper')
    if container:
        for section in container.find_all('div', class_='sub-box'):
            title = section.find('h4', class_='award-ttl')
            items = [li.text.strip() for li in section.find_all('li')] if section.find('ul') else []
            if title and items:
                awards[title.text.strip().lower()] = items
    return awards

def _extract_metadata(soup):
    """Extracts metadata for extra details."""
    return {"page_title": soup.title.string.strip()} if soup.title else {}

# ------------------------------------------------------------------------------
# SECTION: Parallel Scraping
# ------------------------------------------------------------------------------
def scrape_all_profiles_parallel(max_profiles=219):
    """Scrapes profiles in parallel."""
    with ThreadPoolExecutor() as executor:
        profiles = list(executor.map(scrape_startup_profile, range(1, max_profiles + 1)))
    profiles = [profile for profile in profiles if profile]
    with open('startups.json', 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    return profiles

# ------------------------------------------------------------------------------
# Run the Scraper
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("Starting parallel scraping...")
    all_profiles = scrape_all_profiles_parallel()
    print(f"Scraping completed. {len(all_profiles)} profiles saved.")

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Proxy URL
SBR_WEBDRIVER = 'https://brd-customer-hl_4fdeddfa-zone-ai_scrapper:fw1x85e3ot9y@brd.superproxy.io:9515'

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless for no GUI
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

def scrape_website(website):
    print('Connecting to Scraping Browser...')
    
    # Create the Remote WebDriver
    driver = webdriver.Remote(
        command_executor=SBR_WEBDRIVER,
        options=options
    )
    
    try:
        print('Connected! Navigating...')
        driver.get(website)
        
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
    
    finally:
        driver.quit()  # Make sure to close the session after use

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content,'html.parser')
    for script_or_style in soup(['script','style']):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content ="\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip() )

    return cleaned_content

def split_dom_content(dom_content ,max_length=6000):
    return[
        dom_content[i:i+max_length] for i in range(0, len(dom_content),max_length)
    ]

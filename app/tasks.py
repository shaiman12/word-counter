from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from app.models import JobResult
from rq import get_current_job
import os


def count_words_at_url(url: str) -> int:
    job = get_current_job()
    driver = None
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.binary_location = "/usr/bin/chromium"

        service = Service(executable_path="/usr/bin/chromedriver", log_path="/dev/null")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        
        driver.implicitly_wait(20)

        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        for element in soup(["script", "style", "meta", "noscript"]):
            element.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)
        words = [word for word in text.split() if word]
        word_count = len(words)

        JobResult.update(job.id, word_count, words)
        return word_count

    except Exception as e:
        error_message = f"Error processing URL {url}: {str(e)}"
        JobResult.mark_failed(job.id, error_message)
        raise

    finally:
        if driver:
            driver.quit()

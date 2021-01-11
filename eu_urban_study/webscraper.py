import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

output_path = "."

# Statistics output:
# year_data_point and article_data:
#  - year_data_point dict contains: article_count, citation_count, reference_count, 
#  - article_data dict contains: title, author(s), year, reference_count, total_citation, abstract, keywords, type
# The special dict containing all articles with Chinese authors:
#  - china_article_data

def journal_statistics(driver):
    year_data_point = {}
    article_data = {}

    for i in range(1,28):
        year = 1993 + i
        year_data_point[str(year)] = {}
        year_data_point[str(year)]["article_count"] = 0
        year_data_point[str(year)]["citation_count"] = 0
        year_data_point[str(year)]["reference_count"] = 0
        for j in range(1, 5 if i > 1 else 3):
            driver.get("https://journals.sagepub.com/toc/eura/" + str(i) + "/" + str(j))

            WebDriverWait(driver, timeout=100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "table.articleEntry"))
            )
            
            article_count = len(driver.find_elements_by_css_selector("table.articleEntry"))
            year_data_point[str(year)]["article_count"] += article_count

            for k in range(0, article_count):
                WebDriverWait(driver, timeout=100).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "table.articleEntry div.art_title a")) and
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.articleEntryAuthor"))
                )

                article = driver.find_elements_by_css_selector("table.articleEntry div.art_title a")[k]
                article_name = article.text

                print("Inspecting the article '" + article_name + "'...")
                article_data[article_name] = {}
                article_data[article_name]['title'] = article_name
                article_data[article_name]['author'] = ""
                for author in driver.find_elements_by_css_selector("div.articleEntryAuthor a"):
                    article_data[article_name]['author'] += author.text
                article_data[article_name]['year'] = year

                if k == 0 and year == 1994 or "Editorial" in article_name or "editorial" in article_name:
                    continue
                
                WebDriverWait(driver, timeout=100).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "table.articleEntry div.art_title a"))
                )

                driver.get(article.get_attribute("href"))

                WebDriverWait(driver, timeout=100).until(
                  EC.element_to_be_clickable((By.CSS_SELECTOR, "li.articleMetrics a"))
                )

                reference_count = 0
                try:
                    WebDriverWait(driver, timeout=20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "table.references tbody"))
                    )
                    reference_count = len(driver.find_elements_by_css_selector("table.references tr"))
                    year_data_point[str(year)]["reference_count"] += reference_count
                    article_data[article_name]["reference_count"] = reference_count
                except TimeoutException:
                    pass

                article_abstract = ""
                try:
                    WebDriverWait(driver, timeout=20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.abstractSection p"))
                    )
                    article_abstract = driver.find_element_by_css_selector("div.abstractSection p").text
                except TimeoutException:
                    pass
                
                keywords = []
                try:
                    WebDriverWait(driver, timeout=20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "ddiv.abstractKeywords"))
                    )
                    keywords = [i.text for i in driver.find_elements_by_css_selector("div.abstractKeywords a")]
                except TimeoutException:
                    pass
                
                article_data[article_name]["article_type"] = article_type = driver.find_element_by_css_selector("span.ArticleType span").text
                article_data[article_name]["article_abstract"] = article_abstract
                article_data[article_name]["keywords"] = keywords

                article_metrics_button = driver.find_element_by_css_selector("li.articleMetrics a")
                driver.get(article_metrics_button.get_attribute("href"))

                WebDriverWait(driver, timeout=100).until(
                  EC.visibility_of_element_located((By.CSS_SELECTOR, "div.serviceCitationWidget a span"))
                )

                citation_data = driver.find_elements_by_css_selector("div.serviceCitationWidget a span")
                
                print("Article '" + article_name + "' has " + citation_data[0].text + " cross reference and " + citation_data[1].text + " other citations.")
                citation_count = int(citation_data[0].text) + int(citation_data[1].text)
                year_data_point[str(year)]["citation_count"] += citation_count
                article_data[article_name]['total_citation'] = citation_count
                
                driver.back()
                driver.back()

                WebDriverWait(driver, timeout=100).until(
                  EC.visibility_of_element_located((By.CSS_SELECTOR, "table.articleEntry div.art_title a"))
                )

        print("Year " + str(year) + " has " + str(year_data_point[str(year)]["article_count"]) + " articles and "
                + str(year_data_point[str(year)]["citation_count"]) + " citations!")
    return year_data_point

def article_keywords_count():
    return 0

def article_china_related():
    return 0

def article_china_keyword():
    return 0

def article_china_info():
    return 0

if __name__ == "__main__":
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
    driver.maximize_window()
    print(journal_dissertation_and_citation_count(driver))
    driver.close()
import pandas as pd
import requests
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
#  - year_data_point dict contains: article_count, citation_count, reference_count
#  - article_data dict contains: title, author(s), year, reference_count, total_citation, abstract, keywords, type
# The special dict containing all articles with Chinese authors:
#  - china_article_data

black_list = [
    "Missing Voices/Missing Spaces: Reflections on ‘A New Europe?’",
    "Harnessing the Information Society? European Union Policy and Information and Communication Technologies"
]

def journal_statistics(driver, file_article, file_article_read):
    already_processed = file_article_read.read()
    for i in range(3,28):
        year = 1993 + i
        # year_data_point[str(year)] = {}
        # year_data_point[str(year)]["article_count"] = 0
        # year_data_point[str(year)]["citation_count"] = 0
        # year_data_point[str(year)]["reference_count"] = 0
        for j in range(2, 3):
            driver.get("https://journals.sagepub.com/toc/eura/" + str(i) + "/" + str(j))
            
            print("this is Volume" + str(i) + " issue " + str(j))
            print("Checking the article table entry...")

            # WebDriverWait(driver, timeout=100).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, "table.articleEntry"))
            # )
            driver.implicitly_wait(20)

            article_count = len(driver.find_elements_by_css_selector("table.articleEntry"))
            # year_data_point[str(year)]["article_count"] += article_count

            for k in range(0, article_count):
                article_data = {}

                driver.get("https://journals.sagepub.com/toc/eura/" + str(i) + "/" + str(j))
                print("Checking the author...")

                WebDriverWait(driver, timeout=200).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table.articleEntry")) and
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table.articleEntry div.art_title a")) and
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.articleEntryAuthor"))
                )

                article = driver.find_elements_by_css_selector("table.articleEntry div.art_title a")[k]
                article_name = article.text

                if article_name in already_processed:
                    print("This article has already been processed!")
                    continue

                print("Inspecting the article '" + article_name + "'...")
                article_data['title'] = article_name
                article_data['authors'] = ""
                for author in driver.find_elements_by_css_selector("div.articleEntryAuthor a"):
                    article_data['authors'] += author.text + ";"
                article_data['year'] = year

                with requests.get(article.get_attribute("href")) as r:
                    if "application/pdf" in r.headers['Content-Type']:
                        continue
                
                print("Checking the article title clickable...")
                WebDriverWait(driver, timeout=100).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "table.articleEntry div.art_title a"))
                )

                driver.get(article.get_attribute("href"))

                reference_count = 0
                try:
                    print("Checking the table of references...")
                    WebDriverWait(driver, timeout=5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table.references tbody"))
                    )
                    reference_count = len(driver.find_elements_by_css_selector("table.references tr"))
                    # year_data_point[str(year)]["reference_count"] += reference_count
                except TimeoutException:
                    pass

                article_abstract = ""
                try:
                    print("Checking the abstract section...")
                    if not article_name in black_list:
                        WebDriverWait(driver, timeout=5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.abstractSection p"))
                        )
                        article_abstract = driver.find_element_by_css_selector("div.abstractSection p").text
                except TimeoutException:
                    pass
                
                keywords = ""
                try:
                    print("Checking the keyword section...")
                    if not article_name in black_list:
                        WebDriverWait(driver, timeout=5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.abstractKeywords"))
                        )
                        keywords = ";".join([i.text for i in driver.find_elements_by_css_selector("div.abstractKeywords a")])
                except TimeoutException:
                    pass
                
                article_data["article_type"] = article_type = driver.find_element_by_css_selector("span.ArticleType span").text
                article_data["article_abstract"] = article_abstract
                article_data["keywords"] = keywords
                article_data["reference_count"] = reference_count

                article_metrics_button = driver.find_element_by_css_selector("li.articleMetrics a")
                driver.get(article_metrics_button.get_attribute("href"))

                WebDriverWait(driver, timeout=100).until(
                  EC.presence_of_element_located((By.CSS_SELECTOR, "div.serviceCitationWidget a span"))
                )

                citation_data = driver.find_elements_by_css_selector("div.serviceCitationWidget a span")
                
                print("Article '" + article_name + "' has " + citation_data[0].text + " cross reference and " + citation_data[1].text + " other citations.")
                citation_count = int(citation_data[0].text) + int(citation_data[1].text)
                # year_data_point[str(year)]["citation_count"] += citation_count
                article_data['total_citation'] = citation_count

                file_article.write("\"" + article_data['title'] + "\"," + article_data['authors'] + "," + str(article_data['year'])
                             + "," + str(article_data['reference_count']) + "," + str(article_data["total_citation"]) + ",\"" + 
                             article_data["article_abstract"] + "\"," + article_data["keywords"] + ",\"" + article_data["article_type"] + "\"\n" )

if __name__ == "__main__":
    f_article = open("article.csv", "a")
    f_article_read = open("article.csv", "r")

    # f_year.write("article_count,citation_count,reference_count\n")
    # f_article.write("title,authors,year,reference_count,total_citation,abstract,keywords,type\n")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
    driver.maximize_window()
    try:
        journal_statistics(driver, f_article, f_article_read)
    except TimeoutException:
        journal_statistics(driver, f_article, f_article_read)
    driver.close()
    f_article.close()
    f_article_read.close()
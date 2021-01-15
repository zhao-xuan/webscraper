import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import ssl

# 数据分析内容如下：
# 1. 每年论文发表量
# 2. 每年中国学者的发表数量及其基本信息
# 3. 每年不同种类文章的数量
# 4. 每年的热词，每年中国学者的热词

def data_processing():
    with open('article.csv', newline='') as csv_file:
        raw_data = csv.DictReader(csv_file)
        data_by_year = [[] for i in range(28)]
        for row in raw_data:
            print(int(row["year"]) - 1994)
            data_by_year[int(row["year"]) - 1994].append(row)

        total_count_by_year = [0 for i in range(28)]
        china_count_by_year = [0 for i in range(28)]
        china_article_by_year = [[] for i in range(28)]
        category_by_year = [{} for i in range(28)]
        keyword_by_year = [[] for i in range(28)]
        china_keyword_by_year = [[] for i in range(28)]

        china_last_name = []
        with open('lastname.txt', 'r') as last_name_file:
            china_last_name = last_name_file.read().split("\n")
            
        for i in range(28):
            total_count_by_year[i] = len(data_by_year[i])
            temp_china_count = 0
            year_keywords = ""
            for article in data_by_year[i]:
                for last_name in china_last_name:
                    if last_name in word_tokenize(article["authors"]):
                        print("hahah")
                        china_article_by_year[i].append(article)
                        temp_china_count += 1
                
                if not article["type"] in category_by_year[i].keys():
                    category_by_year[i][article["type"]] = 1
                else:
                    category_by_year[i][article["type"]] += 1

                year_keywords += article["keywords"].lower()
            
            china_count_by_year[i] = temp_china_count
            keyword_by_year[i] = FreqDist(word_tokenize(year_keywords)).most_common(10)

            china_year_keywords = ""
            for article in china_article_by_year[i]:
                china_year_keywords += article["keywords"]

            china_keyword_by_year[i] = FreqDist(word_tokenize(china_year_keywords)).most_common(10)
    return [total_count_by_year, china_count_by_year, china_article_by_year, category_by_year, keyword_by_year, china_keyword_by_year]

if __name__ == "__main__":
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('punkt')
    analysis = data_processing()
    total_count_by_year = analysis[0]
    china_count_by_year = analysis[1]
    china_article_by_year = analysis[2]
    category_by_year = analysis[3]
    keyword_by_year = analysis[4]
    china_keyword_by_year = analysis[5]
    print("正在分析每一年的期刊杂志数据...")
    print("期刊杂志数据分析完毕！")
    with open('analysis.csv', 'w') as file:
        file.write("year, total_count, china_total_count, top_keywords, china_top_keywords\n")
        for i in range(28):
            file.write(str(i + 1994) + ", " + str(total_count_by_year[i]) + ", " + str(china_count_by_year[i]) + ", "
                + ";".join(str(keyword_by_year[i]).split(",")) + ", " + ";".join(str(china_keyword_by_year[i]).split(",")) + "\n")
    with open('china_article.csv', "w") as file:
        temp_saved = []
        file.write('title,authors,year,reference_count,total_citation,abstract,keywords,type')
        for i in range(28):
            for article_data in china_article_by_year[i]:
                if not article_data['title'] in temp_saved:
                    temp_saved.append(article_data['title'])
                    file.write("\"" + article_data['title'] + "\"," + article_data['authors'] + "," + str(article_data['year'])
                                    + "," + str(article_data['reference_count']) + "," + str(article_data["total_citation"]) + ",\"" + 
                                    article_data["abstract"] + "\"," + article_data["keywords"] + ",\"" + article_data["type"] + "\"\n" )
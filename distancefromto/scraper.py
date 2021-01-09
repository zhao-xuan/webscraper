'''
该脚本使用前提：
1. 请安装python3.0以上版本，并且用pip/pip3安装pandas，openpyxl和selenium
2. 在电脑上安装Chrome浏览器
3. 在/usr/local/bin目录下安装https://sites.google.com/a/chromium.org/chromedriver/downloads，注意选择正确的chrome版本(86/87/88)
4. 该脚本目前仅供MacOS使用
'''

# pandas是一个数据分析很常用的库
import pandas as pd
# selenium是一个常用的Python爬虫工具，作用是操纵/提交/截取网页上的数据
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# 在这里输入excel文件的路径
xls_file_path = "~/Downloads/country.xlsx"

# 这里会利用pandas将excel表格导入当前Python程序
xls_file = pd.read_excel(io=xls_file_path)

def get_and_print_distance(src_country, dest_country):
    # 这里用启动好的Chrome浏览器去访问https://www.distancefromto.net这个网址
    driver.get("https://www.distancefromto.net")

    # 待网址加载成功之后，寻找起始地输入框，起始地输入框的id和class相关信息可以从Chrome/Safari的开发者工具中查找
    src = driver.find_element_by_id("distancefrom")
    # 清空起始地输入框，以防止之前有多余的文字
    src.clear()
    # 在起始地输入框中输入文字
    src.send_keys(src_country)

    # 寻找目的地输入框，寻找方法同上，输入内容的代码同上
    dest = driver.find_element_by_id("distanceto")
    dest.clear()
    dest.send_keys(dest_country)

    # 寻找“Measure Distance”按键，并按下该按键
    measure = driver.find_element_by_id("hae")
    # 按下网页中按钮的方式有输入回车(Keys.RETURN)或者用`measure.submit()`
    measure.send_keys(Keys.RETURN)

    # 在按下按钮之后，需要等网页重新加载完毕，100指的是timeout时间（超过这个时间则会报错，例如“网页无响应”），而`.until()`中的内容指的是等待的条件，如果条件全部满足，则继续往下执行代码，否则一直在这里停留
    WebDriverWait(driver, 100).until(
                lambda driver: driver.find_element_by_id("totaldistancekm") and 
                               driver.find_element_by_id("totaldistancemiles") and 
                               driver.find_element_by_id("totaldistancenamiles"))

    # 利用`<element>.get_attribute("value")`来寻找得出的结果，注意这里不能使用text，因为结果输入框是一个网页表单元素
    distancekm = driver.find_element_by_id("totaldistancekm").get_attribute("value")
    distancemile = driver.find_element_by_id("totaldistancemiles").get_attribute("value")
    distancenmile = driver.find_element_by_id("totaldistancenamiles").get_attribute("value")

    # 在命令行输出结果
    print(distancekm + "," + distancemile + "," + distancenmile)

if __name__ == "__main__":
    # 这里选择防止浏览器弹出(headless模式)，如果删除这两行代码则Chrome浏览器会自动弹出
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # 这里先启动chromedriver程序，chromedriver是用来在程序中启动Chrome浏览器的虚拟驱动
    driver = webdriver.Chrome(options=chrome_options)

    # 这里打出csv文件的头部
    print("distanceKM, distanceMILE, distanceNA")

    # 在这里利用循环将每一行都处理一遍，其中get_and_print_distance是爬虫的主要程序
    for i in xls_file.index:
        if i > 2944:
            get_and_print_distance(xls_file["Reporter"][i], xls_file["Partner"][i])

    # 关闭浏览器
    driver.close()

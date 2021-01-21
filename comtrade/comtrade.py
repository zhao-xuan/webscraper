import requests
import json

data_keys = ['pfCode', 'yr', 'period', 'periodDesc', 'aggrLevel', 'IsLeaf', 'rgCode', 'rgDesc', 
            'rtCode', 'rtTitle', 'rt3ISO', 'ptCode', 'ptTitle', 'pt3ISO', 'ptCode2', 'ptTitle2', 
            'pt3ISO2', 'cstCode', 'cstDesc', 'motCode', 'motDesc', 'cmdCode', 'cmdDescE', 'qtCode', 
            'qtDesc', 'qtAltCode', 'qtAltDesc', 'TradeQuantity', 'AltQuantity', 'NetWeight', 'GrossWeight', 
            'TradeValue', 'CIFValue', 'FOBValue', 'estCode']

if __name__ == "__main__":
    url = "https://comtrade.un.org/api/get?max=500&type=C&freq=A&px=HS&ps=2019&r=all&p=0&rg=all&cc=TOTAL"
    content = requests.get(url)
    text = content.text
    dic = json.loads(text)
    data_keys = dic['dataset'][0].keys()

    with open("comtrade.csv", "w") as file:
        for i in data_keys:
            file.write(str(i) + ",")
        file.write("\n")
        for i in dic['dataset']:
            for key in data_keys:
                file.write(str(i[key]) + ",")
            file.write("\n")
import wordcloud
import pickle
import csv

comment = ''

with open('wb.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            comment += row[2]
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')

# content_comment = pickle.load(open('./jinkou.pkl', 'rb'))
'''
基于内容的词云
'''
#content = ''
'''
print(len(content_comment))
for i in content_comment:
    content += (' ' + ' '.join(i[2]))
    try:
        for j in i[3:]:
            comment += (' ' + ' '.join(j))
    except:
        continue
w = wordcloud.WordCloud(width=1000, font_path='./msyh.ttc', background_color='white', height=700, stopwords={"回复", "知道", "觉得", "中国", "国家", "评论", "大家", "所有", "必须", "之前", "需要", "哈哈哈", "哈哈哈哈", "真的", "这种", "没有", "不会", "起来", "一点", "已经", "啊啊啊", "可能", "今天", "现在", "很多", "出来", "关注", "即可", "看到", "希望"})
w.generate(content.strip())
w.to_file('jinkou_content.png')
'''

'''
基于评论的词云
'''
w2 = wordcloud.WordCloud(width=1000, font_path='./msyh.ttc', background_color='white', height=700, stopwords={"回复", "知道", "觉得", "中国", "国家", "评论", "大家", "所有", "必须", "之前", "需要", "哈哈哈", "哈哈哈哈", "不是", "现在", "应该", "可能", "不能", "不要", "真的", "这种", "没有", "不会", "起来", "一点", "已经", "一定", "以前", "感觉", "看到", "啊啊啊"})
w2.generate(comment.strip())
w2.to_file('jinkou_comment.png')

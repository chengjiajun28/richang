a = '<div padding="10px">这是一个带有padding属性的元素</div>'

from bs4 import BeautifulSoup

# 假设html文档已经读入到了变量html_doc中
soup = BeautifulSoup(a, 'html.parser')

# 查找所有带有padding属性的元素，并删除它们的padding属性
for tag in soup.find_all(True):
    if tag.has_attr('padding'):
        del tag['padding']

# 获取处理后的html文档
processed_html = str(soup)


print(processed_html)
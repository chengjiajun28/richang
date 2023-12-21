from flask import render_template

from 网站.web.modules.index import index_blue
from 网站.web.modules.utils.some_utility import get_mysql_websites, query_data


@index_blue.route('/')
def index():
    return render_template("index.html")


@index_blue.route('/website')
def website():
    data = get_mysql_websites()

    return render_template("a.html", data=data)


@index_blue.route('/website_number', methods=["GET", "POST"])
def website_number():
    data = get_mysql_websites()

    # 示例配置
    config = {
        'host': '118.195.246.81',
        'port': 3406,
        'user': 'root',
        'password': 'ruse#@!2022r',
        'db': 'ruseinfo_uat',
        'charset': 'utf8mb4'
    }

    sql_query = f'''
            SELECT w.`域名`,
                COALESCE(SUM(CASE WHEN DATE(t.`create_time`) = CURDATE() THEN 1 ELSE 0 END), 0) AS today_count,
                COALESCE(SUM(CASE WHEN DATE(t.`create_time`) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 ELSE 0 END), 0) AS yesterday_count,
                COALESCE(SUM(CASE WHEN DATE(t.`create_time`) = DATE_SUB(CURDATE(), INTERVAL 2 DAY) THEN 1 ELSE 0 END), 0) AS before_yesterday_count
            FROM (SELECT DISTINCT `域名` FROM `datas`.`websites`) w
            LEFT JOIN auction_info t ON w.`域名` = t.website 
                                      AND DATE(t.`create_time`) >= DATE_SUB(CURDATE(), INTERVAL 2 DAY)
            GROUP BY w.`域名`;                
    '''
    result = query_data(sql_query, config)

    data_list = []
    for row in result:
        list = [row[0], int(row[1]), int(row[2]), int(row[3])]

        data_list.append(list)

    def sort_key(item):
        return item[1], item[2], item[3]

    sorted_data = sorted(data_list, key=sort_key)

    return render_template("websites_number.html", datas=sorted_data)

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pymysql
from flask import Flask, render_template

app = Flask(__name__)

# 数据库连接信息
db_config = {
    'host': '118.195.246.81',
    'port': 3406,
    'user': 'root',
    'password': 'ruse#@!2022r',
    'database': 'ruseinfo_uat',
}


# 展示数据页面
@app.route('/')
def show_data():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    sql = """
        SELECT w.`域名`,
            COALESCE(SUM(CASE WHEN DATE(t.`create_time`) = CURDATE() THEN 1 ELSE 0 END), 0) AS today_count,
            COALESCE(SUM(CASE WHEN DATE(t.`create_time`) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 ELSE 0 END), 0) AS yesterday_count,
            COALESCE(SUM(CASE WHEN DATE(t.`create_time`) = DATE_SUB(CURDATE(), INTERVAL 2 DAY) THEN 1 ELSE 0 END), 0) AS before_yesterday_count
        FROM (SELECT DISTINCT `域名` FROM `datas`.`websites`) w
        LEFT JOIN auction_info t ON w.`域名` = t.website 
                                  AND DATE(t.`create_time`) >= DATE_SUB(CURDATE(), INTERVAL 2 DAY)
        GROUP BY w.`域名`;
    """
    cursor.execute(sql)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    print(results)

    return render_template('data.html', data=results)


if __name__ == '__main__':
    app.run(port=8008)

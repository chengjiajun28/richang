from argparse import ArgumentParser

import pymysql
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 数据库连接信息
db_config = {
    'host': '118.195.246.81',
    'port': 3406,
    'user': 'root',
    'password': 'ruse#@!2022r',
    'database': 'ruseinfo_uat',
}


@app.route('/', methods=['GET', 'POST'])
def index():
    data = ['其它', '物资设备', '机动车', '采购', '拆除']

    return render_template('index.html', class_info=data)


@app.route('/selected_option', methods=['POST'])
def selected_option():
    selected_class = request.form['mySelect']

    print(selected_class)

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    sql = f'SELECT id, assets_name, create_time, website FROM `auction_info` WHERE DATE(create_time) = CURDATE()  and assets_type = "{selected_class}";'

    print(sql)

    cursor.execute(sql)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    list = []
    for i in results:
        list.append([i[1]])

    return jsonify(students=list)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=9899)

    args = parser.parse_args()
    host = args.host
    port = args.port

    print(f"启动 Flask 应用程序，IP 地址：{host}，端口：{port}")
    app.run(host=host, port=port)

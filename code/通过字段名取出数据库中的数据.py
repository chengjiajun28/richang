import pymysql

# 数据库连接配置
config = {
    'host': '118.195.246.81',
    'port': 3406,
    'user': 'root',
    'password': 'ruse#@!2022r',
    'db': 'datas',
    'charset': 'utf8mb4'
}

# 连接到数据库
connection = pymysql.connect(**config)

try:
    # 使用cursor()方法创建一个游标对象，用于执行SQL语句
    with connection.cursor() as cursor:
        # 定义SQL查询语句
        sql = "SELECT * FROM websites"

        # 执行SQL查询
        cursor.execute(sql)

        # 使用fetchall()方法获取所有数据
        rows = cursor.fetchall()

        # 遍历结果集，将每行数据转换为字典，并打印字段名和对应的值
        for row in rows:
            data_dict = dict(zip([column[0] for column in cursor.description], row))
            print("Data:", data_dict)

finally:
    # 关闭数据库连接
    connection.close()

import matplotlib.pyplot as plt
import pymysql

if __name__ == '__main__':
    connection = pymysql.connect(
        host='118.195.246.81',
        port=3406,
        user='root',
        password='ruse#@!2022r',
        database='ruseinfo_prd',
    )

    try:
        with connection.cursor() as cursor:

            sql = """SELECT
                  w.`域名`,
                  SUM(CASE WHEN DATE(t.`create_time`) = CURDATE() THEN 1 ELSE 0 END) AS today_count
                FROM
                  (SELECT DISTINCT `域名` FROM `datas`.`websites`) w
                LEFT JOIN auction_info t ON w.`域名` = t.website 
                                      AND DATE(t.`create_time`) = CURDATE()
                GROUP BY
                  w.`域名`;
                """
            cursor.execute(sql)
            result = cursor.fetchall()

            website = []
            data = []

            for i in result:
                website.append(i[0])
                data.append(i[1])

            # 创建折线图
            plt.plot(website, data, marker='o', linestyle='-', label='Revenue')

            # 添加图例、标题和轴标签
            plt.legend()
            plt.title("Monthly Revenue of a Company")
            plt.xlabel("Month")
            plt.ylabel("Revenue (USD)")

            # 旋转 x 轴标签，避免重叠
            plt.xticks(rotation=9999999999999999999999999999999999999)

            # 显示图表
            plt.show()


    finally:
        connection.close()

import threading
import time

import pymysql


def select_mysql_classification(*args, **kwargs):
    connection = pymysql.connect(
        host='118.195.246.81',
        port=3406,
        user='root',
        password='ruse#@!2022r',
        database='datas',
    )

    cursor = connection.cursor()

    sql = f"SELECT * FROM categories"
    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    classification = {}
    for words_list in result:
        # 使用 split 方法将字符串分割，以逗号为分隔符
        words_lists = str(words_list[1]).split(',')

        # 使用 strip 方法移除元素中的逗号和空格
        words_lists = [word.strip('，') for word in words_lists]

        # 使用 filter 函数过滤掉空字符串，并将结果转换为列表
        words_lists = list(filter(lambda x: x != '', words_lists))

        # 移除列表中的空格
        words_lists = [word for word in words_lists if word != '']

        classification.update({
            words_list[0]: words_lists
        })

    return result


def main(cursor, connection, mysql_classification, name, n):
    assets_type = "其它"
    for haha in mysql_classification:
        if not haha[0]:
            continue

        if not haha[1]:
            continue

        string_list = haha[1].split(',')

        # 移除列表中的空格
        words_list = [word for word in string_list if word != '']

        if haha[2]:

            string_list1 = haha[2].split(',')

            # 移除列表中的空格
            words_list1 = [word1 for word1 in string_list1 if word1 != '']

            if any(i1 in name[3] for i1 in words_list1):
                continue

        if any(i in name[3] for i in words_list):
            assets_type = haha[0]

            break

    sql = f"UPDATE auction_info SET assets_type = '{assets_type}' WHERE id = {name[0]}"
    print(sql)

    cursor.execute(sql)
    connection.commit()
    print(f"{n}已修改")


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

            sql = "SELECT * FROM auction_info WHERE DATE(create_time) = DATE('2023-12-06');"
            cursor.execute(sql)
            result = cursor.fetchall()

            mysql_classification = select_mysql_classification()

            for _, name in enumerate(result):
                thread = threading.Thread(target=main, args=(cursor, connection, mysql_classification, name, _))

                thread.start()

                time.sleep(0.3)


    finally:
        connection.close()

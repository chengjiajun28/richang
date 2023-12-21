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


mysql_classification = select_mysql_classification()

for haha in mysql_classification:

    if not haha[1]:
        continue

    string_list = haha[1].split(',')

    # 移除列表中的空格
    words_list = [word for word in string_list if word != '']

    if haha[2]:

        string_list1 = haha[2].split(',')

        # 移除列表中的空格
        words_list1 = [word1 for word1 in string_list1 if word1 != '']

        print(words_list1)
    #
    #     # if any(i1 in name[3] for i1 in words_list1):
    #     #     continue

    # print(words_list)
    #
    # # if any(i in name[3] for i in words_list):
    # #     assets_type = haha[0]
    # #
    # #     break

data = [['allauc', 74, 85, 0], ['bd_ispacechina_zs', 0, 0, 0], ['beijing_gy', 0, 5, 10], ['beijing_js', 2, 5, 11], ['beijing_zf_cc', 0, 0, 0], ['beijing_zf_f', 0, 0, 0], ['beijing_zf_g', 0, 0, 0]]

def sort_key(item):
    return item[1], item[2], item[3]

sorted_data = sorted(data, key=sort_key)

print(sorted_data)
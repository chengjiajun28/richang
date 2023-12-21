import pandas as pd

# 读取txt文件
input_file_name = 'new_example.txt'
with open(input_file_name, 'r', encoding='utf-8') as file:
    content = file.read()

# 将txt文件内容分割成行
lines = content.split('\n')

# 将行列表转换为DataFrame
df = pd.DataFrame(lines, columns=['Data'])

# 如果需要，可以对数据进行进一步处理，例如删除中文字符等

# 读取现有的Excel文件
existing_excel_file = 'existing_data.xlsx'
df_existing = pd.read_excel(existing_excel_file, index_col=0)

# 将新数据添加到现有数据
combined_df = pd.concat([df_existing, df])

# 保存处理后的数据到新的Excel文件
output_excel_file_name = 'new_combined_data.xlsx'
combined_df.to_excel(output_excel_file_name, index=False)

print(f"已将txt文件中的数据添加到Excel文件并将处理后的数据保存到 {output_excel_file_name}")
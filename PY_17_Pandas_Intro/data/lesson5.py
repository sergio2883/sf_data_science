import pandas as pd
#countries_data = pd.read_csv('D:/IDE/github/sf_data_science/PY_17_Pandas_Intro/data/countries.csv', sep=';')
countries_data = pd.read_csv('countries.csv', sep=';')
#display(countries_data)
print(countries_data)

# import pandas as pd
# import os

# # Получаем путь к папке, где находится скрипт
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Формируем путь к файлу (он в той же папке, что и скрипт)
# file_path = os.path.join(script_dir, 'countries.csv')

# # Проверяем, существует ли файл
# if os.path.exists(file_path):
#     countries_data = pd.read_csv(file_path, sep=';')
#     #display(countries_data)
#     print(countries_data)
# else:
#     # Если нет, проверяем в подпапке data
#     file_path = os.path.join(script_dir, 'data', 'countries.csv')
#     if os.path.exists(file_path):
#         countries_data = pd.read_csv(file_path, sep=';')
#         #display(countries_data)
#         print(countries_data)
#     else:
#         print(f"Файл не найден. Проверьте наличие файла в:")
#         print(f"  - {os.path.join(script_dir, 'countries.csv')}")
#         print(f"  - {os.path.join(script_dir, 'data', 'countries.csv')}")
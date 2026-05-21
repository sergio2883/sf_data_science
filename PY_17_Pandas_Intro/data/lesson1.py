import pandas as pd
# print(pd.__version__)
# print(pd.__name__)
# countries = pd.Series(
#     data = ['Англия', 'Канада', 'США', 'Россия', 'Украина', 'Беларусь', 'Казахстан'],
#     index = ['UK', 'CA', 'US', 'RU', 'UA', 'BY', 'KZ'],
#     name = 'countries'
# )
# print(countries)

# countries = pd.Series({
#     'UK': 'Англия',
#     'CA': 'Канада',
#     'US' : 'США',
#     'RU': 'Россия',
#     'UA': 'Украина',
#     'BY': 'Беларусь',
#     'KZ': 'Казахстан'},
#     name = 'countries'
# )
# print(countries)

countries_df = pd.DataFrame({
    'country': ['Англия', 'Канада', 'США', 'Россия', 'Хохляндия', 'Беларусь', 'Казахстан'],
    'population': [56.29, 38.05, 322.28, 146.24, 45.5, 9.5, 17.04],
    'area': [133396, 9984670, 9826630, 17125191, 603628, 207600, 2724902]
    })
countries_df.index = ['UK', 'CA', 'US', 'RU', 'UA', 'BY', 'KZ']
print(countries_df)


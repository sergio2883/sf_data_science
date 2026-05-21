import pandas as pd
import matplotlib.pyplot as plt

covid_data = pd.read_csv(r'D:\IDE\github\sf_data_science\PY_20_Visualization\data\covid_data.csv', sep=',')
vaccinations_data = pd.read_csv(r'D:\IDE\github\sf_data_science\PY_20_Visualization\data\country_vaccinations.csv', sep=',')

covid_data = covid_data.groupby(
    ['date', 'country'], 
    as_index=False
)[['confirmed', 'deaths', 'recovered']].sum()

covid_data['date'] = pd.to_datetime(covid_data['date'])
covid_data['active'] = covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']
covid_data = covid_data.sort_values(by=['country', 'date'])
covid_data['daily_confirmed'] = covid_data.groupby('country')['confirmed'].diff()
covid_data['daily_deaths'] = covid_data.groupby('country')['deaths'].diff()
covid_data['daily_recovered'] = covid_data.groupby('country')['recovered'].diff()
print(covid_data)

vaccinations_data = vaccinations_data[
    ['country', 'date', 'total_vaccinations', 
     'people_vaccinated', 'people_vaccinated_per_hundred',
     'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred',
     'daily_vaccinations', 'vaccines']
]

vaccinations_data['date'] = pd.to_datetime(vaccinations_data['date'])
print(vaccinations_data)

# Находим период для covid_data
min_date = covid_data['date'].min()
max_date = covid_data['date'].max()

print(min_date.date(), '-', max_date.date())
print(f"{min_date.strftime('%Y-%m-%d')}-{max_date.strftime('%Y-%m-%d')}")

# Находим период для vaccinations_data
min_date_vacc = vaccinations_data['date'].min()
max_date_vacc = vaccinations_data['date'].max()

print(min_date_vacc.date(), '-', max_date_vacc.date())
print(f"{min_date_vacc.strftime('%Y-%m-%d')}-{max_date_vacc.strftime('%Y-%m-%d')}")

# Объединяем
covid_df = pd.merge(covid_data, vaccinations_data, 
                    left_on=['date', 'country'], 
                    right_on=['date', 'country'], 
                    how='left')

# Выводим размерность
rows, cols = covid_df.shape
print(f"{rows}-{cols}")

# Создаём признаки death_rate и recover_rate
covid_df['death_rate'] = (covid_df['deaths'] / covid_df['confirmed']) * 100
covid_df['recover_rate'] = (covid_df['recovered'] / covid_df['confirmed']) * 100

# Заменяем бесконечные значения (при делении на 0) на 0 или NaN
covid_df['death_rate'] = covid_df['death_rate'].replace([float('inf'), -float('inf')], 0).fillna(0)
covid_df['recover_rate'] = covid_df['recover_rate'].replace([float('inf'), -float('inf')], 0).fillna(0)

# Проверяем результат
#print(covid_df[['country', 'date', 'confirmed', 'deaths', 'recovered', 'death_rate', 'recover_rate']].head(10))

# Фильтруем данные по США
us_data = covid_df[covid_df['country'] == 'United States']

# Находим максимальную летальность
max_death_rate_us = us_data['death_rate'].max()

# Округляем до 2 знаков
result = round(max_death_rate_us, 2)

print(f"Максимальная летальность в США: {result}%")

# Фильтруем данные по России
russia_data = covid_df[covid_df['country'] == 'Russia']

# Находим средний процент выздоровевших
avg_recover_rate_russia = russia_data['recover_rate'].mean()

# Округляем до 2 знаков
result = round(avg_recover_rate_russia, 2)

print(f"Средний процент выздоровевших в России: {result}%")

grouped_cases = covid_df.groupby('date')['daily_confirmed'].sum()
# grouped_cases.plot(
#     kind='line',
#     figsize=(15, 6),
#     title='Ежедневная заболеваемость во времени',
#     grid = True,
#     lw=3
# );

# grouped_cases.plot(
#     kind='hist',
#     figsize=(10, 6),
#     title='Распределение ежедневной заболеваемости',
#     grid = True,
#     color = 'black',
#     bins=10
# );

grouped_country = covid_df.groupby(['country'])[['confirmed', 'deaths']].last()
# grouped_country = grouped_country.nlargest(10, columns=['confirmed'])
# grouped_country.plot(     kind='bar',     grid=True,     figsize=(12, 4), );

# # Сортируем по количеству умерших (по убыванию) и берём топ-10
# grouped_country = grouped_country.nlargest(10, columns=['deaths'])

# # Строим столбчатую диаграмму
# grouped_country.plot(
#     kind='bar',
#     grid=True,
#     figsize=(12, 4),
#     title='Топ-10 стран по количеству умерших (последние данные)'
# );

# plt.xlabel('Страна')
# plt.ylabel('Количество')
# plt.legend(title='Показатели', labels=['Заболевшие', 'Умершие'])
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()


covid_df.groupby(['country'])['total_vaccinations'].last().nsmallest(5).plot(kind='bar');
plt.xlabel('Страна')
plt.ylabel('Количество')
plt.legend(title='Наименьшее общее число вакцинаций на последний день периода', labels=['Вакцинации'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Показываем график
plt.show()
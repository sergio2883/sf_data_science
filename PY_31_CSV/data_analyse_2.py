import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io
import warnings
from dateutil import parser

# Игнорируем предупреждения
warnings.filterwarnings('ignore')

# Настройка страницы
st.set_page_config(
    page_title="Анализатор данных",
    page_icon="📊",
    layout="wide"
)

# Настройка оформления
st.markdown("""
    <style>
    .main-header {font-size: 2rem; font-weight: 600; color: #0066cc; text-align: center; margin-bottom: 1rem;}
    .chart-title {font-size: 18px; font-weight: 600; margin-bottom: 10px; color: #1E3A8A;}
    .stMetric {background-color: #f0f2f6; padding: 10px; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown('<div class="main-header">📊 Анализ произвольного CSV-файла с табличными данными (модуль 31)</div>', unsafe_allow_html=True)

#Функция для парсинга дат с поддержкой разных форматов
def parse_dates_flexible(series):
    """Гибкий парсинг дат с поддержкой разных форматов, включая ISO 8601"""
    def try_parse(val):
        if pd.isna(val):
            return pd.NaT
        try:
            # Если это уже datetime
            if isinstance(val, (pd.Timestamp, datetime)):
                return val
            
            val_str = str(val).strip()
            
            # Обработка ISO формата с T и Z
            if 'T' in val_str and ('Z' in val_str or '+' in val_str):
                # ISO 8601 формат
                return pd.to_datetime(val_str, format='ISO8601')
            
            # Пробуем числовой формат YYYYMMDD
            if val_str.isdigit() and len(val_str) == 8:
                return pd.to_datetime(val_str, format='%Y%m%d')
            
            # Пробуем формат с временем
            if ' ' in val_str and ':' in val_str:
                return pd.to_datetime(val_str, format='mixed')
            
            # Пробуем другие распространенные форматы
            common_formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%d.%m.%Y',
                '%Y.%m.%d',
                '%d-%m-%Y',
                '%m-%d-%Y'
            ]
            
            for fmt in common_formats:
                try:
                    return pd.to_datetime(val_str, format=fmt)
                except:
                    continue
            
            # Последняя попытка - использовать dateutil
            return parser.parse(val_str)
        except:
            return pd.NaT
    
    return series.apply(try_parse)

# Функция для безопасного преобразования в datetime
def safe_to_datetime(series):
    """Безопасное преобразование в datetime"""
    try:
        # Пробуем стандартное преобразование
        return pd.to_datetime(series, format='ISO8601', errors='coerce')
    except:
        try:
            # Пробуем с mixed форматом
            return pd.to_datetime(series, format='mixed', errors='coerce')
        except:
            # Используем гибкий парсинг
            return parse_dates_flexible(series)

# Функция для кеширования загруженных данных
@st.cache_data
def load_csv(file):
    """Загрузка CSV файла с автоматическим определением типов"""
    try:
        # Пробуем разные разделители
        for sep in [',', ';', '\t', '|']:
            try:
                df = pd.read_csv(file, sep=sep, encoding='utf-8')
                if len(df.columns) > 1:
                    # Попытка распознать даты
                    for col in df.columns:
                        if df[col].dtype == 'object':
                            # Проверяем, можно ли преобразовать в дату
                            sample = df[col].dropna().head(10)
                            if len(sample) > 0:
                                parsed = safe_to_datetime(sample)
                                if parsed.notna().sum() > len(sample) * 0.8:  # 80% успешно распознано
                                    df[col] = safe_to_datetime(df[col])
                    return df, sep
            except:
                continue
        
        # Если не получилось, пробуем с автоопределением
        df = pd.read_csv(file, encoding='utf-8')
        return df, ','
    except Exception as e:
        st.error(f"Ошибка загрузки файла: {e}")
        return None, None

# Функция для определения типа столбца
def get_column_type(col_data):
    """Определение типа столбца с улучшенной обработкой дат"""
    if pd.api.types.is_numeric_dtype(col_data):
        return "numeric"
    elif pd.api.types.is_datetime64_any_dtype(col_data):
        return "datetime"
    else:
        # Проверяем строковые даты
        sample = col_data.dropna().head(10)
        if len(sample) > 0:
            parsed = safe_to_datetime(sample)
            if parsed.notna().sum() > len(sample) * 0.8:
                return "datetime"
        return "categorical"

# Функция для статистического анализа
def calculate_statistics(df, column):
    """Расчет статистик для числового столбца"""
    data = df[column].dropna()
    if len(data) == 0:
        return None
    
    return {
        "Среднее": data.mean(),
        "Медиана": data.median(),
        "Стандартное отклонение": data.std(),
        "Минимум": data.min(),
        "Максимум": data.max(),
        "Квартиль 25%": data.quantile(0.25),
        "Квартиль 75%": data.quantile(0.75),
        "Количество": len(data),
        "Уникальных значений": data.nunique(),
        "Сумма": data.sum(),
        "Дисперсия": data.var()
    }

# Инициализация состояния сессии
if 'df' not in st.session_state:
    st.session_state.df = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
if 'column_types' not in st.session_state:
    st.session_state.column_types = {}

# Боковая панель для загрузки файла
with st.sidebar:
    st.markdown("## 📁 Загрузка данных")
    
    uploaded_file = st.file_uploader(
        "Выберите CSV файл",
        type=['csv'],
        help="Загрузите CSV файл для анализа. Поддерживаются различные разделители и кодировки."
    )
    
    if uploaded_file is not None:
        if st.session_state.file_name != uploaded_file.name:
            st.session_state.file_name = uploaded_file.name
            with st.spinner("Загрузка файла..."):
                df, separator = load_csv(uploaded_file)
                if df is not None:
                    st.session_state.df = df
                    # Обновляем типы столбцов
                    st.session_state.column_types = {col: get_column_type(df[col]) for col in df.columns}
                    st.success(f"✅ Файл загружен!\nРазмер: {df.shape[0]} строк × {df.shape[1]} столбцов")
                    #st.info(f"Разделитель: '{separator}'")
                    #st.info(f"Распознано дат: {sum(1 for t in st.session_state.column_types.values() if t == 'datetime')} столбцов")
                else:
                    st.error("Не удалось загрузить файл")
    
    # Информация о текущем файле
    if st.session_state.df is not None:
        st.markdown("---")
        st.markdown("### 📊 Информация")
        st.write(f"**Файл:** {st.session_state.file_name}")
        st.write(f"**Строк:** {st.session_state.df.shape[0]}")
        st.write(f"**Столбцов:** {st.session_state.df.shape[1]}")
        st.write(f"**Пропусков:** {st.session_state.df.isnull().sum().sum()}")
        
        # Типы данных
        with st.expander("📋 Типы столбцов"):
            type_df = pd.DataFrame({
                'Столбец': list(st.session_state.column_types.keys()),
                'Тип': list(st.session_state.column_types.values())
            })
            st.dataframe(type_df, width='stretch')

# Основная область
if st.session_state.df is not None:
    df = st.session_state.df
    column_types = st.session_state.column_types
    
    # Вкладки для разных разделов
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Данные", "📊 Статистика", "📈 Графики и диаграммы", "📐 Корреляции"])
    
    # Вкладка 1: Отображение данных
    with tab1:
        st.markdown("## 📋 Просмотр данных")
        
        # Настройка отображения
        col1, col2 = st.columns([2, 1])
        with col1:
            rows_to_show = st.slider("Количество строк для отображения", 5, 100, 10)
        with col2:
            if st.button("Показать всю таблицу"):
                rows_to_show = len(df)
        
        # Отображение таблицы
        st.dataframe(df.head(rows_to_show), width='stretch')
        
        # Информация о пропусках
        if df.isnull().sum().sum() > 0:
            with st.expander("📌 Информация о пропущенных значениях"):
                missing_df = pd.DataFrame({
                    'Столбец': df.columns,
                    'Пропуски': df.isnull().sum(),
                    'Процент': (df.isnull().sum() / len(df) * 100).round(2)
                })
                st.dataframe(missing_df[missing_df['Пропуски'] > 0], width='stretch')
    
    # Вкладка 2: Статистический анализ
    with tab2:
        st.markdown("## 📊 Статистический анализ")
        
        # Выбор столбца для анализа (только числовые)
        numeric_cols = [col for col in df.columns if column_types[col] == "numeric"]
        
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Выберите числовой столбец для анализа", numeric_cols)
            
            # Расчет статистик
            stats = calculate_statistics(df, selected_col)
            
            if stats:
                # Отображение статистик в виде метрик
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Среднее", f"{stats['Среднее']:.2f}")
                with col2:
                    st.metric("📈 Медиана", f"{stats['Медиана']:.2f}")
                with col3:
                    st.metric("📉 Стандартное отклонение", f"{stats['Стандартное отклонение']:.2f}")
                with col4:
                    st.metric("🔢 Количество значений", stats['Количество'])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("⬇️ Минимум", f"{stats['Минимум']:.2f}")
                with col2:
                    st.metric("⬆️ Максимум", f"{stats['Максимум']:.2f}")
                with col3:
                    st.metric("📐 25% квартиль", f"{stats['Квартиль 25%']:.2f}")
                with col4:
                    st.metric("📐 75% квартиль", f"{stats['Квартиль 75%']:.2f}")
                
                # Гистограмма распределения
                st.markdown('<div class="chart-title">📊 Распределение значений</div>', unsafe_allow_html=True)
                
                fig, ax = plt.subplots(figsize=(12, 5))
                n, bins, patches = ax.hist(df[selected_col].dropna(), bins=30, edgecolor='black', alpha=0.7, color='#0066cc')
                ax.set_xlabel(selected_col, fontsize=12)
                ax.set_ylabel('Частота', fontsize=12)
                ax.set_title(f'Распределение {selected_col}', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                
                # Добавляем линию среднего и медианы
                ax.axvline(stats['Среднее'], color='red', linestyle='--', linewidth=2, label=f'Среднее: {stats["Среднее"]:.2f}')
                ax.axvline(stats['Медиана'], color='green', linestyle='--', linewidth=2, label=f'Медиана: {stats["Медиана"]:.2f}')
                ax.legend()
                
                st.pyplot(fig)
                
                # Кнопка для загрузки графика
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                buf.seek(0)
                st.download_button(
                    label="📸 Скачать график распределения",
                    data=buf,
                    file_name=f"distribution_{selected_col}.png",
                    mime="image/png"
                )
                plt.close()
        else:
            st.warning("Нет числовых столбцов для статистического анализа")
    
    # Вкладка 3: Построение графиков и диаграмм
    with tab3:
        st.markdown("## 📈 Построение графиков и диаграмм")
        
        # Выбор типа графика
        chart_type = st.selectbox(
            "Выберите тип графика",
            ["Линейный график", "Диаграмма рассеяния", "Столбчатая диаграмма", "Коробчатая диаграмма"]
        )
        
        if chart_type in ["Линейный график", "Диаграмма рассеяния", "Столбчатая диаграмма"]:
            col1, col2 = st.columns(2)
            
            with col1:
                # Для оси X подходят все типы
                x_col = st.selectbox("Выберите столбец для оси X", df.columns)
            
            with col2:
                # Для оси Y подходят числовые столбцы или даты
                if chart_type == "Столбчатая диаграмма":
                    y_col = st.selectbox("Выберите столбец для оси Y", df.columns)
                else:
                    numeric_cols = [col for col in df.columns if column_types[col] == "numeric"]
                    if numeric_cols:
                        y_col = st.selectbox("Выберите числовой столбец для оси Y", numeric_cols)
                    else:
                        st.error("Нет числовых столбцов для построения графика")
                        st.stop()
            
            if st.button("Построить график", type="primary"):
                try:
                    fig, ax = plt.subplots(figsize=(12, 6))
                    
                    # Обработка оси X с безопасным преобразованием дат
                    if column_types[x_col] == "datetime":
                        x_data = safe_to_datetime(df[x_col])
                    else:
                        x_data = df[x_col]
                    
                    if chart_type == "Линейный график":
                        # Сортируем по X для линейного графика
                        if column_types[x_col] == "datetime":
                            # Для дат сортируем
                            sorted_df = df[[x_col, y_col]].dropna().sort_values(x_col)
                            x_data_sorted = sorted_df[x_col]
                            y_data_sorted = sorted_df[y_col]
                        else:
                            # Для других типов
                            sorted_idx = np.argsort(x_data) if not isinstance(x_data, pd.Series) else x_data.sort_values().index
                            x_data_sorted = x_data.iloc[sorted_idx] if isinstance(x_data, pd.Series) else np.array(x_data)[sorted_idx]
                            y_data_sorted = df[y_col].iloc[sorted_idx] if isinstance(df[y_col], pd.Series) else np.array(df[y_col])[sorted_idx]
                        
                        ax.plot(x_data_sorted, y_data_sorted, 
                               marker='o', linewidth=2, markersize=4, color='#0066cc')
                        ax.set_xlabel(x_col, fontsize=12)
                        ax.set_ylabel(y_col, fontsize=12)
                        ax.set_title(f'Линейный график: {y_col} от {x_col}', fontsize=14, fontweight='bold')
                        ax.grid(True, alpha=0.3)
                        
                        if column_types[x_col] == "datetime":
                            plt.xticks(rotation=45)
                        
                    elif chart_type == "Диаграмма рассеяния":
                        ax.scatter(x_data, df[y_col], alpha=0.6, color='#0066cc', s=30)
                        ax.set_xlabel(x_col, fontsize=12)
                        ax.set_ylabel(y_col, fontsize=12)
                        ax.set_title(f'Диаграмма рассеяния: {y_col} vs {x_col}', fontsize=14, fontweight='bold')
                        ax.grid(True, alpha=0.3)
                        
                    elif chart_type == "Столбчатая диаграмма":
                        if column_types[x_col] == "categorical" and column_types[y_col] != "numeric":
                            # Группировка по категориям
                            grouped = df.groupby(x_col).size().sort_values(ascending=False)
                            ax.bar(range(len(grouped)), grouped.values, color='#0066cc', alpha=0.7)
                            ax.set_xticks(range(len(grouped)))
                            ax.set_xticklabels(grouped.index, rotation=45, ha='right')
                            ax.set_ylabel('Количество', fontsize=12)
                            ax.set_title(f'Распределение значений по {x_col}', fontsize=14, fontweight='bold')
                        elif column_types[y_col] == "numeric":
                            if column_types[x_col] == "categorical":
                                grouped = df.groupby(x_col)[y_col].mean().sort_values(ascending=False)
                                ax.bar(range(len(grouped)), grouped.values, color='#0066cc', alpha=0.7)
                                ax.set_xticks(range(len(grouped)))
                                ax.set_xticklabels(grouped.index, rotation=45, ha='right')
                                ax.set_ylabel(f'Среднее значение {y_col}', fontsize=12)
                            else:
                                ax.bar(x_data, df[y_col], color='#0066cc', alpha=0.7, width=0.8)
                                ax.set_xlabel(x_col, fontsize=12)
                                ax.set_ylabel(y_col, fontsize=12)
                            ax.set_title(f'Столбчатая диаграмма: {y_col} от {x_col}', fontsize=14, fontweight='bold')
                        ax.grid(True, alpha=0.3, axis='y')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Кнопка для загрузки графика
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                    buf.seek(0)
                    st.download_button(
                        label="📸 Скачать график",
                        data=buf,
                        file_name=f"chart_{chart_type}_{x_col}_vs_{y_col}.png",
                        mime="image/png"
                    )
                    plt.close()
                    
                except Exception as e:
                    st.error(f"Ошибка при построении графика: {str(e)}")
                    st.info("Попробуйте выбрать другой тип графика или другие столбцы")
        
        elif chart_type == "Коробчатая диаграмма":
            # Для коробчатой диаграммы выбираем числовые столбцы
            numeric_cols = [col for col in df.columns if column_types[col] == "numeric"]
            
            if len(numeric_cols) > 0:
                selected_cols = st.multiselect("Выберите числовые столбцы для коробчатой диаграммы", numeric_cols, default=numeric_cols[:min(3, len(numeric_cols))])
                
                if selected_cols and st.button("Построить Коробчатую диаграмму", type="primary"):
                    fig, ax = plt.subplots(figsize=(12, 6))
                    data_to_plot = [df[col].dropna() for col in selected_cols]
                    bp = ax.boxplot(data_to_plot, tick_labels=selected_cols, patch_artist=True)
                    for box in bp['boxes']:
                        box.set_facecolor('#0066cc')
                        box.set_alpha(0.7)
                    ax.set_ylabel('Значения', fontsize=12)
                    ax.set_title('Коробчатая диаграмма для выбранных столбцов', fontsize=14, fontweight='bold')
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Кнопка для загрузки
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                    buf.seek(0)
                    st.download_button(
                        label="📸 Скачать Коробчатую диграмму",
                        data=buf,
                        file_name="boxplot.png",
                        mime="image/png"
                    )
                    plt.close()
            else:
                st.warning("Нет числовых столбцов для построения Коробчатой диаграммы")
    
    # Вкладка 4: Корреляционный анализ
    with tab4:
        st.markdown("## 📐 Корреляционный анализ")
        
        numeric_cols = [col for col in df.columns if column_types[col] == "numeric"]
        
        if len(numeric_cols) >= 2:
            # Выбор метода визуализации
            viz_method = st.radio("Метод визуализации", ["Тепловая карта", "Таблица"], horizontal=True)
            
            # Матрица корреляций
            corr_matrix = df[numeric_cols].corr()
            
            if viz_method == "Тепловая карта":
                fig, ax = plt.subplots(figsize=(12, 10))
                
                # Создание тепловой карты
                im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
                ax.set_xticks(range(len(numeric_cols)))
                ax.set_yticks(range(len(numeric_cols)))
                ax.set_xticklabels(numeric_cols, rotation=45, ha='right', fontsize=10)
                ax.set_yticklabels(numeric_cols, fontsize=10)
                
                # Добавление значений
                for i in range(len(numeric_cols)):
                    for j in range(len(numeric_cols)):
                        text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                      ha="center", va="center", 
                                      color="black" if abs(corr_matrix.iloc[i, j]) < 0.5 else "white",
                                      fontsize=9)
                
                plt.colorbar(im, ax=ax, label='Коэффициент корреляции', shrink=0.8)
                ax.set_title('Матрица корреляций', fontsize=16, fontweight='bold', pad=20)
                plt.tight_layout()
                st.pyplot(fig)
                
                # Кнопка для загрузки
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                buf.seek(0)
                st.download_button(
                    label="📸 Скачать матрицу корреляций",
                    data=buf,
                    file_name="correlation_matrix.png",
                    mime="image/png"
                )
                plt.close()
            else:
                st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm', vmin=-1, vmax=1), width='stretch')
            
            # Топ корреляций
            st.markdown("### 🔍 Топ корреляций")
            
            # Сбор всех пар корреляций
            corr_pairs = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr_pairs.append({
                        'Переменная 1': numeric_cols[i],
                        'Переменная 2': numeric_cols[j],
                        'Корреляция': corr_matrix.iloc[i, j],
                        'Сила': 'Сильная положительная' if corr_matrix.iloc[i, j] > 0.7 else 
                                'Средняя положительная' if corr_matrix.iloc[i, j] > 0.3 else
                                'Слабая положительная' if corr_matrix.iloc[i, j] > 0 else
                                'Сильная отрицательная' if corr_matrix.iloc[i, j] < -0.7 else
                                'Средняя отрицательная' if corr_matrix.iloc[i, j] < -0.3 else
                                'Слабая отрицательная'
                    })
            
            # Сортировка по абсолютному значению корреляции
            corr_pairs.sort(key=lambda x: abs(x['Корреляция']), reverse=True)
            
            # Отображение топ-10 корреляций
            top_corr = pd.DataFrame(corr_pairs[:10])
            st.dataframe(top_corr, width='stretch')
        else:
            st.warning(f"Для корреляционного анализа необходимо минимум 2 числовых столбца. Найдено: {len(numeric_cols)}")

else:
    # Отображение приглашения к загрузке
    st.info("Для начала анализа загрузите CSV файл с помощью боковой панели")
    
    # Возможности приложения в expander
    with st.expander("Возможности приложения", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📊 Анализ данных
            - Загрузка CSV файлов различных форматов
            - Автоматическое распознавание дат и типов данных
            - Просмотр данных в интерактивной таблице
            - Информация о пропущенных значениях
            
            #### 📈 Визуализация
            - Линейные графики
            - Диаграммы рассеяния
            - Столбчатые диаграммы
            - Коробчатая диаграмма
            """)
        
        with col2:
            st.markdown("""
            #### 📐 Статистика
            - Среднее, медиана, стандартное отклонение
            - Квартили, минимум, максимум
            - Гистограммы распределения
            - Корреляционный анализ
            
            #### 💾 Экспорт
            - Скачивание графиков в PNG
            - Экспорт результатов анализа
            """)
    
    with st.expander("📝 Пример формата CSV файла"):
        st.code("""
date,sales,product,price,category
2024-01-15,100,Product_A,10.5,Electronics
20240116,150,Product_B,15.2,Clothing
2024/01/17,120,Product_A,12.0,Electronics
15/01/2024,200,Product_C,8.5,Clothing
1975-02-23T02:58:41.000Z,300,Product_D,20.0,Electronics
        """, language="csv")
        st.info("💡 Поддерживаются различные форматы дат: ISO 8601 (с T и Z), YYYY-MM-DD, YYYYMMDD, DD/MM/YYYY и другие")

# Footer
st.markdown("---")
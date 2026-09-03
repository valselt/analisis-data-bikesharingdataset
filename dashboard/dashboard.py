import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='white')

# Menyiapkan DataFrame
def create_mean_rent_df(df):
    rent_df = df.resample(rule='D', on='dteday').agg({
        'instant': 'nunique',
        'cnt': 'mean'
    })
    rent_df = rent_df.reset_index()

    return rent_df

def create_sum_rent_df(df):
    rent_df = df.resample(rule='D', on='dteday').agg({
        'instant': 'nunique',
        'cnt': 'sum'
    })
    rent_df = rent_df.reset_index()

    return rent_df

def create_mean_rent_byseason_df(df):
    rent_by_season_df = df.groupby('season').agg({
        'instant': 'nunique',
        'cnt': 'mean'
    })
    rent_by_season_df = rent_by_season_df.reset_index()

    return rent_by_season_df

def create_sum_rent_byseason_df(df):
    rent_by_season_df = df.groupby('season').agg({
        'instant': 'nunique',
        'cnt': 'sum'
    })
    rent_by_season_df = rent_by_season_df.reset_index()

    return rent_by_season_df

def create_mean_rent_byweather_df(df):
    rent_by_weather_df = df.groupby('weathersit').agg({
        'instant': 'nunique',
        'cnt': 'mean'
    })
    rent_by_weather_df = rent_by_weather_df.reset_index()

    return rent_by_weather_df

def create_sum_rent_byweather_df(df):
    rent_by_weather_df = df.groupby('weathersit').agg({
        'instant': 'nunique',
        'cnt': 'sum'
    })
    rent_by_weather_df = rent_by_weather_df.reset_index()

    return rent_by_weather_df

def create_mean_rent_byday_df(df):
    rent_by_day_df = df.groupby('weekday').agg({
        'instant': 'nunique',
        'cnt': 'mean'
    })
    rent_by_day_df = rent_by_day_df.reset_index()

    return rent_by_day_df

def create_sum_rent_byday_df(df):
    rent_by_day_df = df.groupby('weekday').agg({
        'instant': 'nunique',
        'cnt': 'sum'
    })
    rent_by_day_df = rent_by_day_df.reset_index()

    return rent_by_day_df

def create_mean_rent_byholiday_df(df):
    rent_by_holiday_df = df.groupby('holiday').agg({
        'instant': 'nunique',
        'cnt': 'mean'
    })
    rent_by_holiday_df = rent_by_holiday_df.reset_index()

    return rent_by_holiday_df

def create_sum_rent_byholiday_df(df):
    rent_by_holiday_df = df.groupby('holiday').agg({
        'instant': 'nunique',
        'cnt': 'sum'
    })
    rent_by_holiday_df = rent_by_holiday_df.reset_index()

    return rent_by_holiday_df

day_df = pd.read_parquet("https://drive.google.com/uc?export=download&id=1AJLZjNxBFtUEuyIl6xfudDV0_GzGbdOm")
hour_df = pd.read_parquet("https://drive.google.com/uc?export=download&id=1J94M47FgF42WVNodKa_Wz_sdKI-CWiEF")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Membuat Komponen Filter

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/valselt/proyekanalisisdata_dicoding/main/rentabike-logo_convert.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    display_type = st.segmented_control(
        label="Tampilan Hasil:",
        options=["Persen", "Angka"],
        default="Persen"
    )
    formula_type = st.segmented_control(
        label="Perhitungan Hasil:",
        options=["Mean", "Sum"],
        default="Mean"
    )

main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

if formula_type == "Mean":
    daily_rent_df = create_mean_rent_df(main_day_df)
    daily_rent_byseason_df = create_mean_rent_byseason_df(main_day_df)
    daily_rent_byweather_df = create_mean_rent_byweather_df(main_day_df)
    daily_rent_byday_df = create_mean_rent_byday_df(main_day_df)
    daily_rent_byholiday_df = create_mean_rent_byholiday_df(main_day_df)
else:
    daily_rent_df = create_sum_rent_df(main_day_df)
    daily_rent_byseason_df = create_sum_rent_byseason_df(main_day_df)
    daily_rent_byweather_df = create_sum_rent_byweather_df(main_day_df)
    daily_rent_byday_df = create_sum_rent_byday_df(main_day_df)
    daily_rent_byholiday_df = create_sum_rent_byholiday_df(main_day_df)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data

st.header('Bicycle Rent Dashboard 🚲')

# -> Rent Overview

if formula_type == "Mean":
    st.subheader('Rata-rata Sewa Harian Sepeda')
else:
    st.subheader('Total Sewa Harian Sepeda')

total_rent = daily_rent_df['cnt'].sum()
st.metric(label='Total Sewa', value=f"{total_rent:,} kali")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df['dteday'], 
    daily_rent_df['cnt'],
    marker='o',
    linewidth=2,
    color='blue'
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig, dpi=500)

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# -> Rent by Season
if formula_type == "Mean":
    st.subheader('Rata-rata Sewa Harian Sepeda Berdasarkan Musim')
else:
    st.subheader('Total Sewa Harian Sepeda Berdasarkan Musim')

total_rent_all_season = daily_rent_byseason_df['cnt'].sum()
daily_rent_byseason_df['percentage'] = (daily_rent_byseason_df['cnt'] / total_rent_all_season) * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    season1_df = daily_rent_byseason_df[daily_rent_byseason_df['season'] == 1]
    if not season1_df.empty:
        if display_type == "Angka":
            result_season1 = season1_df['cnt'].values[0]
            text_result_season1 = f"{result_season1:,} kali"
        else:
            result_season1 = season1_df['percentage'].values[0]
            text_result_season1 = f"{result_season1:.1f}%"
    else:
        if display_type == "Angka":
            text_result_season1 = "0 kali"
        else:
            text_result_season1 = "0.0%"
    st.metric("Musim Semi", value=text_result_season1)



with col2:
    season2_df = daily_rent_byseason_df[daily_rent_byseason_df['season'] == 2]
    if not season2_df.empty:
        if display_type == "Angka":
            result_season2 = season2_df['cnt'].values[0]
            text_result_season2 = f"{result_season2:,} kali"
        else:
            result_season2 = season2_df['percentage'].values[0]
            text_result_season2 = f"{result_season2:.1f}%"
    else:
        if display_type == "Angka":
            text_result_season2 = "0 kali"
        else:
            text_result_season2 = "0.0%"
    st.metric("Musim Panas", value=text_result_season2)

with col3:
    season3_df = daily_rent_byseason_df[daily_rent_byseason_df['season'] == 3]
    if not season3_df.empty:
        if display_type == "Angka":
            result_season3 = season3_df['cnt'].values[0]
            text_result_season3 = f"{result_season3:,} kali"
        else:
            result_season3 = season3_df['percentage'].values[0]
            text_result_season3 = f"{result_season3:.1f}%"
    else:
        if display_type == "Angka":
            text_result_season3 = "0 kali"
        else:
            text_result_season3 = "0.0%"
    st.metric("Musim Gugur", value=text_result_season3)

with col4:
    season4_df = daily_rent_byseason_df[daily_rent_byseason_df['season'] == 4]
    if not season4_df.empty:
        if display_type == "Angka":
            result_season4 = season4_df['cnt'].values[0]
            text_result_season4 = f"{result_season4:,} kali"
        else:
            result_season4 = season4_df['percentage'].values[0]
            text_result_season4 = f"{result_season4:.1f}%"
    else:
        if display_type == "Angka":
            text_result_season4 = "0 kali"
        else:
            text_result_season4 = "0.0%"
    st.metric("Musim Dingin", value=text_result_season4)

fig, ax = plt.subplots(figsize=(16, 8))

season_mapping = {
    1: 'Semi',
    2: 'Panas',
    3: 'Gugur',
    4: 'Dingin'
}

daily_rent_byseason_df['season_category'] = daily_rent_byseason_df['season'].map(season_mapping)

sns.barplot(
    y='cnt', 
    x='season_category',
    data=daily_rent_byseason_df.sort_values(by="cnt", ascending=False),
    ax=ax,
    hue='season_category'
)

ax.set_ylabel(None)
ax.set_xlabel(None)

ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

ax.ticklabel_format(style='plain', axis='y')

st.pyplot(fig, dpi=500)

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# -> Rent by Weather Situation

if formula_type == "Mean":
    st.subheader('Rata-rata Sewa Harian Sepeda Berdasarkan Kondisi Cuaca')
else:
    st.subheader('Total Sewa Harian Sepeda Berdasarkan Kondisi Cuaca')


total_rent_all_weather = daily_rent_byweather_df['cnt'].sum()
daily_rent_byweather_df['percentage'] = (daily_rent_byweather_df['cnt'] / total_rent_all_weather) * 100 

col1, col2, col3, col4 = st.columns(4)
with col1:
    weather1_df = daily_rent_byweather_df[daily_rent_byweather_df['weathersit'] == 1]
    if not weather1_df.empty:
        if display_type == "Angka":
            result_weather1 = weather1_df['cnt'].values[0]
            text_result_weather1 = f"{result_weather1:,} kali"
        else:
            pct_weather1 = weather1_df['percentage'].values[0]
            text_result_weather1 = f"{pct_weather1:.1f}%"
    else:
        if display_type == "Angka":
            text_result_weather1 = "0 kali"
        else:
            text_result_weather1 = "0.0%"
    st.metric("Kategori 1", value=text_result_weather1)

with col2:
    weather2_df = daily_rent_byweather_df[daily_rent_byweather_df['weathersit'] == 2]
    if not weather2_df.empty:
        if display_type == "Angka":
            result_weather2 = weather2_df['cnt'].values[0]
            text_result_weather2 = f"{result_weather2:,} kali"
        else:
            pct_weather2 = weather2_df['percentage'].values[0]
            text_result_weather2 = f"{pct_weather2:.1f}%"
    else:
        if display_type == "Angka":
            text_result_weather2 = "0 kali"
        else:
            text_result_weather2 = "0.0%"
    st.metric("Kategori 2", value=text_result_weather2)
with col3:
    weather3_df = daily_rent_byweather_df[daily_rent_byweather_df['weathersit'] == 3]
    if not weather3_df.empty:
        if display_type == "Angka":
            result_weather3 = weather3_df['cnt'].values[0]
            text_result_weather3 = f"{result_weather3:,} kali"
        else:
            pct_weather3 = weather3_df['percentage'].values[0]
            text_result_weather3 = f"{pct_weather3:.1f}%"
    else:
        if display_type == "Angka":
            text_result_weather3 = "0 kali"
        else:
            text_result_weather3 = "0.0%"
    st.metric("Kategori 3", value=text_result_weather3)
with col4:
    weather4_df = daily_rent_byweather_df[daily_rent_byweather_df['weathersit'] == 4]
    if not weather4_df.empty:
        if display_type == "Angka":
            result_weather4 = weather4_df['cnt'].values[0]
            text_result_weather4 = f"{result_weather4:,} kali"
        else:
            pct_weather4 = weather4_df['percentage'].values[0]
            text_result_weather4 = f"{pct_weather4:.1f}%"
    else:
        if display_type == "Angka":
            text_result_weather4 = "0 kali"
        else:
            text_result_weather4 = "0.0%"
    st.metric("Kategori 4", value=text_result_weather4)


fig, ax = plt.subplots(figsize=(16, 8))

weathersit_mapping = {
    1: 'Kategori 1',
    2: 'Kategori 2',
    3: 'Kategori 3',
    4: 'Kategori 4'
}

daily_rent_byweather_df['weathersit_category'] = daily_rent_byweather_df['weathersit'].map(weathersit_mapping)

sns.barplot(
    y='cnt', 
    x='weathersit_category',
    data=daily_rent_byweather_df.sort_values(by="cnt", ascending=False),
    ax=ax,
    hue='weathersit_category'
)

ax.set_ylabel(None)
ax.set_xlabel(None)

ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

ax.ticklabel_format(style='plain', axis='y')

st.pyplot(fig, dpi=500)

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# -> Rent by Day of the Week

if formula_type == "Mean":
    st.subheader('Rata-rata Sewa Harian Sepeda Berdasarkan Hari dalam Seminggu')
else:
    st.subheader('Total Sewa Harian Sepeda Berdasarkan Hari dalam Seminggu')

total_rent_all_day = daily_rent_byday_df['cnt'].sum()
daily_rent_byday_df['percentage'] = (daily_rent_byday_df['cnt'] / total_rent_all_day) * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    day1_df = daily_rent_byday_df[daily_rent_byday_df['weekday'] == 0]
    if not day1_df.empty:
        if display_type == "Angka":
            result_day1 = day1_df['cnt'].values[0]
            text_result_day1 = f"{result_day1:,} kali"
        else:
            pct_day1 = day1_df['percentage'].values[0]
            text_result_day1 = f"{pct_day1:.1f}%"
    else:
        if display_type == "Angka":
            text_result_day1 = "0 kali"
        else:
            text_result_day1 = "0.0%"

    st.metric("Minggu", value=text_result_day1)

with col2:
    day2_df = daily_rent_byday_df[daily_rent_byday_df['weekday'] == 1]
    if not day2_df.empty:
        if display_type == "Angka":
            result_day2 = day2_df['cnt'].values[0]
            text_result_day2 = f"{result_day2:,} kali"
        else:
            pct_day2 = day2_df['percentage'].values[0]
            text_result_day2 = f"{pct_day2:.1f}%"
    else:
        if display_type == "Angka":
            text_result_day2 = "0 kali"
        else:
            text_result_day2 = "0.0%"
    st.metric("Senin", value=text_result_day2)

with col3:
    day3_df = daily_rent_byday_df[daily_rent_byday_df['weekday'] == 2]
    if not day3_df.empty:
        if display_type == "Angka":
            result_day3 = day3_df['cnt'].values[0]
            text_result_day3 = f"{result_day3:,} kali"
        else:
            pct_day3 = day3_df['percentage'].values[0]
            text_result_day3 = f"{pct_day3:.1f}%"
    else:
        if display_type == "Angka":
            text_result_day3 = "0 kali"
        else:
            text_result_day3 = "0.0%"
    st.metric("Selasa", value=text_result_day3)

with col4:
    day4_df = daily_rent_byday_df[daily_rent_byday_df['weekday'] == 3]
    if not day4_df.empty:
        if display_type == "Angka":
            result_day4 = day4_df['cnt'].values[0]
            text_result_day4 = f"{result_day4:,} kali"
        else:
            pct_day4 = day4_df['percentage'].values[0]
            text_result_day4 = f"{pct_day4:.1f}%"
    else:
        if display_type == "Angka":
            text_result_day4 = "0 kali"
        else:
            text_result_day4 = "0.0%"
    st.metric("Rabu", value=text_result_day4)


col5, col6, col7 = st.columns(3)

with col5:
    day5_df = daily_rent_byday_df[daily_rent_byday_df['weekday'] == 4]
    if not day5_df.empty:
        if display_type == "Angka":
            result_day5 = day5_df['cnt'].values[0]
            text_result_day5 = f"{result_day5:,} kali"
        else:
            pct_day5 = day5_df['percentage'].values[0]
            text_result_day5 = f"{pct_day5:.1f}%"
    else:
        if display_type == "Angka":
            text_result_day5 = "0 kali"
        else:
            text_result_day5 = "0.0%"
    st.metric("Kamis", value=text_result_day5)

with col6:
    day6_df = daily_rent_byday_df[daily_rent_byday_df['weekday'] == 5]
    if not day6_df.empty:
        if display_type == "Angka":
            result_day6 = day6_df['cnt'].values[0]
            text_result_day6 = f"{result_day6:,} kali"
        else:
            pct_day6 = day6_df['percentage'].values[0]
            text_result_day6 = f"{pct_day6:.1f}%"
    else:
        if display_type == "Angka":
            text_result_day6 = "0 kali"
        else:
            text_result_day6 = "0.0%"
    st.metric("Jumat", value=text_result_day6)

with col7:
    day7_df = daily_rent_byday_df[daily_rent_byday_df['weekday'] == 6]
    if not day7_df.empty:
        if display_type == "Angka":
            result_day7 = day7_df['cnt'].values[0]
            text_result_day7 = f"{result_day7:,} kali"
        else:
            pct_day7 = day7_df['percentage'].values[0]
            text_result_day7 = f"{pct_day7:.1f}%"
    else:
        if display_type == "Angka":
            text_result_day7 = "0 kali"
        else:
            text_result_day7 = "0.0%"
    st.metric("Sabtu", value=text_result_day7)

fig, ax = plt.subplots(figsize=(16, 8))

weekday_mapping = {
    0: 'Minggu',
    1: 'Senin',
    2: 'Selasa',
    3: 'Rabu',
    4: 'Kamis',
    5: 'Jumat',
    6: 'Sabtu'
}

daily_rent_byday_df['weekday_category'] = daily_rent_byday_df['weekday'].map(weekday_mapping)

sns.barplot(
    y='cnt', 
    x='weekday_category',
    data=daily_rent_byday_df.sort_values(by="cnt", ascending=False),
    ax=ax,
    hue='weekday_category'
)

ax.set_ylabel(None)
ax.set_xlabel(None)

ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

ax.ticklabel_format(style='plain', axis='y')

st.pyplot(fig, dpi=500)

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# -> Rent by Holiday

if formula_type == "Mean":
    st.subheader('Rata-rata Sewa Harian Sepeda Berdasarkan Hari Liburan')
else:
    st.subheader('Total Sewa Harian Sepeda Berdasarkan Hari Liburan')
    
total_rent_all_holiday = daily_rent_byholiday_df['cnt'].sum()
daily_rent_byholiday_df['percentage'] = (daily_rent_byholiday_df['cnt'] / total_rent_all_holiday) * 100

col1, col2 = st.columns(2)
with col1:
    holiday1_df = daily_rent_byholiday_df[daily_rent_byholiday_df['holiday'] == 0]
    if not holiday1_df.empty:
        if display_type == "Angka":
            result_holiday1 = holiday1_df['cnt'].values[0]
            text_result_holiday1 = f"{result_holiday1:,} kali"
        else:
            pct_holiday1 = holiday1_df['percentage'].values[0]
            text_result_holiday1 = f"{pct_holiday1:.1f}%"
    else:
        if display_type == "Angka":
            text_result_holiday1 = "0 kali"
        else:
            text_result_holiday1 = "0.0%"
    st.metric("Bukan Hari Libur", value=text_result_holiday1)

with col2:
    holiday2_df = daily_rent_byholiday_df[daily_rent_byholiday_df['holiday'] == 1]
    if not holiday2_df.empty:
        if display_type == "Angka":
            result_holiday2 = holiday2_df['cnt'].values[0]
            text_result_holiday2 = f"{result_holiday2:,} kali"
        else:
            pct_holiday2 = holiday2_df['percentage'].values[0]
            text_result_holiday2 = f"{pct_holiday2:.1f}%"
    else:
        if display_type == "Angka":
            text_result_holiday2 = "0 kali"
        else:
            text_result_holiday2 = "0.0%"
    st.metric("Hari Libur", value=text_result_holiday2)

fig, ax = plt.subplots(figsize=(16, 8))

holiday_mapping = {
    0: 'Bukan Hari Libur',
    1: 'Hari Libur'
}

daily_rent_byholiday_df['holiday_category'] = daily_rent_byholiday_df['holiday'].map(holiday_mapping)

sns.barplot(
    y='cnt', 
    x='holiday_category',
    data=daily_rent_byholiday_df.sort_values(by="cnt", ascending=False),
    ax=ax,
    hue='holiday_category'
)

ax.set_ylabel(None)
ax.set_xlabel(None)

ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

ax.ticklabel_format(style='plain', axis='y')

st.pyplot(fig, dpi=500)

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)


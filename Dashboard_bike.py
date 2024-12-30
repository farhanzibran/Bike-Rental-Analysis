import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load the merged data
@st.cache_data
def load_data():
    data = pd.read_csv('merged_data.csv')
    data['dteday'] = pd.to_datetime(data['dteday'])  # Convert to datetime format
    return data

merged_df = load_data()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/farhanzibran/Bike-Rental-Analysis/raw/main/logo_sepeda.png") 
# Streamlit App
st.title("Bike Data Analysis")
st.sidebar.header("Filter Options")

# Filter by Date Range
date_range = st.sidebar.date_input(
    "Select Date Range",
    [merged_df['dteday'].min(), merged_df['dteday'].max()]
)
filtered_df = merged_df[(merged_df['dteday'] >= pd.Timestamp(date_range[0])) & 
                        (merged_df['dteday'] <= pd.Timestamp(date_range[1]))]

# Filter by Hour
hour_range = st.sidebar.slider("Select Hour Range", 0, 23, (0, 23))
filtered_df = filtered_df[(filtered_df['hr'] >= hour_range[0]) & 
                          (filtered_df['hr'] <= hour_range[1])]

# Display Filtered Data
st.subheader("Filtered Data")
st.write(filtered_df)

# Plot: Penyewaan sepeda dari waktu ke waktu
st.subheader("Penyewaan sepeda dari waktu ke waktu")
time_group = st.radio("Berdasarkan", ['Hour', 'Day', 'Month'])
if time_group == 'Hour':
    data_grouped = filtered_df.groupby('hr')['cnt'].mean()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=data_grouped.index, y=data_grouped.values, palette="viridis")
    plt.title("Average Rentals by Hour")
    plt.xlabel("Hour")
    plt.ylabel("Average Rentals")
    st.pyplot(plt)
elif time_group == 'Day':
    data_grouped = filtered_df.groupby(filtered_df['dteday'].dt.date)['cnt'].sum()
    plt.figure(figsize=(10, 5))
    data_grouped.plot()
    plt.title("Total Rentals by Day")
    plt.xlabel("Day")
    plt.ylabel("Total Rentals")
    st.pyplot(plt)
else:
    data_grouped = filtered_df.groupby(filtered_df['dteday'].dt.month)['cnt'].sum()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=data_grouped.index, y=data_grouped.values, palette="viridis")
    plt.title("Total Rentals by Month")
    plt.xlabel("Month")
    plt.ylabel("Total Rentals")
    st.pyplot(plt)

# Plot: Weather Effects
st.subheader("Dampak Cuaca Terhadap penyewaan sepeda")
weather_factor = st.selectbox("Pilih faktor Cuaca", ['temp', 'hum', 'windspeed'])
plt.figure(figsize=(10, 5))
sns.scatterplot(x=filtered_df[weather_factor], y=filtered_df['cnt'], alpha=0.5, color='blue')
plt.title(f"Bike Rentals vs {weather_factor.capitalize()}")
plt.xlabel(weather_factor.capitalize())
plt.ylabel("Bike Rentals")
st.pyplot(plt)

# Distribusi penyewaan sepeda berdasarkan jenis pengguna
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Jenis Pengguna")
user_type = st.radio("Pilih Jenis Pengguna", ["Casual", "Registered", "Both"])
plt.figure(figsize=(10, 5))
if user_type == "Casual":
    sns.histplot(filtered_df['casual'], bins=30, kde=True, color='orange', label='Casual')
    plt.title("Distribusi Penyewaan Sepeda: Casual")
elif user_type == "Registered":
    sns.histplot(filtered_df['registered'], bins=30, kde=True, color='blue', label='Registered')
    plt.title("Distribusi Penyewaan Sepeda: Registered")
else:
    sns.histplot(filtered_df['casual'], bins=30, kde=True, color='orange', label='Casual', alpha=0.6)
    sns.histplot(filtered_df['registered'], bins=30, kde=True, color='blue', label='Registered', alpha=0.6)
    plt.title("Distribusi Penyewaan Sepeda: Casual dan Registered")
plt.xlabel("Jumlah Penyewaan")
plt.ylabel("Frekuensi")
plt.legend()
st.pyplot(plt)

# Korelasi antar variabel
st.subheader("Korelasi Antar Variabel")
corr = filtered_df[['temp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Heatmap Korelasi Antar Variabel")
st.pyplot(plt)

# Penyewaan sepeda berdasarkan hari dalam seminggu
st.subheader("Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
day_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
filtered_df['weekday_label'] = filtered_df['weekday'].map(day_mapping)

plt.figure(figsize=(10, 5))
sns.boxplot(x='weekday_label', y='cnt', data=filtered_df, palette='viridis')
plt.title("Jumlah Penyewaan Berdasarkan Hari")
plt.xlabel("Hari")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(plt)

# Penyewaan sepeda berdasarkan hari kerja atau libur
st.subheader("Penyewaan Sepeda Berdasarkan Hari Kerja atau Libur")
day_type = st.radio("Pilih Jenis Hari", ["Working Day", "Holiday"])
if day_type == "Working Day":
    data = filtered_df[filtered_df['workingday_x'] == 1]
    title = "Hari Kerja"
else:
    data = filtered_df[filtered_df['workingday_x'] == 0]
    title = "Hari Libur"

plt.figure(figsize=(10, 5))
sns.barplot(x=data['hr'], y=data['cnt'], ci=None, palette="coolwarm")
plt.title(f"Penyewaan Sepeda pada {title}")
plt.xlabel("Jam")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(plt)

# Conclusion Section
st.subheader("Insights")
st.write("""
- Penyewaan sepeda sangat bervariasi berdasarkan waktu, cuaca, dan jenis pengguna.
- Penyewaan lebih tinggi pada waktu-waktu tertentu (misalnya, akhir pekan, cuaca hangat) dan lebih rendah pada cuaca buruk.
- Gunakan filter di sebelah kiri untuk menjelajahi tren secara interaktif.
""")

st.caption('Copyright © Farhazibran 2024')
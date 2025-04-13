import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

data = pd.read_csv('data_khs_mahasiswa.csv')

nim_list = data[~(data['NIM'] == 2211511001)]['NIM'].unique()
semester_list = sorted(data['Semester'].unique(), key=lambda x: (int(x.split()[1]), x.split()[0]))  

st.title("Dashboard Nilai Tekom22")
st.write("Untuk memenuhi Submission saya membuat API untuk portal 2 unand berikut adalah data KHS dari mahasiswa Teknik Komputer Universitas Andalas dari 2022 hingga 2024 anda bisa melihat data KHS mahasiswa dengan memilih NIM di sidebar dan melihat data KHS mahasiswa tersebut di paling bawah ada sebaran IPK untuk semua mahasiswa Exynos22. || Tidak intensi jahat hanya ingin menyelesaikan kelas dicoding")
col1, col2 = st.columns([1, 1])
col1.write("Data yang diolah terdiri dari:")

rows, cols = data.shape
min_date = data['Semester'].min()
with col1:
    st.metric("Jumlah Baris", rows)
    st.metric("Jumlah Kolom", cols)
with col2:
    st.write("Rentang Waktu Data")
    st.write(f"{min_date} hingga {semester_list[-1]}")
with st.sidebar:
    st.image('logo.png')  
    selected_nim = st.selectbox("Pilih NIM", nim_list)
    filtered_data = data[data['NIM'] == selected_nim]


for semester in filtered_data['Semester'].unique():
    semester_data = filtered_data[filtered_data['Semester'] == semester]
    st.write(f"---")
    st.write(f"**Semester: {semester}**")
    unique_sks = semester_data.drop_duplicates(subset='Nama Mata Kuliah')['Jumlah SKS'].sum()
    if '2022' in semester and ('Ganjil' in semester or 'Genap' in semester):
        unique_sks += 4
    col1, col2 = st.columns([1, 1])
    col1.write("Informasi Semester :")
    with col1:
        st.metric("Rata-rata Nilai: ", semester_data['Nilai'].mean())
        st.metric("IP: ", semester_data['IP'].values[0])
    with col2:
        st.metric("Jumlah SKS pada Semester : ", unique_sks)

  
    simplified_table = semester_data.drop(columns=['NIM', 'IP', 'Nilai', 'Komponen Penilaian', 'Kelas', 'Semester'], errors='ignore')
    simplified_table = simplified_table.drop_duplicates(subset='Nama Mata Kuliah')
    st.markdown("**Tabel Ringkasan Mata Kuliah (Unik)**")
    st.dataframe(simplified_table)
    st.dataframe(semester_data)


st.subheader("Grafik IP per Semester")

ip_per_semester = filtered_data.groupby('Semester')['IP'].mean().reset_index()
ip_per_semester = ip_per_semester.set_index('Semester').reindex(semester_list).reset_index()
fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(x='Semester', y='IP', data=ip_per_semester, marker='o', label="IP per Semester")
ax.set_title("Grafik IP per Semester", fontsize=16)
ax.set_xlabel("Semester", fontsize=12)
ax.set_ylabel("IP", fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
ax.legend()
st.pyplot(fig)


st.subheader("Grafik Akumulasi IPK")


filtered_data_sorted = filtered_data.sort_values(by='Semester')


cumulative_ipk = []
total_ip = 0
total_semester = 0
for semester in semester_list:
    semester_data = filtered_data_sorted[filtered_data_sorted['Semester'] == semester]
    ip = semester_data['IP'].values[0]
    total_ip += ip
    total_semester += 1
    cumulative_ipk_value = total_ip / total_semester  
    cumulative_ipk.append(cumulative_ipk_value)


semester_gpa = pd.DataFrame({
    'Semester': semester_list,
    'Cumulative IPK': cumulative_ipk
})


fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(semester_gpa['Semester'], semester_gpa['Cumulative IPK'], marker='o', linestyle='-', color='b')


ax.set_title('Cumulative GPA (IPK) by Semester', fontsize=16)
ax.set_xlabel('Semester', fontsize=12)
ax.set_ylabel('Cumulative IPK', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)


st.pyplot(fig)


last_ipk = semester_gpa['Cumulative IPK'].values[-1]

total_sks = filtered_data.drop_duplicates(subset='Nama Mata Kuliah')['Jumlah SKS'].sum()
for semester in filtered_data['Semester'].unique():
    if '2022' in semester and ('Ganjil' in semester or 'Genap' in semester):
        total_sks += 4



col1, col2 = st.columns([1, 1])
    col1.write("Informasi Semester :")
    with col1:
        st.metric(f"Final IPK: {last_ipk:.2f}")
    with col2:
        st.metric("Jumlah SKS Total yang diambil : ", total_sks)

st.subheader("Sebaran IPK")


ip_final = data[['NIM', 'Semester', 'IP']].drop_duplicates(subset=['NIM', 'Semester'])


ipk_akhir = ip_final.groupby('NIM')['IP'].mean().reset_index()
ipk_akhir.rename(columns={'IP': 'IPK Akhir'}, inplace=True)


ipk_akhir['NIM'] = ipk_akhir['NIM'].astype(str)
ipk_akhir = ipk_akhir.sort_values(by='NIM', ascending=False)


fig, ax = plt.subplots(figsize=(10, len(ipk_akhir)*0.35))
sns.barplot(y='NIM', x='IPK Akhir', data=ipk_akhir, palette='Blues_d')
ax.set_title('Sebaran IPK', fontsize=14)
ax.set_xlabel('IPK Akhir')
ax.set_ylabel('NIM')
st.pyplot(fig)

st.caption("---")
st.caption("Fadhillah Rahmad Kurnia || 	MC184D5Y0386 || DBS Cooding Camp @ 2024 All Rights Reserved")

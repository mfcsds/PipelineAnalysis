import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk menghitung tegangan pada pipa
def calculate_pipe_tension(weight_per_length, length_suspended, stinger_angle):
    """
    Menghitung tegangan pada pipa.
    
    :param weight_per_length: Berat pipa per unit panjang (N/m)
    :param length_suspended: Panjang pipa yang tergantung (m)
    :param stinger_angle: Sudut stinger terhadap horizontal (derajat)
    :return: Tegangan pada pipa (N)
    """
    # Mengubah sudut dari derajat ke radian
    stinger_angle_radians = np.radians(stinger_angle)

    # Menghitung komponen vertikal dari berat pipa
    vertical_force = weight_per_length * length_suspended * np.cos(stinger_angle_radians)

    # Menghitung tegangan total pada pipa
    tension = vertical_force / np.cos(stinger_angle_radians)
    return tension

# Fungsi untuk mengevaluasi kondisi pipa
def evaluate_pipe_condition(tension, max_safe_tension):
    # ... (kode sama seperti sebelumnya)
    """
    Mengevaluasi kondisi pipa berdasarkan tegangan yang dihitung.
    
    :param tension: Tegangan pada pipa (N)
    :param max_safe_tension: Tegangan maksimum aman untuk pipa (N)
    :return: Kondisi pipa (aman atau overstress)
    """
    if tension <= max_safe_tension:
        return "Pipa dalam kondisi aman"
    else:
        return "Pipa overstress"
def calculate_tension_with_buoyancy(weight_per_length, length_suspended, stinger_angle, buoyancy_reduction, num_buoyancy_bags):
    """
    Menghitung tegangan pada pipa dengan mempertimbangkan buoyancy bag.

    :param weight_per_length: Berat pipa per unit panjang sebelum buoyancy bag (N/m)
    :param length_suspended: Panjang pipa yang tergantung (m)
    :param stinger_angle: Sudut stinger terhadap horizontal (derajat)
    :param buoyancy_reduction: Pengurangan berat per unit panjang karena buoyancy bag (N/m)
    :param num_buoyancy_bags: Jumlah buoyancy bag
    :return: Tegangan pada pipa (N)
    """
    # Menghitung berat per panjang pipa setelah mempertimbangkan buoyancy bag
    effective_weight_per_length = weight_per_length - (buoyancy_reduction * num_buoyancy_bags)

    # Menghitung tegangan pada pipa dengan berat efektif
    tension = calculate_pipe_tension(effective_weight_per_length, length_suspended, stinger_angle)
    return tension
# Fungsi utama untuk Streamlit app
def main():
    st.title("Simulasi Pemasangan Pipa Bawah Laut")

    # Sidebar untuk input parameter
    st.sidebar.title("Parameter")
    weight_per_length = st.sidebar.number_input("Berat per Panjang Pipa (N/m)", value=800, min_value=0)
    length_suspended = st.sidebar.number_input("Panjang Pipa yang Tergantung (m)", value=100, min_value=0)
    stinger_angle = st.sidebar.slider("Sudut Stinger (derajat)", 0, 90, 30)
    max_safe_tension = st.sidebar.number_input("Tegangan Maksimum Aman (N)", value=100000, min_value=0)

    # Input untuk buoyancy bag
    st.sidebar.title("Buoyancy Bag")
    buoyancy_reduction = st.sidebar.number_input("Pengurangan Berat per Bag (N/m)", value=50, min_value=0)
    num_buoyancy_bags = st.sidebar.number_input("Jumlah Buoyancy Bag", value=10, min_value=0)

    # Hitung tegangan pipa tanpa dan dengan buoyancy bag
    tension_without_buoyancy = calculate_pipe_tension(weight_per_length, length_suspended, stinger_angle)
    tension_with_buoyancy = calculate_tension_with_buoyancy(weight_per_length, length_suspended, stinger_angle, buoyancy_reduction, num_buoyancy_bags)

    # Evaluasi kondisi pipa
    pipe_condition_without_buoyancy = evaluate_pipe_condition(tension_without_buoyancy, max_safe_tension)
    pipe_condition_with_buoyancy = evaluate_pipe_condition(tension_with_buoyancy, max_safe_tension)

    # Tampilkan hasil
    st.write("## Hasil Simulasi")
    st.write(f"Tegangan tanpa Buoyancy Bag: {tension_without_buoyancy} N - {pipe_condition_without_buoyancy}")
    st.write(f"Tegangan dengan Buoyancy Bag: {tension_with_buoyancy} N - {pipe_condition_with_buoyancy}")

    # Visualisasi
    conditions = ['Tanpa Buoyancy Bag', 'Dengan Buoyancy Bag']
    tensions = [tension_without_buoyancy, tension_with_buoyancy]

    fig, ax = plt.subplots()
    sns.barplot(x=conditions, y=tensions, palette="coolwarm", ax=ax)
    ax.set_title('Perbandingan Tegangan pada Pipa')
    ax.set_xlabel('Kondisi')
    ax.set_ylabel('Tegangan (N)')
    st.pyplot(fig)

if __name__ == "__main__":
    main()

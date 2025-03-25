import csv  # Standard library untuk handling CSV
from datetime import datetime, timedelta  # Standard library untuk waktu

class JadwalKuliah:
    def __init__(self):
        self.mata_kuliah = []
        self.ruangan = {
            'A101': {'kapasitas': 30, 'fasilitas': ['proyektor', 'whiteboard']},
            'B202': {'kapasitas': 50, 'fasilitas': ['ac', 'proyektor', 'sound system']},
            'C303': {'kapasitas': 20, 'fasilitas': ['whiteboard']}
        }
        self.hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        self.jam_mulai = datetime.strptime('08:00', '%H:%M')
    
    def generate_jadwal(self):
        """Generate jadwal otomatis dengan algoritma sederhana"""
        if not self.mata_kuliah:
            print("Belum ada mata kuliah yang terdaftar!")
            return
        
        # Urutkan berdasarkan prioritas (sks terbanyak dulu)
        self.mata_kuliah.sort(key=lambda x: x['sks'], reverse=True)
        
        current_time = self.jam_mulai
        current_day = 0
        assigned_rooms = {day: [] for day in self.hari}
        
        print("\n=== HASIL PENJADWALAN ===")
        for mk in self.mata_kuliah:
            # Cari ruangan yang sesuai
            ruangan_tersedia = None
            for code, spec in self.ruangan.items():
                if (spec['kapasitas'] >= mk['kapasitas'] and 
                    all(f in spec['fasilitas'] for f in mk.get('kebutuhan_ruangan', [])) and
                    code not in assigned_rooms[self.hari[current_day]]):
                    ruangan_tersedia = code
                    break
            
            if not ruangan_tersedia:
                print(f"⚠ Tidak ada ruangan yang memenuhi untuk {mk['nama']}")
                continue
            
            # Format waktu
            end_time = current_time + timedelta(minutes=50 * mk['sks'])
            waktu_str = f"{current_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
            
            # Simpan jadwal
            mk['jadwal'] = {
                'hari': self.hari[current_day],
                'waktu': waktu_str,
                'ruangan': ruangan_tersedia
            }
            
            print(f"{mk['nama']} ({mk['sks']} SKS)")
            print(f"  ⏰ {self.hari[current_day]}, {waktu_str}")
            print(f"  🏫 Ruang {ruangan_tersedia}\n")
            
            # Update untuk next slot
            assigned_rooms[self.hari[current_day]].append(ruangan_tersedia)
            current_time = end_time + timedelta(minutes=10)
            
            # Cek jika melebihi jam operasional
            if current_time > datetime.strptime('16:00', '%H:%M'):
                current_day += 1
                current_time = self.jam_mulai
                if current_day >= len(self.hari):
                    print("❗ Jadwal sudah penuh untuk minggu ini")
                    break
    
    def tambah_matkul(self):
        """Interface untuk menambah mata kuliah"""
        print("\n🔧 Tambah Mata Kuliah Baru")
        nama = input("Nama mata kuliah: ")
        
        # Validasi SKS
        while True:
            try:
                sks = int(input("Jumlah SKS (1-4): "))
                if 1 <= sks <= 4:
                    break
                print("Masukkan angka antara 1-4!")
            except ValueError:
                print("Input harus angka!")
        
        # Validasi kapasitas
        while True:
            try:
                kapasitas = int(input("Kapasitas mahasiswa: "))
                break
            except ValueError:
                print("Input harus angka!")
        
        # Kebutuhan khusus
        kebutuhan = input("Kebutuhan ruangan (proyektor/whiteboard/ac/sound system), pisahkan koma: ")
        kebutuhan_ruangan = [k.strip() for k in kebutuhan.split(',') if k.strip()]
        
        self.mata_kuliah.append({
            'nama': nama,
            'sks': sks,
            'kapasitas': kapasitas,
            'kebutuhan_ruangan': kebutuhan_ruangan
        })
        print(f"✅ {nama} berhasil ditambahkan!")
    
def main():
    sistem = JadwalKuliah()
    
    while True:
        print("\n📚 Sistem Penjadwalan Mata Kuliah")
        print("1. Tambah Mata Kuliah")
        print("2. Generate Jadwal")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1-3): ")
        
        if pilihan == '1':
            sistem.tambah_matkul()
        elif pilihan == '2':
            sistem.generate_jadwal()
        elif pilihan == '3':
            print("Terima kasih telah menggunakan sistem!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()

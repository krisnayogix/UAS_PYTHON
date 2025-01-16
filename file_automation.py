import csv
from datetime import datetime

class AttendanceTracker:
    def __init__(self):
        self.attendance = {}

    def add_attendance(self, employee_id, check_in_datetime, check_out_datetime):
        """Menambahkan data kehadiran untuk karyawan dengan check-in dan check-out datetime."""
        self.attendance[employee_id] = {
            'check_in': check_in_datetime,
            'check_out': check_out_datetime
        }

    def generate_report(self):
        """Menghasilkan laporan kehadiran untuk semua karyawan."""
        report = []
        longest_working_employee = None
        longest_hours = 0

        for employee_id, times in self.attendance.items():
            if times['check_out']:
                check_in_date = times['check_in'].strftime("%Y-%m-%d")
                check_in_time = times['check_in'].strftime("%H:%M:%S")
                check_out_date = times['check_out'].strftime("%Y-%m-%d")
                check_out_time = times['check_out'].strftime("%H:%M:%S")
                total_hours = (times['check_out'] - times['check_in']).seconds / 3600

                # Update the longest working employee if needed
                if total_hours > longest_hours:
                    longest_hours = total_hours
                    longest_working_employee = employee_id

                report.append(f"KARYAWAN {employee_id}:")
                report.append(f"  TANGGAL CHECK-IN: {check_in_date}, JAM CHECK-IN: {check_in_time}")
                report.append(f"  TANGGAL CHECK-OUT: {check_out_date}, JAM CHECK-OUT: {check_out_time}")
                report.append(f"  TOTAL JAM KERJA: {total_hours:.2f} JAM.\n")
            else:
                report.append(f"KARYAWAN {employee_id} BELUM CHECK-OUT.\n")

        # Menambahkan informasi karyawan yang bekerja paling lama
        if longest_working_employee:
            report.append(f"KARYAWAN YANG BEKERJA PALING LAMA ADALAH KARYAWAN {longest_working_employee} DENGAN {longest_hours:.2f} JAM KERJA.\n")

        return "\n".join(report).upper()  # Mengubah seluruh laporan menjadi huruf besar

    def save_report_to_file(self, report, filename="output.txt"):
        """Menyimpan laporan ke dalam file."""
        with open(filename, 'w') as file:
            file.write(report)

    def add_manual_attendance(self):
        """Fungsi untuk menambahkan data kehadiran secara manual."""
        employee_id = int(input("Masukkan ID Karyawan: "))
        check_in_date = input("Masukkan tanggal check-in (YYYY-MM-DD): ")
        check_in_time = input("Masukkan waktu check-in (HH:MM:SS): ")
        check_out_date = input("Masukkan tanggal check-out (YYYY-MM-DD): ")
        check_out_time = input("Masukkan waktu check-out (HH:MM:SS): ")

        # Mengonversi input ke datetime
        check_in_datetime = datetime.strptime(check_in_date + " " + check_in_time, "%Y-%m-%d %H:%M:%S")
        check_out_datetime = datetime.strptime(check_out_date + " " + check_out_time, "%Y-%m-%d %H:%M:%S")

        # Menambahkan data ke dalam tracker
        self.add_attendance(employee_id, check_in_datetime, check_out_datetime)

def read_csv(file_path):
    tracker = AttendanceTracker()
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            check_in_datetime = datetime.strptime(row['check_in_date'] + " " + row['check_in_time'], "%Y-%m-%d %H:%M:%S")
            check_out_datetime = datetime.strptime(row['check_out_date'] + " " + row['check_out_time'], "%Y-%m-%d %H:%M:%S")

            # Memasukkan data ke dalam tracker tanpa filter bulan
            employee_id = int(row['employee_id'])
            tracker.add_attendance(employee_id, check_in_datetime, check_out_datetime)

    return tracker

if __name__ == "__main__":
    tracker = AttendanceTracker()

    while True:
        print("\nPilih opsi:")
        print("1. Tambahkan data kehadiran manual")
        print("2. Baca data dari file CSV")
        print("3. Generate laporan")
        print("4. Keluar")
        
        choice = input("Masukkan pilihan (1/2/3/4): ")
        
        if choice == '1':
            tracker.add_manual_attendance()
        elif choice == '2':
            file_path = input("Masukkan path file CSV: ")
            tracker = read_csv(file_path)
        elif choice == '3':
            print("\nLAPORAN KEHADIRAN KARYAWAN:")
            report = tracker.generate_report()
            print(report)
            tracker.save_report_to_file(report, "laporan_karyawan.txt")
        elif choice == '4':
            print("Keluar program.")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

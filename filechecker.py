import time
import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Konfigurasi email
smtp_server = 'smtp.gmail.com'  # Ganti dengan server SMTP Anda
smtp_port = 587  # Port SMTP Anda (587 adalah port umum untuk TLS)
smtp_username = 'Email Anda'  # Ganti dengan alamat email Anda
smtp_password = 'Sandi Anda'  # Ganti dengan kata sandi email Anda

source_folder = "Folder Sumber"  # Ganti dengan path folder sumber
destination_folder = "Folder Tujuan"  # Ganti dengan path folder tujuan
notification_recipient = "Email Penerima"  # Ganti dengan alamat email penerima notifikasi

def copy_file(source_path, destination_folder):
    # Ekstrak nama file dari path sumber
    file_name = os.path.basename(source_path)

    # Buat path tujuan dengan nama file yang sama
    destination_path = os.path.join(destination_folder, file_name)

    # Jika file sudah ada di tujuan, simpan yang lama ke folder source dengan tambahan "edited" di nama file
    if os.path.exists(destination_path):
        edited_destination_path = os.path.join(source_folder, f"edited_{file_name}")
        shutil.copy2(destination_path, edited_destination_path)
        print(f"File {file_name} disalin ke {edited_destination_path} (sebelumnya diubah)")

    # Salin file ke tujuan
    shutil.copy2(source_path, destination_path)
    print(f"File {file_name} disalin ke {destination_folder}")

    # Kirim notifikasi email bahwa file baru atau ada file yang diedit
    message = f"File {file_name} telah {'dibuat' if not os.path.exists(destination_path) else 'diubah'}."
    send_notification(message)

def send_notification(message):
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = notification_recipient
    msg['Subject'] = 'Notifikasi Tarik Data Absensi'

    body = message
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, notification_recipient, msg.as_string())
        print("Notifikasi email telah dikirim.")
    except smtplib.SMTPException as e:
        print(f"Gagal mengirim notifikasi email: {str(e)}")
    finally:
        server.quit()

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print(f'File baru terdeteksi: {event.src_path}')
        copy_file(event.src_path, destination_folder)

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'File diubah: {event.src_path}')
        copy_file(event.src_path, destination_folder)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, source_folder, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
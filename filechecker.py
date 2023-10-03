import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_folder = "D:\\cronjob\\checksys"  # Ganti dengan path folder sumber
destination_folder = "D:\\cronjob\\talenta"  # Ganti dengan path folder tujuan

def copy_file(source_path, destination_folder):
    # Ekstrak nama file dari path sumber
    file_name = os.path.basename(source_path)

    # Buat path tujuan dengan nama file yang sama
    destination_path = os.path.join(destination_folder, file_name)

    # Salin file
    shutil.copy2(source_path, destination_path)
    print(f"File {file_name} disalin ke {destination_folder}")

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

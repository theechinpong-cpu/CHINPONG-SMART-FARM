import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        # ไม่แสดงโฟลเดอร์ที่เป็น .git หรือ .github (มันเยอะ)
        if '.git' in dirs:
            dirs.remove('.git')
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

if __name__ == "__main__":
    print("--- โครงสร้างไฟล์ปัจจุบันของพี่ธี ---")
    list_files(os.getcwd())

import os

def delet(output_file):
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            print(f"已移除現有的{output_file}")
        except Exception as e:
            print("移除 {output_file} 時發生錯誤：{e}")
            return

if __name__ == "__main__":
    output_file = "./base.ogg"
    delet(output_file)
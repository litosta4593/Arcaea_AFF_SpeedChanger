import os
import sys
import shutil

def modify_speed(input_path, output_path, speed_factor):
    from arc_aff_modify_speed import aff_mod
    aff_mod(speed_factor,input_path,output_path)

def change_audio(input_file, output_file, speed_factor):
    from change_audio import change_audio
    change_audio(input_file, output_file, speed_factor)

def modify_sonlist(folder_path, speed_factor,type="chart"):
    parent_folder = os.path.dirname(folder_path)
    if os.path.exists(os.path.join(parent_folder, "songlist")):
        folder_name = os.path.basename(folder_path)
        if type == "chart":
            from songlist_mod import add_speed_variation
            if add_speed_variation(parent_folder,folder_name, speed_factor):
                print(f"成功修改songlist")
        if type == "base":
            from songlist_mod import change_base_bpm
            if change_base_bpm(parent_folder,folder_name, speed_factor):
                print(f"成功修改songlist的bpm_base")
    else:
        print("找不到songlist")
            

def process_folder(folder_path, speed_factor):
    parent_folder = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path)
    output_folder = os.path.join(parent_folder, f"{folder_name}_{speed_factor}")
    os.makedirs(output_folder, exist_ok=True)

    for i in range(4):
        aff_file = os.path.join(folder_path, f"{i}.aff")
        if os.path.exists(aff_file):
            output_file = os.path.join(output_folder, f"{i}.aff")
            modify_speed(aff_file, output_file, speed_factor)
    
    base_img_file = os.path.join(folder_path, "base.jpg")
    if os.path.exists(base_img_file):
        output_base_img_file = os.path.join(output_folder, "base.jpg")
        shutil.copy(base_img_file, output_base_img_file)
    
    base256_img_file = os.path.join(folder_path, "base_256.jpg")
    if os.path.exists(base256_img_file):
        output_base256_img_file = os.path.join(output_folder, "base_256.jpg")
        shutil.copy(base256_img_file, output_base256_img_file)

    base_ogg_file = os.path.join(folder_path, "base.ogg")
    if os.path.exists(base_ogg_file):
        output_base_ogg_file = os.path.join(output_folder, "base.ogg")
        change_audio(base_ogg_file, output_base_ogg_file, speed_factor)

    print(f"Processing completed.輸出結果到{output_folder}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run.py <speed_factor> <folder_path> [type]")
        sys.exit()

    speed_factor = float(sys.argv[1])
    folder_path = sys.argv[2]
    
    if len(sys.argv) > 3:
        type = sys.argv[3]
    else:
        type = "chart"

    modify_sonlist(folder_path, speed_factor, type)
    process_folder(folder_path, speed_factor)

    
   
    

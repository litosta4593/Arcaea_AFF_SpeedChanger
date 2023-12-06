import os
import sys

def modify_speed(input_path, output_path, speed_factor):
    cmd = f"python arc_aff_modify_speed.py {input_path} {output_path} {speed_factor}"
    os.system(cmd)

def change_audio(input_file, output_file, speed_factor):
    from change_audio import change_audio
    change_audio(input_file, output_file, speed_factor)

def process_folder(folder_path, speed_factor):
    output_folder = os.path.join(folder_path, "output")
    os.makedirs(output_folder, exist_ok=True)

    for i in range(4):
        aff_file = os.path.join(folder_path, f"{i}.aff")
        if os.path.exists(aff_file):
            output_file = os.path.join(output_folder, f"{i}_speeded.aff")
            modify_speed(aff_file, output_file, speed_factor)

    base_ogg_file = os.path.join(folder_path, "base.ogg")
    if os.path.exists(base_ogg_file):
        output_base_ogg_file = os.path.join(output_folder, "base_speeded.ogg")
        change_audio(base_ogg_file, output_base_ogg_file, speed_factor)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run.py <speed_factor> <folder_path>")
        sys.exit(1)

    speed_factor = float(sys.argv[1])
    folder_path = sys.argv[2]

    process_folder(folder_path, speed_factor)

    print("Processing completed.")

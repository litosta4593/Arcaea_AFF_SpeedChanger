import os
import sys

def timing_change(time, speed):
    return str(int(float(time) / float(speed)))

def to2(value):
    return ('%.2f' % value)

def process_timing(line, speed):
    description = line[line.find('(') + 1:line.find(')') - 1]
    parameters = description.split(",")
    return f"timing({timing_change(parameters[0], speed)},{to2(float(parameters[1]) * float(speed))},{to2(float(parameters[2]))});"

def process_note(line, speed):
    description = line[line.find('(') + 1:line.find(')')]
    parameters = description.split(",")
    return f"({timing_change(parameters[0], speed)},{parameters[1]});"

def process_hold(line, speed):
    description = line[line.find('(') + 1:line.find(')')]
    parameters = description.split(",")
    return f"hold({timing_change(parameters[0], speed)},{timing_change(parameters[1], speed)},{parameters[2]});"

def process_arc(line, speed):
    description = line[line.find('(') + 1:line.find(')') - 1]
    parameters = description.split(",")
    first_comma_index = line.find(',')
    second_comma_index = line.find(',', first_comma_index + 1)

    if line.find('[') != -1:#沒有arctap
        arctap_description = line[line.find('[') + 1:-3]
        parameters2 = arctap_description.split(",")
        arctap_after = ",".join([f"arctap({timing_change(float(b[7:-1]), speed)})" for b in parameters2])
        return f"arc({timing_change(parameters[0], speed)},{timing_change(parameters[1], speed)}{line[second_comma_index:line.find('[') + 1]}{arctap_after}];"
    else:
        return f"arc({timing_change(parameters[0], speed)},{timing_change(parameters[1], speed)}{line[second_comma_index:-1]}"

def process_scenecontrol(line, speed):
    description = line[line.find('(') + 1:line.find(')') - 1]
    parameters = description.split(",")
    first_comma_index = line.find(',')
    return f"scenecontrol({timing_change(parameters[0], speed)}{line[first_comma_index:-1]}"

def process_audio_offset(line, speed):
    parameters = line[line.find(':') + 1:-1]
    return f"AudioOffset:{timing_change(parameters, speed)}"

def get_file_path(prompt, default_path="."):
    user_input = input(f"{prompt}（留空表示使用當前路徑 '{default_path}'）：")
    if not user_input:
        return os.path.abspath(default_path)
    return os.path.abspath(user_input)

def aff_mod(speed,input_file_path,output_file_path):

    all_lines = []

    with open(input_file_path, 'r') as f:
        for line in f:
            command = line[0:line.find('(')]
            command = command.strip()
            if command == "timing":
                processed_line = process_timing(line, speed)
                all_lines.append(processed_line + "\n")
            elif command == "":
                processed_line = process_note(line, speed)
                all_lines.append(processed_line + "\n")
            elif command == "hold":
                processed_line = process_hold(line, speed)
                all_lines.append(processed_line + "\n")
            elif command == "arc":
                processed_line = process_arc(line, speed)
                all_lines.append(processed_line + "\n")
            elif command == "scenecontrol":
                processed_line = process_scenecontrol(line, speed)
                all_lines.append(processed_line + "\n")
            elif command.find('AudioOffset') != -1:
                processed_line = process_audio_offset(line, speed)
                all_lines.append(processed_line + "\n")
            else:
                all_lines.append(line)

    with open(output_file_path, 'w') as f:
        f.writelines(all_lines)

    print(f"谱面變速完成，輸出文件路徑：{output_file_path}")

def main():
    if len(sys.argv) != 4:
        print("請提供正確的參數數量。使用方法：arc_aff_modify_speed.py 輸入路徑 輸出路徑 變速倍率0.5~2")
        return

    parm1 = sys.argv[1]
    parm2 = sys.argv[2]
    speed = sys.argv[3]

    aff_mod(speed,parm1,parm2)

if __name__ == "__main__":
    main()
    

from arc_aff_modify_speed import aff_mod

input_file_path = "./test/test.aff"
output_file_path = "./test/test_out.aff"
aff_mod(0.5,input_file_path,output_file_path)

print("start check")
with open(output_file_path, 'r') as f:
        for line in f:
            command = line[0:line.find('(')]
            command = command.strip()
            if command == "timing":
                if line.strip() != "timing(0,100.00,4.00);":
                    print("timing error")
                    break
            if command == "":
                if line.strip() != "(20,1);":
                    print("note error")
                    break
            if command == "hold":
                if line.strip() != "hold(40,60,1);":
                    print("hold error")
                    break
            if command == "arc":
                if line.strip() != "arc(80,100,1.00,0.75,si,1.00,1.00,0,none,true)[arctap(82)];":
                    print("arc error")
                    break
            if command == "scenecontrol":
                line_scenecontrol = line[line.find('(')+1:line.find(')')]
                parameters = line_scenecontrol.split(",")
                features_to_check = ["trackhide","trackshow","trackdisplay","redline","arcahvdistort","arcahvdebris","hidegroup","enwidencamera","enwidenlanes"]
                expected_lines = ["scenecontrol(120,trackhide);",
                  "scenecontrol(120,trackshow);",
                  "scenecontrol(120,trackdisplay,40,1);",
                  "scenecontrol(120,redline,40,1);",
                  "scenecontrol(120,arcahvdistort,40,1);",
                  "scenecontrol(120,arcahvdebris,40,1);",
                  "scenecontrol(120,hidegroup,0,1);",
                  "scenecontrol(120,enwidencamera,40,1);",
                  "scenecontrol(120,enwidenlanes,40,1);"]
                for feature, expected_line in zip(features_to_check, expected_lines):
                    if parameters[1] == feature:
                        if line.strip() != expected_line:
                            print(f"scenecontrol {feature} error")
                            break
                
            if command == 'AudioOffset':
                if line.strip() != "AudioOffset:0":
                    print("AudioOffset error")
                    break
            if command == 'camera':
                if line.strip() != "camera(140,10,10,10,0,0,0,l,40);":
                    print("camera error")
                    break
        else:
            print("fin")

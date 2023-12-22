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
            elif command == "":
                if line.strip() != "(20,1);":
                    print("note error")
                    break
            elif command == "hold":
                if line.strip() != "hold(40,60,1);":
                    print("hold error")
                    break
            elif command == "arc":
                if line.strip() != "arc(80,100,1.00,0.75,si,1.00,1.00,0,none,true)[arctap(82)];":
                    print("arc error")
                    break
            elif command == "scenecontrol":
                if line.strip() != "scenecontrol(60,enwidencamera,20,1);":
                    print("scenecontrol error")
                    break
            elif command == 'AudioOffset':
                if line.strip() != "AudioOffset:0":
                    print("AudioOffset error")
                    break
            elif command == 'camera':
                if line.strip() != "camera(70,10,10,10,0,0,0,l,20);":
                    print("camera error")
                    break
        else:
            print("all good")

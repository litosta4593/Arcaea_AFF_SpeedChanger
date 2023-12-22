from pydub import AudioSegment
from pydub.utils import mediainfo
import os
import sys

def change_audio(input_file, output_file, speed_factor):
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            print(f"已移除現有的{output_file}")
        except Exception as e:
            print("移除 {output_file} 時發生錯誤：{e}")
            return


    audio = AudioSegment.from_ogg(input_file)

    try:
        if speed_factor > 1:
            audio = audio.speedup(playback_speed=speed_factor)
        if speed_factor < 1:
            audio = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * speed_factor)
            })
            #https://stackoverflow.com/questions/43408833/how-to-increase-decrease-playback-speed-on-wav-file
        
        original_bitrate = mediainfo(input_file)['bit_rate']
        audio.export(output_file,format="ogg",bitrate=original_bitrate)
        if speed_factor < 1:
            print(f"已將 {input_file} 放慢處理{speed_factor}倍，結果存為 {output_file}")
        if speed_factor > 1:
            print(f"已將 {input_file} 快速處理{speed_factor}倍，結果存為 {output_file}")

    except Exception as e:
        print("處理音檔時發生錯誤：{e}")
        return False
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("請提供正確的參數數量。使用方法：arc_aff_modify_speed.py 輸入路徑 輸出路徑 變速倍率0.5~2")

    input_filename = sys.argv[1]
    speed_factor = float(sys.argv[2])
    output_filename = input_filename.replace(".ogg", "_speeded.ogg")
    change_audio(input_filename, output_filename, speed_factor)

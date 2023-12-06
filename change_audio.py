from pydub import AudioSegment
import sys

def change_audio(input_file, output_file, speed_factor):

    audio = AudioSegment.from_ogg(input_file)

    if speed_factor > 1:
        audio = audio.speedup(playback_speed=speed_factor)
    if speed_factor < 1:
        audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed_factor)
    })
    #https://stackoverflow.com/questions/43408833/how-to-increase-decrease-playback-speed-on-wav-file

    audio.export(output_file, format="ogg")


def main():
    if len(sys.argv) != 3:
        print("請提供正確的參數數量。使用方法：arc_aff_modify_speed.py 輸入路徑 輸出路徑 變速倍率0.5~2")
        return

    input_filename = sys.argv[1]
    speed_factor = float(sys.argv[2])

    change_audio(input_filename, "base_speeded.ogg",speed_factor)
    if speed_factor < 1:
        print(f"已將 {input_filename} 放慢處理，結果存為 {output_filename}")
    if speed_factor > 1:
        print(f"已將 {input_filename} 快速處理，結果存為 {output_filename}")

if __name__ == "__main__":
    main()


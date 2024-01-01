import json
import copy

def load_songlist(folder_path):
    with open(f'{folder_path}/songlist', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_songlist(folder_path,data):
    with open(f'{folder_path}/songlist', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def add_speed_variation(folder_path,id, speed):
    new_id = f"{id}_{speed}"
    data = load_songlist(folder_path)

    if any(song["id"] == id for song in data["songs"]):
        if any(song["id"] == new_id for song in data["songs"]):
            print("變速歌曲id已存在songlist中")
            return False

        # 找到原始歌曲的索引
        song_index = next((index for index, song in enumerate(data["songs"]) if song["id"] == id), None)

        if song_index is not None:
            base = copy.deepcopy(data["songs"][song_index])
            base["id"] = new_id
            data["songs"].append(base)
            
    else:
        print("找到songlist，但歌曲id不存在 songlist 中")
        return False

    save_songlist(folder_path,data)
    return True

def change_base_bpm(folder_path,id, speed):
    data = load_songlist(folder_path)
    if any(song["id"] == id for song in data["songs"]):
        original_song_index = next((index for index, song in enumerate(data["songs"]) if song["id"] == id), None)
        if original_song_index is not None:
            base = data["songs"][original_song_index]
            base["bpm_base"] = '%.4f' %(float(base["bpm_base"])*speed)
            save_songlist(folder_path,data)
            return True
    else:
        print("找到songlist，但歌曲id不存在 songlist 中")
    return False



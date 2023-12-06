# Arcaea_AFF_SpeedChanger
> An Arcaea chart file modified program base on Python
# 功能
將 Arcaea譜面文件(.aff)做變速處理
![示例圖片](./img/example.jpg)
# 安裝
直接下載原碼使用
# 使用方法
使用命令行
arc_aff_modify_speed.py 輸入路徑 輸出路徑 變速倍率(0.5~2)數字越小越慢

*範例*
```bash
python arc_aff_modify_speed.py ./2.aff ./3.aff 0.5
```
# 待完成功能
- 對scenecontrol和camera變速支持
- 資料夾批量處理0~3.aff
- 音源變速
- songlist修改(改變基礎流速)
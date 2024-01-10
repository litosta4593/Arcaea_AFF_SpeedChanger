import os
import sys
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QSlider, QMessageBox, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # UI 元件初始化
        self.setWindowTitle("AFF變速工具")
        self.setGeometry(100, 100, 400, 300)

        # 鎖定視窗大小
        self.setFixedSize(400, 350)

        self.layout = QVBoxLayout()

        # 變速方式
        self.speedTypeLabel = QLabel("變速方式:")
        self.speedTypeComboBox = QComboBox()
        self.speedTypeComboBox.addItems(["譜面內容", "流速"])
        self.layout.addWidget(self.speedTypeLabel)
        self.layout.addWidget(self.speedTypeComboBox)

        # 變速內容
        self.speedContentLabel = QLabel("變速內容:")
        self.speedContentComboBox = QComboBox()
        self.speedContentComboBox.addItems(["全部", "純音樂", "純譜面"])
        self.layout.addWidget(self.speedContentLabel)
        self.layout.addWidget(self.speedContentComboBox)

        # 變速倍率
        self.speedFactorLabel = QLabel("變速倍率:")
        self.layout.addWidget(self.speedFactorLabel)
        self.speedFactorLayout = QHBoxLayout()
        self.speedFactorValueLineEdit = QLineEdit("1.0")  # 將原本的 QLabel 改成 QLineEdit
        self.speedLabelQuick  = QLabel("快")
        self.speedLabelSlow = QLabel("慢")
        self.speedFactorSlider = QSlider()
        self.speedFactorSlider.setMinimum(25)
        self.speedFactorSlider.setMaximum(300)
        self.speedFactorSlider.setValue(100)
        self.speedFactorSlider.setOrientation(1)
        self.speedFactorSlider.valueChanged.connect(self.updateSpeedFactorLabel)
        self.speedFactorLayout.addWidget(self.speedFactorValueLineEdit)
        self.speedFactorLayout.addWidget(self.speedLabelSlow)
        self.speedFactorLayout.addWidget(self.speedFactorSlider)
        self.speedFactorLayout.addWidget(self.speedLabelQuick)
        self.speedFactorLayout.setStretchFactor(self.speedFactorValueLineEdit, 1)  # 設定 QLineEdit 的 stretch factor
        self.speedFactorLayout.setStretchFactor(self.speedFactorSlider, 5)  # 設定 QSlider 的 stretch factor
        self.layout.addLayout(self.speedFactorLayout)

        # 歌曲路徑
        self.songPathLabel = QLabel("歌曲路徑:")
        self.songPathLineEdit = QLineEdit()
        self.layout.addWidget(self.songPathLabel)
        self.layout.addWidget(self.songPathLineEdit)

        # 開啟資料夾按鈕
        self.browseButton = QPushButton("開啟資料夾")
        self.browseButton.clicked.connect(self.browseFolder)
        self.layout.addWidget(self.browseButton)

        # 提示
        self.infoLabel = QLabel("")
        self.layout.addWidget(self.infoLabel)

        # 輸出按鈕
        self.outputButton = QPushButton("輸出")
        self.outputButton.clicked.connect(self.processMain)
        self.layout.addWidget(self.outputButton)

        # 主要窗口中央顯示區域
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

        # 初始化時禁用變速內容選項
        self.speedContentComboBox.setEnabled(True)

        # 設定變速方式的信號與槽
        self.speedTypeComboBox.currentTextChanged.connect(self.updateSpeedContentComboBox)
    
    def browseFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "選擇資料夾")
        if folder_path:
            # 檢查資料夾路徑是否合法
            parent_folder = os.path.dirname(folder_path)
            if os.path.exists(os.path.join(parent_folder, "songlist")):
                self.infoLabel.setText(f"找到 songlist 文件")
                self.infoLabel.setStyleSheet("color: black;") 
            else:
                self.infoLabel.setText(f"找不到 songlist ")
                self.infoLabel.setStyleSheet("color: yellow;") 
            self.songPathLineEdit.setText(folder_path)

    def processMain(self):
        speed_type = self.speedTypeComboBox.currentText()
        speed_content = self.speedContentComboBox.currentText()
        speed_factor = float(self.speedFactorValueLineEdit.text())  # 從 QLineEdit 中獲取輸入的值
        folder_path = self.songPathLineEdit.text()
        if os.path.isdir(folder_path):
            try:
                if speed_type == "譜面內容":
                    self.infoLabel.setText(f"{speed_type}{speed_content}修改中")
                    self.infoLabel.setStyleSheet("color: blue;")
                    QApplication.processEvents()
                    if speed_content == "全部":
                        audio_file_exist = os.path.exists(os.path.join(folder_path, "base.ogg"))
                        aff_files_exist = all(os.path.exists(os.path.join(folder_path, f"{i}.aff")) for i in range(4))
                        if audio_file_exist and aff_files_exist:
                            self.processFull(folder_path, speed_factor)
                        else:
                            self.infoLabel.setText(f"缺少必要檔案，無法執行變速")
                            self.infoLabel.setStyleSheet("color: red;")
                        
                    elif speed_content == "純音樂":
                        audio_file_exist = os.path.exists(os.path.join(folder_path, "base.ogg"))
                        if audio_file_exist:
                            self.changeAudio(folder_path, speed_factor)
                        else:
                            self.infoLabel.setText(f"缺少 base.ogg 檔案，無法執行變速")
                            self.infoLabel.setStyleSheet("color: red;")
                    elif speed_content == "純譜面":
                        aff_files_exist = all(os.path.exists(os.path.join(folder_path, f"{i}.aff")) for i in range(4))
                        if aff_files_exist:
                            self.processAff(folder_path, speed_factor)
                        else:
                            self.infoLabel.setText(f"缺少 0~3.aff 檔案，無法執行變速")
                            self.infoLabel.setStyleSheet("color: red;")
                    else:
                        QMessageBox.warning(self, "警告", "不支援的變速內容", QMessageBox.Ok)
                elif speed_type == "流速":
                    self.infoLabel.setText(f"{speed_type}修改中")
                    self.infoLabel.setStyleSheet("color: blue;")
                    QApplication.processEvents()
                    self.processSonglist(folder_path, speed_factor)
                else:
                    QMessageBox.warning(self, "警告", "不支援的變速方式", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"發生錯誤: {str(e)}", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "警告", "請輸入合法的資料夾路徑", QMessageBox.Ok)
    
    def updateSpeedFactorLabel(self):
        # 連接的事件，當滑軌的值改變時更新顯示目前數值的地方
        speed_factor = self.speedFactorSlider.value() / 100.0
        self.speedFactorValueLineEdit.setText(f"{speed_factor:.2f}")

    def updateSpeedContentComboBox(self):
        # 當變速方式改變時，更新變速內容選項的狀態
        speed_type = self.speedTypeComboBox.currentText()
        self.speedContentComboBox.setEnabled(speed_type != "流速")

    def changeAudio(self, folder_path, speed_factor):
        from change_audio import change_audio
        parent_folder = os.path.dirname(folder_path)
        folder_name = os.path.basename(folder_path)
        output_folder = os.path.join(parent_folder, f"{folder_name}_{speed_factor}")
        input_file = os.path.join(folder_path, "base.ogg")
        output_file = os.path.join(output_folder, "base.ogg")
        change_audio(input_file, output_file, speed_factor)
        self.infoLabel.setText(f"成功執行純音樂變速")
        self.infoLabel.setStyleSheet("color: green;")

    def processSonglist(self, folder_path, speed_factor):
        parent_folder = os.path.dirname(folder_path)
        if os.path.exists(os.path.join(parent_folder, "songlist")):
            folder_name = os.path.basename(folder_path)
            from songlist_mod import change_base_bpm
            if change_base_bpm(parent_folder, folder_name, speed_factor):
                print(f"成功修改songlist的bpm_base")
            self.infoLabel.setText(f"成功執行流速改變")
            self.infoLabel.setStyleSheet("color: green;")
        else:
            self.infoLabel.setText(f"找不到 songlist 無法執行流速改變")
            self.infoLabel.setStyleSheet("color: red;")

    def processFull(self, folder_path, speed_factor):
        from arc_aff_modify_speed import aff_mod
        parent_folder = os.path.dirname(folder_path)
        folder_name = os.path.basename(folder_path)
        output_folder = os.path.join(parent_folder, f"{folder_name}_{speed_factor}")
        os.makedirs(output_folder, exist_ok=True)

        #處理songlist
        if os.path.exists(os.path.join(parent_folder, "songlist")):
            folder_name = os.path.basename(folder_path)
            from songlist_mod import add_speed_variation
            if add_speed_variation(parent_folder,folder_name, speed_factor):
                print(f"成功修改songlist")

        for i in range(4):
            aff_file = os.path.join(folder_path, f"{i}.aff")
            if os.path.exists(aff_file):
                output_file = os.path.join(output_folder, f"{i}.aff")
                aff_mod(speed_factor, aff_file, output_file)
        
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
            from change_audio import change_audio
            change_audio(base_ogg_file, output_base_ogg_file, speed_factor)

        print(f"Processing completed.輸出結果到{output_folder}")
        self.infoLabel.setText(f"成功執行譜面變速")
        self.infoLabel.setStyleSheet("color: green;")

    def processAff(self, folder_path, speed_factor):
        from arc_aff_modify_speed import aff_mod
        parent_folder = os.path.dirname(folder_path)
        folder_name = os.path.basename(folder_path)
        output_folder = os.path.join(parent_folder, f"{folder_name}_{speed_factor}")
        os.makedirs(output_folder, exist_ok=True)

        for i in range(4):
            aff_file = os.path.join(folder_path, f"{i}.aff")
            if os.path.exists(aff_file):
                output_file = os.path.join(output_folder, f"{i}.aff")
                aff_mod(speed_factor, aff_file, output_file)
        
        print(f"Processing completed.輸出結果到{output_folder}")
        self.infoLabel.setText(f"成功執行純譜面變速")
        self.infoLabel.setStyleSheet("color: green;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # 設定視窗在畫面中央開啟
    screenGeometry = app.desktop().screenGeometry()
    x = (screenGeometry.width() - window.width()) // 2
    y = (screenGeometry.height() - window.height()) // 2
    window.move(x, y)

    window.show()
    sys.exit(app.exec_())

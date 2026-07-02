import os
import sys
from PyQt5.QtWidgets import (QTextEdit, QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QShortcut)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QKeySequence, QIcon
import pygame


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class RezeroNotepad(QMainWindow):

    def load_startup_file(self):
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_edit.setText(file.read())
            except Exception as e:
                print("Failed to open file:", e)


    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_startup_file()

    def initUI(self):
        self.dark_mode = False
        pygame.mixer.init()
        self.setWindowTitle("Re:Notepad - Writing in another Timeline")
        self.setGeometry(250, 250, 700, 400)
        self.setWindowIcon(QIcon(resource_path("rezero.ico")))

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 25, 20, 0)

        barusu = QLabel("Re:Notepad - Writing in another Timeline from Zero")
        barusu.setAlignment(Qt.AlignCenter)
        barusu.setStyleSheet("""
            font-family: 'Arial Black', Arial;
            font-size: 35px;
            font-weight: bold;
            color: hsl(74, 100%, 50%);
            letter-spacing: 1px;
            padding-bottom: 5px;
        """)

        layout.addWidget(barusu)

        self.text_edit = QTextEdit(self)
        font = self.text_edit.font()
        font.setPointSize(20)
        self.text_edit.setFont(font)
        self.text_edit.setPlaceholderText("Start Writing your timeline, BRO😉")
        self.is_saved = True

        self.text_edit.setStyleSheet("""
            font-weight: bold;
        """)


        self.setCentralWidget(container)

        self.new_btn = QPushButton("New Timeline")
        self.save_btn = QPushButton("Save Timeline")
        self.open_btn = QPushButton("Open Timeline")
        self.exit_btn = QPushButton("Leave Timeline")
        self.theme_btn = QPushButton("🌗Change Timeline Theme")

        self.word_count = QLabel("Words: 0")
        self.char_count = QLabel("Characters: 0")
        self.line_count = QLabel("Lines: 0")

        self.rbd_sound = pygame.mixer.Sound(resource_path("rbdsound.mp3"))
        self.revive_sound = pygame.mixer.Sound(resource_path("revive.mp3"))

        left_column = QVBoxLayout()
        right_column = QVBoxLayout()

        left_column.addWidget(self.new_btn)
        left_column.addWidget(self.save_btn)

        right_column.addWidget(self.open_btn)
        right_column.addWidget(self.exit_btn)
        right_column.addWidget(self.theme_btn)



        buttons = QHBoxLayout()
        buttons.addLayout(left_column)
        buttons.addLayout(right_column)
        layout.addLayout(buttons)

        self.new_btn.setMinimumHeight(50)
        self.open_btn.setMinimumHeight(50)
        self.save_btn.setMinimumHeight(50)
        self.exit_btn.setMinimumHeight(50)

        self.new_btn.setFixedSize(250, 80)
        self.open_btn.setFixedSize(250, 80)
        self.save_btn.setFixedSize(250, 80)
        self.exit_btn.setFixedSize(250, 80)
        self.theme_btn.setFixedSize(250, 80)

        self.new_btn.setStyleSheet("""
            QPushButton {
                background-color: hsl(182, 79%, 49%);
                color: black;
                font-size: 16px;
                font-family: Arial;
                font-weight: bold;
                border-radius: 12px;
                padding: 8px;
                margin: 10px;
            }
            
            QPushButton:hover {
                background-color: hsl(182, 84%, 69%);
                border: 2px solid white;
            }
        """)

        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: hsl(286, 77%, 51%);
                color: black;
                font-size: 16px;
                font-family: Arial;
                font-weight: bold;
                border-radius: 12px;
                padding: 8px;
                margin: 10px;
            }

                QPushButton:hover {
                    background-color: hsl(286, 73%, 71%);
                    border: 2px solid white;
                }
        """)

        self.open_btn.setStyleSheet("""
                    QPushButton {
                        background-color: hsl(49, 87%, 54%);
                        color: black;
                        font-size: 16px;
                        font-family: Arial;
                        font-weight: bold;
                        border-radius: 12px;
                        padding: 8px;
                        margin: 10px;
                    }

                        QPushButton:hover {
                            background-color: hsl(49, 78%, 73%);
                            border: 2px solid white;
                        }
                """)

        self.exit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: hsl(0, 85%, 53%);
                        color: black;
                        font-size: 16px;
                        font-family: Arial;
                        font-weight: bold;
                        border-radius: 12px;
                        padding: 8px;
                        margin: 10px;
                    }

                        QPushButton:hover {
                            background-color: hsl(0, 87%, 62%);
                            border: 2px solid white;
                        }
                """)
        self.theme_btn.setStyleSheet("""
                    QPushButton {
                        background-color: hsl(104, 0%, 0%);
                        color: yellow;
                        font-size: 16px;
                        font-family: Arial;
                        font-weight: bold;
                        border-radius: 12px;
                        padding: 8px;
                        margin: 10px;
                    }

                    QPushButton:hover {
                        background-color: hsl(0, 0%, 13%);
                        border: 2px solid white;
                    }
                """)



        layout.addWidget(self.text_edit)

        status_bar = QHBoxLayout()

        status_bar.addWidget(self.word_count)
        status_bar.addSpacing(10)

        status_bar.addWidget(self.char_count)
        status_bar.addSpacing(10)

        status_bar.addWidget(self.line_count)


        layout.addLayout(status_bar)


        self.new_btn.clicked.connect(self.new_file)
        self.save_btn.clicked.connect(self.save_file)
        self.open_btn.clicked.connect(self.open_file)
        self.exit_btn.clicked.connect(self.leave_timeline)
        self.text_edit.textChanged.connect(self.timeline_changed)
        self.theme_btn.clicked.connect(self.toggle_theme)

        QShortcut(QKeySequence('Ctrl+N'), self, self.new_file)
        QShortcut(QKeySequence('Ctrl+O'), self, self.open_file)
        QShortcut(QKeySequence('Ctrl+S'), self, self.save_file)
        QShortcut(QKeySequence('Ctrl+Q'), self, self.leave_timeline)
        QShortcut(QKeySequence('Ctrl+T'), self, self.toggle_theme)


    def new_file(self):
        self.revive_sound.play()
        self.text_edit.clear()

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_edit.toPlainText())
            self.is_saved = True

    def  open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_edit.setText(file.read())

    def leave_timeline(self):

        print(self.is_saved)

        msg = QMessageBox(self)

        msg.setStyleSheet("""
                    QMessageBox{
                        background-color: hsl(0, 0%, 10%)
                    }

                    QLabel{
                        color: cyan;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    
                    QPushButton {
                        background-color: #2b2b2b;
                        color: yellow;
                        border-radius: 10px;
                        padding: 8px;
                        min-width: 140px;
                        font-weight: bold;
                    }

                    QPushButton:hover {
                        background-color: crimson;
                        color: black;
                        border: 2px solid white
                    }
                """)

        msg.setWindowTitle("Return By Death?")
        msg.setText("Are u sure u want to abandon this timeline?")

        abandon_btn = msg.addButton(
            "💀Abandon Timeline",
            QMessageBox.YesRole
        )

        continue_btn = msg.addButton(
            "↻Continue Timeline",
            QMessageBox.NoRole
        )



        abandon_btn.setFixedSize(180, 45)
        continue_btn.setFixedSize(180, 45)

        self.rbd_sound.play()

        msg.exec_()

        if msg.clickedButton() == abandon_btn:
            self.close()


    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget{
                background-color: hsl(0, 0%, 12%);
                color: white;
            }
            
            QTextEdit{
                background: hsl(0, 0%, 17%);
                color: cyan;
                border: 2px solid #555;
                selection-background-color: #00bcd4;
                selection-color: black;
                caret-color: cyan;
            }
            
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 12px;
            }
            
            QScrollBar::handle:vertical {
                background: cyan;
                min-height: 20px;
                border-radius: 6px;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
                border: none;
            }
        """)

        self.word_count.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: cyan;
        """)
        self.char_count.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: cyan;
        """)
        self.line_count.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: cyan;
        """)



    def set_light_theme(self):
        self.setStyleSheet("""
            QWidget{
                background-color: white;
                color: black;
            }
            
            QTextEdit{
                background: white;
                color: black;
                border: 2px solid gray;
                selection-background-color: #00bcd4;
                selection-color: white;
                caret-color: black;
            }
            
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 12px;
            }
            
            QScrollBar::handle:vertical {
                background: black;
                min-height: 20px;
                border-radius: 6px;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
                border: none;
            }
        """)
        
        self.word_count.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: black;
        """)
        self.char_count.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: black;
        """)
        self.line_count.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: black;
        """)

    def toggle_theme(self):
        if self.dark_mode:
            self.set_light_theme()
            self.dark_mode = False

        else:
            self.set_dark_theme()
            self.dark_mode = True

    def timeline_changed(self):
        self.is_saved = False

        text = self.text_edit.toPlainText()

        words = len(text.split())
        chars = len(text)
        lines = self.text_edit.document().blockCount()

        self.word_count.setText(f"Words: {words}")
        self.char_count.setText(f"Characters: {chars}")
        self.line_count.setText(f"Lines: {lines}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = RezeroNotepad()
    notepad.show()
    sys.exit(app.exec_())




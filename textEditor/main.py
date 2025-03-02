import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox,
    QComboBox, QToolBar, QVBoxLayout, QWidget, QStatusBar, QLabel, QCheckBox
)
from PyQt5.QtGui import QFontDatabase, QFont, QTextCursor
from PyQt5.QtCore import Qt, QTimer


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)

        self.text_area = QTextEdit(self)
        self.setCentralWidget(self.text_area)

        self.current_file = None
        self.is_dark_mode = False  #  Dark mode state

        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.setup_autosave()

    def create_menu(self):
        # Creates the menu bar.# 
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.create_action("New", "Ctrl+N", self.new_file))
        file_menu.addAction(self.create_action("Open", "Ctrl+O", self.open_file))
        file_menu.addAction(self.create_action("Save", "Ctrl+S", self.save_file))
        file_menu.addAction(self.create_action("Save As", "Ctrl+Shift+S", self.save_file_as))
        file_menu.addSeparator()
        file_menu.addAction(self.create_action("Exit", "Ctrl+Q", self.close))

        view_menu = menubar.addMenu("View")
        self.dark_mode_action = self.create_action("Toggle Dark Mode", None, self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)

    def create_toolbar(self):
        # Creates a toolbar with font selection and formatting options.# 
        toolbar = QToolBar("Toolbar", self)
        self.addToolBar(toolbar)

        #  Font Selector
        self.font_selector = QComboBox(self)
        self.font_selector.setFixedWidth(200)
        self.font_selector.addItems(QFontDatabase().families())  #  Load all system fonts
        self.font_selector.currentTextChanged.connect(self.change_font)
        toolbar.addWidget(self.font_selector)

        #  Font Size Selector
        self.font_size_selector = QComboBox(self)
        self.font_size_selector.setFixedWidth(60)
        self.font_size_selector.addItems([str(i) for i in range(8, 73, 2)])  #  Sizes from 8 to 72
        self.font_size_selector.currentTextChanged.connect(self.change_font_size)
        toolbar.addWidget(self.font_size_selector)

        toolbar.addSeparator()
        toolbar.addAction(self.create_action("Bold", "Ctrl+B", self.toggle_bold))
        toolbar.addAction(self.create_action("Italic", "Ctrl+I", self.toggle_italic))
        toolbar.addAction(self.create_action("Underline", "Ctrl+U", self.toggle_underline))
        toolbar.addSeparator()
        toolbar.addAction(self.create_action("Align Left", "Ctrl+L", lambda: self.align_text(Qt.AlignLeft)))
        toolbar.addAction(self.create_action("Align Center", "Ctrl+E", lambda: self.align_text(Qt.AlignCenter)))
        toolbar.addAction(self.create_action("Align Right", "Ctrl+R", lambda: self.align_text(Qt.AlignRight)))
        toolbar.addAction(self.create_action("Justify", "Ctrl+J", lambda: self.align_text(Qt.AlignJustify)))

    def create_statusbar(self):
        # Creates a status bar with autosave info. 
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.status_label = QLabel("Autosave enabled")
        self.statusbar.addWidget(self.status_label)

    def create_action(self, name, shortcut, function):
        # Helper function to create actions with shortcuts. 
        action = QAction(name, self)
        if shortcut:
            action.setShortcut(shortcut)
        action.triggered.connect(function)
        return action

    def new_file(self):
        # Clears the editor for a new file. 
        self.text_area.clear()
        self.current_file = None
        self.setWindowTitle("New File - PyQt5 Text Editor")

    def open_file(self):
        # Opens an existing text file.
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area.setText(file.read())
            self.current_file = file_path
            self.setWindowTitle(f"{file_path} - PyQt5 Text Editor")

    def save_file(self):
        # Saves the current file. 
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.text_area.toPlainText())
        else:
            self.save_file_as()

    def save_file_as(self):
         # Saves the file with a new name.  
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.current_file = file_path
            self.save_file()
            self.setWindowTitle(f"{file_path} - PyQt5 Text Editor")

    def change_font(self, font_name):
        # Changes the font of the selected text or the text editor. 
        if font_name:
            font = self.text_area.currentFont()
            font.setFamily(font_name)
            self.text_area.setCurrentFont(font)

    def change_font_size(self, size):
        # Changes the font size of the selected text or the text editor. 
        if size.isdigit():
            font = self.text_area.currentFont()
            font.setPointSize(int(size))
            self.text_area.setCurrentFont(font)

    def toggle_bold(self):
        # Toggles bold formatting. 
        font = self.text_area.currentFont()
        font.setBold(not font.bold())
        self.text_area.setCurrentFont(font)

    def toggle_italic(self):
        # Toggles italic formatting.
        font = self.text_area.currentFont()
        font.setItalic(not font.italic())
        self.text_area.setCurrentFont(font)

    def toggle_underline(self):
        # Toggles underline formatting. 
        font = self.text_area.currentFont()
        font.setUnderline(not font.underline())
        self.text_area.setCurrentFont(font)

    def align_text(self, alignment):
        # Aligns the selected text based on the chosen alignment. 
        self.text_area.setAlignment(alignment)

    def toggle_dark_mode(self):
        # Toggles dark mode on and off. 
        if self.is_dark_mode:
            self.setStyleSheet("")
            self.text_area.setStyleSheet("")
        else:
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
            self.text_area.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.is_dark_mode = not self.is_dark_mode

    def setup_autosave(self):
        # Sets up automatic saving every 30 seconds. 
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(30000)  #  Save every 30 seconds

    def autosave(self):
        # Automatically saves the file if it has a path.# 
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.text_area.toPlainText())
            self.status_label.setText("Autosaved")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())

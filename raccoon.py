import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel, QWidget, QPlainTextEdit, QMessageBox, QLineEdit
from graph_editor import load_jsonld, save_jsonld, edit_jsonld, extract_information
import json
from graph_visualizer import draw_graph
import io
import builtins
from commands import open_file
import os

def list_jsonld_files():
    files = os.listdir('.')
    jsonld_files = [f for f in files if f.endswith('.jsonld')]
    if not jsonld_files:
        print("No JSON-LD files found in the current directory.")
    else:
        print("Available JSON-LD files:")
        for file in jsonld_files:
            print(file)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.apply_stylesheet()


    def send_terminal_input(self):
        input_text = self.terminal_input.text()[1:]  # Exclude the first character ">"
        self.terminal_widget.appendPlainText("> " + input_text)
        self.terminal_input.clear()
        self.terminal_input.setText(">")

        # Execute input command and redirect stdout
        old_stdout = sys.stdout
        redirected_stdout = io.StringIO()
        sys.stdout = redirected_stdout

        command = input_text.strip()

        try:
            if command == 'open':
                list_jsonld_files()
            elif command in dir(sys.modules[__name__]):
                func = getattr(sys.modules[__name__], command)
                if callable(func):
                    func()
                else:
                    print(f"{command} is not callable")
            else:
                exec(input_text, globals())
        except Exception as e:
            print(f"Error: {e}")

        output = redirected_stdout.getvalue()
        sys.stdout = old_stdout

        # Append output to the terminal
        self.terminal_widget.appendPlainText(output.strip())

    # UI
    def initUI(self):

        class TerminalInput(QLineEdit):
            def __init__(self, parent=None):
                super(TerminalInput, self).__init__(parent)
                self.setText(">")

            def keyPressEvent(self, event):
                if self.cursorPosition() == 0 and event.text() == "\b":
                    return
                super(TerminalInput, self).keyPressEvent(event)
                
            def focusInEvent(self, event):
                if self.cursorPosition() == 0:
                    self.setCursorPosition(1)
                super(TerminalInput, self).focusInEvent(event)
                self.setWindowTitle('Raccoon')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # Terminal Output
        self.terminal_widget = QPlainTextEdit(self)
        self.terminal_widget.setReadOnly(True)
        vbox.addWidget(self.terminal_widget)

        # Terminal Input
        self.terminal_input = TerminalInput(self)
        self.terminal_input.returnPressed.connect(self.send_terminal_input)
        vbox.addWidget(self.terminal_input)


        central_widget.setLayout(vbox)

    # theme
    def apply_stylesheet(self):
        qss = '''
            QWidget {
                background-color: #444654;
                color: #ffffff; 
            }
            
            QPushButton {
                background-color: #343541;
                border: 1px solid #343541;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            
            QPushButton:hover {
                background-color: #444654;
                border: 1px solid #343541;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            
            QPushButton:pressed {
                background-color: #444654;
                border: 1px solid #343541;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            
            QTextEdit, QPlainTextEdit {
                background-color: #000000;
                color: #ffffff;
                border: 3px solid #343541;
                border-radius: 3px;
            }

            TerminalInput {
                background-color: #000000;
                color: #ffffff;
                border: 1px solid #444654;
                border-radius: 3px;
            }

        '''


        self.setStyleSheet(qss)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
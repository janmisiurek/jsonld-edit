import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel, QWidget, QPlainTextEdit, QMessageBox, QLineEdit
from graph_editor import load_jsonld, save_jsonld, edit_jsonld, extract_information
import json
from graph_visualizer import draw_graph
import io
import builtins
from commands import open_file

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
            if command in dir(sys.modules[__name__]):
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
                self.setWindowTitle('Knowledge Graph App')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # JSON-LD Text Edit
        self.jsonld_edit = QTextEdit(self)
        hbox.addWidget(self.jsonld_edit)

        # Extracted Information Text Edit
        self.extracted_info_edit = QTextEdit(self)
        hbox.addWidget(self.extracted_info_edit)

        vbox.addLayout(hbox)


        # Load Button
        self.load_button = QPushButton('Load JSON-LD', self)
        self.load_button.clicked.connect(self.load_jsonld)
        vbox.addWidget(self.load_button)

        # Save Button
        self.save_button = QPushButton('Save JSON-LD', self)
        self.save_button.clicked.connect(self.save_jsonld)
        vbox.addWidget(self.save_button)

        # Edit Button
        self.edit_button = QPushButton('Edit JSON-LD', self)
        self.edit_button.clicked.connect(self.edit_jsonld)
        vbox.addWidget(self.edit_button)

        # Draw Graph Button
        self.draw_button = QPushButton('Draw Graph', self)
        self.draw_button.clicked.connect(self.draw_graph)
        vbox.addWidget(self.draw_button)

        # Schema Input Label
        self.schema_label = QLabel('Schema:', self)
        vbox.addWidget(self.schema_label)

        # Schema Input
        self.schema_input = QTextEdit(self)
        vbox.addWidget(self.schema_input)

        # Parse Schema Button zamienic na filtrSchema
        self.parse_schema_button = QPushButton('Parse Schema', self)
        self.parse_schema_button.clicked.connect(self.parse_schema)
        vbox.addWidget(self.parse_schema_button)

        # Extract Button
        self.extract_button = QPushButton('Extract Information', self)
        self.extract_button.clicked.connect(self.extract_information)
        vbox.addWidget(self.extract_button)

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

    def load_jsonld(self):
        global filepath
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open JSON-LD File', '', 'JSON-LD Files (*.jsonld);;All Files (*)')
        if filepath:
            jsonld_data = load_jsonld(filepath)
            self.jsonld_edit.setPlainText(jsonld_data)

    def save_jsonld(self):
        filepath, _ = QFileDialog.getSaveFileName(self, 'Save JSON-LD File', '', 'JSON-LD Files (*.jsonld);;All Files (*)')
        if filepath:
            jsonld_data = self.jsonld_edit.toPlainText()
            success = save_jsonld(filepath, jsonld_data)

    def edit_jsonld(self):
        jsonld_data = self.jsonld_edit.toPlainText()
        edited_jsonld = edit_jsonld(jsonld_data)
        self.jsonld_edit.setPlainText(edited_jsonld)

    def draw_graph(self):
        jsonld_data = self.jsonld_edit.toPlainText()
        graph_image = draw_graph(jsonld_data)
        # Display graph_image in a QLabel or other widget as needed

    def extract_information(self):
        jsonld_data = self.jsonld_edit.toPlainText()
        schema_text = self.schema_input.toPlainText()
        
        with open(filepath) as f:
            jsonld_dict = json.load(f)

        if jsonld_data and schema_text:
            try:
                schema_dict = json.loads(schema_text)

                extracted_data = extract_information(jsonld_dict, schema_dict)
                # Umieść extracted_data w polu self.extracted_info_edit
                self.extracted_info_edit.setPlainText(json.dumps(extracted_data, indent=4))
            except json.JSONDecodeError:
                QMessageBox.warning(self, 'Warning', 'Invalid JSON format in the schema input.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter JSON-LD data and a schema before extracting information.')

    def parse_schema(self):
        schema_text = self.schema_input.toPlainText()
        try:
            self.schema_dict = json.loads(schema_text)
            QMessageBox.information(self, 'Success', 'Schema parsed successfully.')
        except json.JSONDecodeError:
            QMessageBox.warning(self, 'Warning', 'Invalid JSON format in the schema input.')
            self.schema_dict = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
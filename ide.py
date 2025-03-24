import sys
import io
import contextlib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QSplitter, QInputDialog
)
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt


class PythonIDE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python IDE")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Splitter to separate editor and console
        self.splitter = QSplitter(Qt.Vertical)
        self.layout.addWidget(self.splitter)

        # Code editor (QScintilla)
        self.editor = QsciScintilla()
        self.editor.setUtf8(True)
        self.editor.setAutoIndent(True)
        self.editor.setIndentationGuides(True)
        self.editor.setIndentationsUseTabs(False)
        self.editor.setIndentationWidth(4)
        self.editor.setMarginLineNumbers(1, True)
        self.editor.setMarginWidth(1, "0000")

        # Python lexer for syntax highlighting
        self.lexer = QsciLexerPython()
        self.lexer.setDefaultColor(QColor(0, 0, 0))  # Default text color (black)
        self.lexer.setDefaultPaper(QColor(255, 255, 255))  # Background color (white)
        self.lexer.setFont(QFont("Consolas", 10))  # Set font for the lexer

        # Customize syntax highlighting colors for light theme
        self.lexer.setColor(QColor(0, 0, 255), QsciLexerPython.Keyword)  # Keywords (blue)
        self.lexer.setColor(QColor(163, 21, 21), QsciLexerPython.DoubleQuotedString)  # Double-quoted strings (red)
        self.lexer.setColor(QColor(163, 21, 21), QsciLexerPython.SingleQuotedString)  # Single-quoted strings (red)
        self.lexer.setColor(QColor(0, 128, 0), QsciLexerPython.Comment)  # Comments (green)
        self.lexer.setColor(QColor(0, 128, 0), QsciLexerPython.CommentBlock)  # Block comments (green)
        self.lexer.setColor(QColor(255, 0, 0), QsciLexerPython.Number)  # Numbers (red)

        # Set lexer to the editor
        self.editor.setLexer(self.lexer)

        # Add editor to the splitter
        self.splitter.addWidget(self.editor)

        # Console output (QTextEdit)
        self.console = QTextEdit()
        self.console.setReadOnly(True)  # Make the console read-only
        self.console.setStyleSheet("background-color: white; color: black; font-family: Consolas; font-size: 12px;")
        self.splitter.addWidget(self.console)

        # Run button
        self.run_button = QPushButton("Run Code")
        self.run_button.clicked.connect(self.run_code)
        self.layout.addWidget(self.run_button)

    def run_code(self):
        # Get the code from the editor
        code = self.editor.text()

        # Redirect stdout to capture the output
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                # Replace input() with a custom input function
                def custom_input(prompt=""):
                    self.console.append(prompt)  # Show the prompt in the console
                    input_dialog = QInputDialog(self)
                    input_dialog.setInputMode(QInputDialog.TextInput)
                    input_dialog.setWindowTitle("Input")
                    input_dialog.setLabelText(prompt)
                    if input_dialog.exec_() == QInputDialog.Accepted:
                        return input_dialog.textValue()
                    return ""  # Return empty string if canceled

                # Override the built-in input() function
                import builtins
                original_input = builtins.input
                builtins.input = custom_input

                # Execute the code
                exec(code)

                # Restore the original input() function
                builtins.input = original_input

                # Display the output
                result = output.getvalue()
                self.console.append("Code executed successfully:\n")
                self.console.append(result)
            except Exception as e:
                self.console.append(f"Error: {e}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = PythonIDE()
    ide.show()
    sys.exit(app.exec_())

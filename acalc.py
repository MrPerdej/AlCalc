import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QMenuBar, 
                            QMenu, QMessageBox, QFileDialog, QAction, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

class ACalc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ACalc")
        self.setWindowIcon(QIcon.fromTheme("accessories-calculator"))
        self.setMinimumSize(350, 450)
        
        self.kde_dark_gray = QColor(192, 192, 192)
        self.kde_medium_gray = QColor(220, 220, 220)
        self.kde_light_gray = QColor(240, 240, 240)
        self.kde_highlight = QColor(48, 150, 200)
        self.kde_button_dark = QColor(160, 160, 160)
        
        palette = QPalette()
        palette.setColor(QPalette.Window, self.kde_light_gray)
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.AlternateBase, self.kde_medium_gray)
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, self.kde_medium_gray)
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, self.kde_highlight)
        palette.setColor(QPalette.HighlightedText, Qt.white)
        QApplication.setPalette(palette)
        
        self.history = []
        self.current_expression = ""
        self.create_menu()
        self.create_ui()
        
    def create_menu(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        
        menubar.setStyleSheet("""
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 %s, stop:1 %s);
                border: 1px solid %s;
                padding: 2px;
                spacing: 3px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 3px 10px;
                border-radius: 2px;
            }
            QMenuBar::item:selected {
                background: %s;
                color: white;
            }
            QMenu {
                background-color: %s;
                border: 1px solid %s;
                padding: 1px;
            }
            QMenu::item {
                padding: 3px 25px 3px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected {
                background-color: %s;
                color: white;
                border: 1px solid %s;
            }
            QMenu::separator {
                height: 1px;
                background: %s;
                margin: 3px 5px;
            }
        """ % (self.kde_medium_gray.name(), self.kde_light_gray.name(),
               self.kde_dark_gray.name(), self.kde_highlight.name(),
               self.kde_light_gray.name(), self.kde_dark_gray.name(),
               self.kde_highlight.name(), self.kde_highlight.darker(120).name(),
               self.kde_dark_gray.name()))
        
        file_menu = menubar.addMenu("&File")
        
        save_action = QAction(QIcon.fromTheme("document-save"), "&Save History", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_history)
        file_menu.addAction(save_action)
        
        load_action = QAction(QIcon.fromTheme("document-open"), "&Load History", self)
        load_action.setShortcut("Ctrl+L")
        load_action.triggered.connect(self.load_history)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        clear_action = QAction(QIcon.fromTheme("edit-clear"), "&Clear History", self)
        clear_action.triggered.connect(self.clear_history)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(QIcon.fromTheme("application-exit"), "&Quit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction(QIcon.fromTheme("help-about"), "&About ACalc", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)
        
        display_frame = QWidget()
        display_frame.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {self.kde_dark_gray.name()};
                border-radius: 4px;
            }}
        """)
        display_layout = QVBoxLayout(display_frame)
        display_layout.setSpacing(0)
        display_layout.setContentsMargins(6, 6, 6, 6)
        
        self.expression_label = QLabel("")
        self.expression_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.expression_label.setStyleSheet("""
            QLabel {
                color: #505050;
                font-family: "Fixed";
                font-size: 14px;
                border: none;
                padding: 0 3px;
                qproperty-alignment: 'AlignRight | AlignVCenter';
            }
        """)
        
        self.result_label = QLabel("0")
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.result_label.setStyleSheet("""
            QLabel {
                color: black;
                font-family: "Fixed";
                font-size: 22px;
                font-weight: bold;
                border: none;
                padding: 0 3px;
                qproperty-alignment: 'AlignRight | AlignVCenter';
            }
        """)
        
        display_layout.addWidget(self.expression_label)
        display_layout.addWidget(self.result_label)
        layout.addWidget(display_frame)
        
        buttons_frame = QWidget()
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setSpacing(5)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        button_rows = [
            ["C", "(", ")", "/", "√"],
            ["7", "8", "9", "*", "sin"],
            ["4", "5", "6", "-", "cos"],
            ["1", "2", "3", "+", "tan"],
            ["0", ".", "π", "=", "ln"],
            ["e", "!", "^", "log", "exp"]
        ]
        
        for row in button_rows:
            hbox = QHBoxLayout()
            hbox.setSpacing(5)
            for btn_text in row:
                btn = QPushButton(btn_text)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setMinimumSize(40, 40)
                font = QFont("Helvetica", 12)
                font.setBold(True)
                btn.setFont(font)
                
                if btn_text in ["="]:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #99cc99, stop:1 #88aa88);
                            border: 2px solid {self.kde_dark_gray.name()};
                            border-radius: 4px;
                            color: black;
                        }}
                        QPushButton:pressed {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #88aa88, stop:1 #779977);
                            border: 2px inset {self.kde_dark_gray.name()};
                            padding: 2px 0px 0px 2px;
                        }}
                    """)
                elif btn_text in ["C"]:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ff9999, stop:1 #ee8888);
                            border: 2px solid {self.kde_dark_gray.name()};
                            border-radius: 4px;
                            color: black;
                        }}
                        QPushButton:pressed {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ee8888, stop:1 #dd7777);
                            border: 2px inset {self.kde_dark_gray.name()};
                            padding: 2px 0px 0px 2px;
                        }}
                    """)
                elif btn_text in ["+", "-", "*", "/", "^"]:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ffcc99, stop:1 #eebb88);
                            border: 2px solid {self.kde_dark_gray.name()};
                            border-radius: 4px;
                            color: black;
                        }}
                        QPushButton:pressed {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #eebb88, stop:1 #ddaa77);
                            border: 2px inset {self.kde_dark_gray.name()};
                            padding: 2px 0px 0px 2px;
                        }}
                    """)
                elif btn_text in ["√", "sin", "cos", "tan", "ln", "log", "exp", "!"]:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #99ccff, stop:1 #88bbee);
                            border: 2px solid {self.kde_dark_gray.name()};
                            border-radius: 4px;
                            color: black;
                        }}
                        QPushButton:pressed {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #88bbee, stop:1 #77aadd);
                            border: 2px inset {self.kde_dark_gray.name()};
                            padding: 2px 0px 0px 2px;
                        }}
                    """)
                else:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {self.kde_medium_gray.name()}, stop:1 {self.kde_dark_gray.name()});
                            border: 2px solid {self.kde_dark_gray.name()};
                            border-radius: 4px;
                            color: black;
                        }}
                        QPushButton:pressed {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {self.kde_dark_gray.name()}, stop:1 {self.kde_button_dark.name()});
                            border: 2px inset {self.kde_dark_gray.name()};
                            padding: 2px 0px 0px 2px;
                        }}
                    """)
                
                btn.clicked.connect(self.on_button_click)
                hbox.addWidget(btn)
            buttons_layout.addLayout(hbox)
        
        layout.addWidget(buttons_frame, 1)
        
    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        
        if text == "C":
            self.current_expression = ""
            self.result_label.setText("0")
            self.expression_label.setText("")
        elif text == "=":
            self.calculate_result()
        elif text == "√":
            self.current_expression += "sqrt("
            self.expression_label.setText(self.current_expression)
        elif text == "sin":
            self.current_expression += "sin("
            self.expression_label.setText(self.current_expression)
        elif text == "cos":
            self.current_expression += "cos("
            self.expression_label.setText(self.current_expression)
        elif text == "tan":
            self.current_expression += "tan("
            self.expression_label.setText(self.current_expression)
        elif text == "ln":
            self.current_expression += "log("
            self.expression_label.setText(self.current_expression)
        elif text == "log":
            self.current_expression += "log10("
            self.expression_label.setText(self.current_expression)
        elif text == "exp":
            self.current_expression += "exp("
            self.expression_label.setText(self.current_expression)
        elif text == "!":
            self.current_expression += "factorial("
            self.expression_label.setText(self.current_expression)
        elif text == "π":
            self.current_expression += str(math.pi)
            self.expression_label.setText(self.current_expression)
        elif text == "e":
            self.current_expression += str(math.e)
            self.expression_label.setText(self.current_expression)
        elif text == "^":
            self.current_expression += "**"
            self.expression_label.setText(self.current_expression)
        else:
            self.current_expression += text
            self.expression_label.setText(self.current_expression)
            
        self.calculate_partial()
        
    def calculate_partial(self):
        try:
            expression = self.current_expression
            if not expression:
                return
                
            expression = expression.replace("sqrt", "math.sqrt")
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("log", "math.log")
            expression = expression.replace("log10", "math.log10")
            expression = expression.replace("exp", "math.exp")
            expression = expression.replace("factorial", "math.factorial")
            expression = expression.replace("π", str(math.pi))
            expression = expression.replace("e", str(math.e))
            
            result = eval(expression, {"math": math, "__builtins__": None}, {})
            self.result_label.setText(str(result))
        except:
            pass
            
    def calculate_result(self):
        try:
            expression = self.current_expression
            if not expression:
                return
                
            expression = expression.replace("sqrt", "math.sqrt")
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("log", "math.log")
            expression = expression.replace("log10", "math.log10")
            expression = expression.replace("exp", "math.exp")
            expression = expression.replace("factorial", "math.factorial")
            expression = expression.replace("π", str(math.pi))
            expression = expression.replace("e", str(math.e))
            
            result = eval(expression, {"math": math, "__builtins__": None}, {})
            self.result_label.setText(str(result))
            
            self.history.append(f"{self.current_expression} = {result}")
            self.current_expression = str(result)
            self.expression_label.setText("")
        except Exception as e:
            self.result_label.setText("Error")
            
    def save_history(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save History", "", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("\n".join(self.history))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
                
    def load_history(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load History", "", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.history = f.read().splitlines()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not load file: {str(e)}")
                
    def clear_history(self):
        self.history = []
        
    def show_about(self):
        about_text = """
        <h2>ACalc</h2>
        <p>Advanced Calculator with OldSchool Interface</p>
        <p>Version beta 2.4</p>
        <p>Created for the AMNY Project</p>
        <p>Features:</p>
        <ul>
            <li>Basic and scientific operations</li>
            <li>Classic interface design</li>
            <li>Calculation history</li>
            <li>GNU OpenSource license</li>
        </ul>
        <p>© 2025 AMNY Project</p>
        """
        QMessageBox.about(self, "About ACalc", about_text)
        
    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.calculate_result()
        elif key == Qt.Key_Backspace:
            self.current_expression = self.current_expression[:-1]
            self.expression_label.setText(self.current_expression)
            self.calculate_partial()
        elif key == Qt.Key_Escape:
            self.current_expression = ""
            self.result_label.setText("0")
            self.expression_label.setText("")
        elif text in "0123456789.+-*/()":
            self.current_expression += text
            self.expression_label.setText(self.current_expression)
            self.calculate_partial()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    if QIcon.hasThemeIcon("accessories-calculator"):
        app.setWindowIcon(QIcon.fromTheme("accessories-calculator"))
    
    calculator = ACalc()
    calculator.show()
    sys.exit(app.exec_())

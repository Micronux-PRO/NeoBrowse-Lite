import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QMessageBox, QWidget, QVBoxLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QSize

class MatrixBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeoBrowse Lite")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #0f0f0f; color: #00ff00;")

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        self.homepages = {
            "index": os.path.abspath("index.html"),
            "matrix": os.path.abspath("Matrix_Homepage.html")
        }

        self.current_homepage = self.select_homepage()
        self.load_homepage(self.current_homepage)

        self.init_toolbar()

    def select_homepage(self):
        index_path = self.homepages["index"]
        matrix_path = self.homepages["matrix"]

        if os.path.exists(index_path) and os.path.getsize(index_path) > 10:
            print(f"🧠 Defaulting to index.html: {index_path}")
            return index_path
        elif os.path.exists(matrix_path):
            print(f"⚠️ index.html missing or empty. Falling back to Matrix_Homepage.html: {matrix_path}")
            return matrix_path
        else:
            print("❌ No homepage found. Generating error page.")
            return self.generate_error_page()

    def load_homepage(self, path):
        if os.path.exists(path):
            self.current_homepage = path
            url = QUrl.fromLocalFile(path)
            print(f"🔄 Loading: {url.toString()}")
            self.browser.setUrl(url)
        else:
            QMessageBox.critical(self, "Error", f"File not found:\n{path}")
            self.browser.setHtml("<h1 style='color:red;'>404: File Not Found</h1>")

    def generate_error_page(self):
        error_path = os.path.abspath("error.html")
        with open(error_path, "w") as f:
            f.write("""
                <html>
                <head><title>Error</title></head>
                <body style='background:black;color:red;text-align:center;'>
                    <h1>404: No homepage found</h1>
                    <p>Neither index.html nor Matrix_Homepage.html could be loaded.</p>
                </body>
                </html>
            """)
        return error_path

    def init_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #1a1a1a;
                spacing: 10px;
                padding: 5px;
            }
            QToolButton {
                color: #00ff00;
                padding: 6px;
                margin-right: 10px;
                font-weight: bold;
            }
        """)
        self.addToolBar(toolbar)

        def add_action(name, path):
            action = QAction(name, self)
            action.triggered.connect(lambda: self.load_homepage(path))
            toolbar.addAction(action)

        add_action("Load index.html", self.homepages["index"])
        add_action("Load Matrix_Homepage.html", self.homepages["matrix"])
        add_action("Reload Current", self.current_homepage)

        toolbar.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)
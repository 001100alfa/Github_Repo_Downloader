#!/usr/bin/env python3
import sys
import os
import subprocess
import requests

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QFileDialog, QToolBar, QAction, QWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

API_URL = "https://api.github.com/search/repositories"

DARK_STYLE = """
QMainWindow {
    background-color: #2b2b2b;
    color: #ffffff;
}
QLabel, QLineEdit, QListWidget, QPushButton {
    background-color: #3c3f41;
    color: #ffffff;
}
QLineEdit, QListWidget {
    border: 1px solid #555;
}
QPushButton {
    border: 1px solid #555;
    padding: 5px;
}
QListWidget::item {
    padding: 5px;
}
"""

class GitHubSearchThread(QThread):
    results_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        params = {"q": self.query, "per_page": 50}
        try:
            response = requests.get(API_URL, params=params)
            if response.status_code != 200:
                self.error_occurred.emit(f"API Hatası: {response.status_code} - {response.reason}")
                return
            data = response.json()
            items = data.get("items", [])
            results = []
            for item in items:
                results.append({
                    "full_name": item.get("full_name"),
                    "clone_url": item.get("clone_url"),
                    "description": item.get("description") or "",
                    "stars": item.get("stargazers_count", 0)
                })
            self.results_ready.emit(results)
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub Repo Downloader")
        self.setGeometry(100, 100, 800, 600)
        self.dark_theme_active = False
        self.search_thread = None

        # Üst bar: Toolbar oluşturuluyor ve Dark Theme butonu ekleniyor.
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        self.theme_action = QAction("Dark Theme", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_action)

        # Arama kriteri için etiket ve text alanı
        self.search_label = QLabel("Arama Sorgusu:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("örn. language:python")

        # Sonuçları gösterecek liste
        self.results_list = QListWidget()

        # Dizin seçimi butonu
        self.dir_button = QPushButton("İndirilecek Dizin Seç")
        self.dir_button.clicked.connect(self.select_directory)
        self.download_dir = os.getcwd()  # Varsayılan olarak mevcut dizin
        self.dir_label = QLabel(f"İndirilecek Dizin: {self.download_dir}")

        # Arama ve İndirme butonları
        self.search_button = QPushButton("Ara")
        self.search_button.clicked.connect(self.start_search)
        self.select_all_button = QPushButton("Tümünü Seç")
        self.select_all_button.clicked.connect(self.select_all)
        self.download_button = QPushButton("Seçilenleri İndir")
        self.download_button.clicked.connect(self.download_selected)

        # Durum mesajı etiketi
        self.status_label = QLabel("Hazır.")

        # Layout düzenlemesi
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.search_label)
        top_layout.addWidget(self.search_edit)

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.dir_button)
        dir_layout.addWidget(self.dir_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.select_all_button)
        button_layout.addWidget(self.download_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(dir_layout)
        main_layout.addWidget(self.results_list)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def toggle_theme(self):
        if self.dark_theme_active:
            self.setStyleSheet("")
            self.dark_theme_active = False
            self.theme_action.setText("Dark Theme")
        else:
            self.setStyleSheet(DARK_STYLE)
            self.dark_theme_active = True
            self.theme_action.setText("Light Theme")

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "İndirilecek Dizin Seç", os.getcwd())
        if directory:
            self.download_dir = directory
            self.dir_label.setText(f"İndirilecek Dizin: {self.download_dir}")

    def start_search(self):
        query_input = self.search_edit.text().strip()
        if not query_input:
            QMessageBox.warning(self, "Hata", "Lütfen bir arama sorgusu giriniz.")
            return
        # "stars:>100" koşulunu sorguya ekleme
        query = f"{query_input} stars:>100"
        self.results_list.clear()
        self.status_label.setText("Arama yapılıyor...")
        self.search_button.setEnabled(False)
        self.download_button.setEnabled(False)
        self.select_all_button.setEnabled(False)
        self.search_thread = GitHubSearchThread(query)
        self.search_thread.results_ready.connect(self.display_results)
        self.search_thread.error_occurred.connect(self.search_error)
        self.search_thread.start()

    def display_results(self, results):
        self.search_button.setEnabled(True)
        self.download_button.setEnabled(True)
        self.select_all_button.setEnabled(True)
        self.status_label.setText(f"{len(results)} sonuç bulundu.")
        for result in results:
            item = QListWidgetItem()
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setText(f"{result['full_name']} - ★ {result['stars']} \n{result['description']}")
            item.setData(Qt.UserRole, result)
            self.results_list.addItem(item)

    def search_error(self, error_message):
        self.search_button.setEnabled(True)
        self.select_all_button.setEnabled(True)
        self.status_label.setText("Arama hatası oluştu.")
        QMessageBox.critical(self, "Arama Hatası", error_message)

    def select_all(self):
        count = self.results_list.count()
        for index in range(count):
            item = self.results_list.item(index)
            item.setCheckState(Qt.Checked)

    def download_selected(self):
        count = self.results_list.count()
        if count == 0:
            QMessageBox.information(self, "Bilgi", "İndirilecek repo bulunamadı.")
            return
        selected_items = []
        for index in range(count):
            item = self.results_list.item(index)
            if item.checkState() == Qt.Checked:
                selected_items.append(item)
        if not selected_items:
            QMessageBox.information(self, "Bilgi", "Lütfen indirilecek repoları seçiniz.")
            return

        for item in selected_items:
            repo_data = item.data(Qt.UserRole)
            clone_url = repo_data.get("clone_url")
            self.status_label.setText(f"Klonlanıyor: {repo_data.get('full_name')} ...")
            QApplication.processEvents()
            try:
                subprocess.run(["git", "clone", clone_url], cwd=self.download_dir, check=True)
            except subprocess.CalledProcessError as e:
                QMessageBox.warning(self, "Klonlama Hatası", f"{repo_data.get('full_name')} klonlanamadı: {e}")
        self.status_label.setText("Seçilen repolar klonlandı.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
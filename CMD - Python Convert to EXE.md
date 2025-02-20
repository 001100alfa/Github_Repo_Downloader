open --> CMD

pip install pyinstaller

pyinstaller --onefile Github_Repo_Downloader.py

pyinstaller --noconsole --onefile --icon=github.ico --name Github_Repo_Downloader.exe Github_Repo_Downloader.py

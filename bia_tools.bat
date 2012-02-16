    set PIP=C:\Python27\pyinstaller-1.5.1\
    python %PIP%pyinstaller.py --onefile --console --name pak_magick -p src\ src\pak_magick.py
    python %PIP%pyinstaller.py --onefile --console --name ctx_magick -p src\ src\ctx_magick.py
    python %PIP%pyinstaller.py --onefile --console --name find_pkle -p src\ src\find_pkle.py


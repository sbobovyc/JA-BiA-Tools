    set PIP=C:\Python27\pyinstaller-1.5.1\
    set ICON=.\misc\jabia_icon.ico
    set ICON1=.\misc\pak_icon.ico
    set ICON2=.\misc\ctx_icon.ico
    set ICON3=.\misc\pkle_icon.ico
    set ICON4=.\misc\deg_icon.ico
    python %PIP%pyinstaller.py --onefile --console --icon %ICON1% --name pak_magick -p src\ src\pak_magick.py
    python %PIP%pyinstaller.py --onefile --console --icon %ICON2% --name ctx_magick -p src\ src\ctx_magick.py
    python %PIP%pyinstaller.py --onefile --console --icon %ICON3% --name find_pkle -p src\ src\find_pkle.py
    python %PIP%pyinstaller.py --onefile --console --icon %ICON4% --name deg_magick -p src\ src\deg_magick.py

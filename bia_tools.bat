    set PIP=C:\Python27\pyinstaller-3.1\
    set UPX_PATH=C:\upx391w
    set ICON=.\misc\jabia_icon.ico
    set ICON1=.\misc\pak_icon.ico
    set ICON2=.\misc\ctx_icon.ico
    set ICON3=.\misc\vtp_icon.ico
    set ICON4=.\misc\deg_icon.ico
    set ICON5=.\misc\cui_icon.ico
    python %PIP%pyinstaller.py --upx-dir=%UPX_PATH% --onefile --console --icon %ICON1% --name pak_magick -p src\ src\pak_magick.py
    python %PIP%pyinstaller.py --upx-dir=%UPX_PATH% --onefile --console --icon %ICON2% --name ctx_magick -p src\ src\ctx_magick.py
    python %PIP%pyinstaller.py --upx-dir=%UPX_PATH% --onefile --console --icon %ICON3% --name vtp_magick -p src\ src\vtp_magick.py
    python %PIP%pyinstaller.py --upx-dir=%UPX_PATH% --onefile --console --icon %ICON4% --name deg_magick -p src\ src\deg_magick.py
    python %PIP%pyinstaller.py --upx-dir=%UPX_PATH% --onefile --console --icon %ICON5% --name cui_magick -p src\ src\cui_magick.py
    REM python %PIP%pyinstaller.py --onefile --console --name crf2obj -p src\ src\crf2obj.py
    REM python %PIP%pyinstaller.py -upx-dir=%UPX_PATH% --onefile --console --name jabia_wizard -p src\experimental src\experimental\jabia_wizard.py
    REM python %PIP%pyinstaller.py --upx-dir=%UPX_PATH% --onefile --console --icon %ICON3% --name find_pkle -p src\ src\find_pkle.py

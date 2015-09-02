PIP=/c/Python27/pyinstaller-2.1
UPX_PATH=/c/upx391w

ICON=./misc/jabia_icon.ico
ICON1=./misc/pak_icon.ico
ICON2=./misc/ctx_icon.ico
ICON3=./misc/vtp_icon.ico
ICON4=./misc/deg_icon.ico
ICON5=./misc/cui_icon.ico

TEMP=./tmp

.PHONY: all
all: pak ctx vtp deg cui wizard

pak:
	python $(PIP)/pyinstaller.py --upx-dir=$(UPX_PATH) --onefile --console --icon $(ICON1) --name pak_magick -p src/ src/pak_magick.py
ctx:
	python $(PIP)/pyinstaller.py --upx-dir=$(UPX_PATH) --onefile --console --icon $(ICON2) --name ctx_magick -p src/ src/ctx_magick.py
vtp:
	python $(PIP)/pyinstaller.py --upx-dir=$(UPX_PATH) --onefile --console --icon $(ICON3) --name vtp_magick -p src/ src/vtp_magick.py
deg:
	python $(PIP)/pyinstaller.py --upx-dir=$(UPX_PATH) --onefile --console --icon $(ICON4) --name deg_magick -p src/ src/deg_magick.py
cui:
	python $(PIP)/pyinstaller.py --upx-dir=$(UPX_PATH) --onefile --console --icon $(ICON5) --name cui_magick -p src/ src/cui_magick.py
wizard:
	python $(PIP)/pyinstaller.py --upx-dir=$(UPX_PATH) --onefile --console --name jabia_wizard -p src/ src/experimental/jabia_wizard.py


.PHONY: test
test:
	mkdir -p $(TEMP)
	python src/pak_magick.py data_win32.pak $(TEMP)
	python src/pak_magick.py configs_win32.pak.crypt $(TEMP)
	python src/pak_magick.py interface_win32.pak.crypt $(TEMP)
	python src/ctx_magick.py $(TEMP)/bin_win32/interface/main.ctx $(TEMP)
	python src/ctx_magick.py $(TEMP)/main.ctx.txt $(TEMP) 
	python src/deg_magick.py $(TEMP)/bin_win32/configs/main.deg $(TEMP)
	python src/deg_magick.py $(TEMP)/main.deg.txt $(TEMP)
	python src/cui_magick.py $(TEMP)/bin_win32/interface/interface.cui $(TEMP)
	python src/cui_magick.py $(TEMP)/interface.cui.txt $(TEMP)
	rm -rf $(TEMP)

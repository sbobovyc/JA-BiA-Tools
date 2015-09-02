    @echo off
    set ROOT="C:\Program Files (x86)\Steam\steamapps\common\jabia"
    set BIA=C:\Users\sbobovyc\Desktop\bia\1.11
    set BIN=.\dist
    set TEMP=%BIA%\temp

    echo Testing pak_magick
    %BIN%\pak_magick.exe %ROOT%\configs_win32.pak.crypt %BIA%
    %BIN%\pak_magick.exe %ROOT%\interface_win32.pak.crypt %BIA%
    %BIN%\pak_magick.exe %ROOT%\data_win32.pak %BIA%
    %BIN%\pak_magick.exe %ROOT%\data1_win32.pak %BIA%
    %BIN%\pak_magick.exe %ROOT%\data2_win32.pak %BIA%
    %BIN%\pak_magick.exe %ROOT%\data3_win32.pak %BIA%
    %BIN%\pak_magick.exe %ROOT%\data4_win32.pak %BIA%

    echo.
    echo Testing cui_magick
    %BIN%\cui_magick.exe %BIA%\bin_win32\interface\interface.cui %TEMP%
    %BIN%\cui_magick.exe %TEMP%\interface.cui.txt 

    echo.
    echo Testing ctx_magick
    mkdir %TEMP%
    %BIN%\ctx_magick.exe %BIA%\bin_win32\interface\equipment.ctx %TEMP%
    %BIN%\ctx_magick.exe %TEMP%\equipment.sqlite %TEMP%
    %BIN%\ctx_magick.exe %TEMP%\equipment.ctx.txt %TEMP%

    echo. 
    echo Testing deg_magick
    %BIN%\deg_magick.exe %BIA%\bin_win32\configs\main.deg %TEMP%
    %BIN%\deg_magick.exe %TEMP%\main.deg.txt %TEMP%


    @echo off
    set BIA=C:\Users\sbobovyc\Desktop\bia\1.06
    set BIN=.\dist
    set TEMP=%BIA%\temp

    echo Testing pak_magick
    %BIN%\pak_magick.exe %BIA%\configs_win32.pak %BIA%
    %BIN%\pak_magick.exe %BIA%\interface_win32.pak %BIA%
    %BIN%\pak_magick.exe %BIA%\data_win32.pak %BIA%
    %BIN%\pak_magick.exe %BIA%\data1_win32.pak %BIA%
    %BIN%\pak_magick.exe %BIA%\data2_win32.pak %BIA%
    %BIN%\pak_magick.exe %BIA%\data3_win32.pak %BIA%

    echo.
    echo Testing ctx_magick
    mkdir %TEMP%
    %BIN%\ctx_magick.exe %BIA%\bin_win32\interface\equipment.ctx %TEMP%
    %BIN%\ctx_magick.exe %TEMP%\equipment.ctx.txt %TEMP%

    echo. 
    echo Testing deg_magick
    %BIN%\deg_magick.exe %BIA%\bin_win32\configs\main.deg %TEMP%
    %BIN%\deg_magick.exe %TEMP%\main.deg.txt %TEMP%

    echo.
    echo Testing cui_magick
    %BIN%\cui_magick.exe %BIA%\bin_win32\interface\interface.cui %TEMP%
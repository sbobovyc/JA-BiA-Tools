
[Getting started](https://github.com/sbobovyc/JA-BiA-Tools/wiki/Getting-started) <-- Must read for new modders
[Compiling project from source](https://github.com/sbobovyc/JA-BiA-Tools/wiki/Compiling-project-from-source)
[Mods] (http://www.moddb.com/mods/sbobovycs-jabia-mods-tools) <strong>Mods are now distributed exclusively through moddb!</strong>

########
BINARY
########
1. Open a command prompt, you should see something like "C:\Users\your_name"
2. Then change directory to where the tools are:
cd C:\Users\your_name\Desktop\bia_tools
3. Use the tools:
pak_magick.exe somefile.pak
pak_magick.exe somefile.pak.crypt
ctx_magick.exe somefile.ctx
deg_magick.exe somefile.deg

4. All files have a help
pak_magick.exe -h
ctx_magick.exe -h
deg_magick.exe -h

ctx_magick.exe equipment.ctx
Unpacking C:\Users\sbobovyc\workspace\JA-BiA-Tools\dist\equipment.ctx
Creating C:\Users\sbobovyc\workspace\JA-BiA-Tools\dist\equipment.ctx.txt

ctx_magick.exe equipment.ctx.txt
Packing C:\Users\sbobovyc\workspace\JA-BiA-Tools\dist\equipment.ctx.txt
Creating C:\Users\sbobovyc\workspace\JA-BiA-Tools\dist\equipment.ctx

ctx_magick.exe equipment.ctx -i
Unpacking C:\Users\sbobovyc\Desktop\test\bin_win32\interface\equipment.ctx
Number of itmes: 1082
Last item id: 14016
Number of languages in file: 5
Data offset: 0x43
Language: eng, data offset: 0x0 bytes
Language: ger, data offset: 0x25f1c bytes
Language: fra, data offset: 0x4f9ee bytes
Language: ita, data offset: 0x79b54 bytes
Language: spa, data offset: 0xa0a1c bytes

5. Most tools also have debug output
deg_magick.exe main.deg -d

########
PYTHON
########
cd src
python pak_magick.py -h
python ctx_magick.py -h
python deg_magick.py -h

python pak_magick.py "C:\Program Files (x86)\Jagged Alliance Back in Action Demo\voices_win32.pak"

python ctx_magick.py ..\..\..\Desktop\test\bin_win32\interface\equipment.ctx
Unpacking C:\Users\sbobovyc\Desktop\test\bin_win32\interface\equipment.ctx
Creating C:\Users\sbobovyc\workspace\JA-BiA-Tools\src\equipment.ctx.txt

python ctx_magick.py equipment.ctx.txt
Packing C:\Users\sbobovyc\workspace\JA-BiA-Tools\src\equipment.ctx.txt
Creating C:\Users\sbobovyc\workspace\JA-BiA-Tools\src\equipment.ctx

python ctx_magick.py equipment.ctx -i
Unpacking C:\Users\sbobovyc\Desktop\test\bin_win32\interface\equipment.ctx
Number of itmes: 1082
Last item id: 14016
Number of languages in file: 5
Data offset: 0x43
Language: eng, data offset: 0x0 bytes
Language: ger, data offset: 0x25f1c bytes
Language: fra, data offset: 0x4f9ee bytes
Language: ita, data offset: 0x79b54 bytes
Language: spa, data offset: 0xa0a1c bytes

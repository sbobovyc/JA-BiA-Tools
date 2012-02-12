########
PYTHON
########
cd src
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

########
BINARY
########
cd dist

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



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



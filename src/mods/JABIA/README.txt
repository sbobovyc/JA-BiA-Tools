Dependencies:

Microsoft Detours 3.0
Boost 1.55
my custom C# injector library
Inno Setup (to compile the exe and dlls into an installer)

1. Download, install and compile Detours 3.0 for x86
2. Download and build DllInjection (Release build) from WinHookInject repo
git clone https://github.com/sbobovyc/WinHookInject.git
3. Open JABIA.sln and compile, making sure JABIA_mod_launcher_ng  has a reference to DllInjection.dll
4. Use Inno Setup to compile jabia_setup.iss
* JABIA\Release\Output\jabia_mod_launcher_setup.exe
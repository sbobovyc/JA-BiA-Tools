#ifndef MOD_LAUNCHER
#define MOD_LAUNCHER
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <iostream> 
#include <fstream> 

#define PATH_TO_MOD_LAUNCHER_XML "\\mods\\JABIA_mod_launcher.xml"
#define LAUNCHER_VERSION_STRING "Version 0.3c\r\n"
#define MOTD "For latest updates, check:\r\n http://www.moddb.com/mods/sbobovycs-jabia-mods-tools/downloads \r\n"

#define LAUNCHER_NAME "JaggedAllianceBIA.exe"
#define EXE_NAME "GameJABiA.exe"

#define DEBUGGER_DLL_PATH "\\mods\\debugger\\JABIA_debug.dll"
#define XPMOD_DLL_PATH "\\mods\\xpmod\\JABIA_xpmod.dll"
#define LOOTDROP_DLL_PATH "\\mods\\loot_drop\\JABIA_loot_drop.dll"
#define CAMERA_DLL_PATH "\\mods\\camera\\JABIA_camera.dll"
#define PATHMOD_DLL_PATH "\\mods\\pathmod\\JABIA_pathmod.dll"

typedef struct JABIA_mod_launcher_parameters { 
	bool debug_mod;
	bool xp_mod;
	bool loot_drop_mod;
	bool camera_mod;
	bool path_mod;


	// initializer list to use copy constructor instead of default constructor
    JABIA_mod_launcher_parameters() : 	
		debug_mod(false), xp_mod(false), loot_drop_mod(false), camera_mod(false), path_mod(false)
    {

	}
	
	
	
	// TODO add pretty print 
    friend std::ostream& operator << (std::ostream& out, JABIA_mod_launcher_parameters& d) 
    {
		out << "debug: " << d.debug_mod 
			<< " xp: " << d.xp_mod
			<< " loot: " << d.loot_drop_mod
			<< " camera: " << d.camera_mod
			<< " path: " << d.path_mod;
        return out;
    }

	// take care of serilization to xml
    template<class Archive>
    void serialize(Archive& archive, const unsigned int version)
    {
		archive & BOOST_SERIALIZATION_NVP(debug_mod);
		archive & BOOST_SERIALIZATION_NVP(xp_mod);
		archive & BOOST_SERIALIZATION_NVP(loot_drop_mod);
		archive & BOOST_SERIALIZATION_NVP(camera_mod);
		archive & BOOST_SERIALIZATION_NVP(path_mod);
    }
} JABIA_mod_launcher_parameters;

#endif

/*
@author: sbobovyc
*/

/*
Copyright (C) 2013 Stanislav Bobovych

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef GAME_VERSION
#define GAME_VERSION

#include <windows.h>
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <boost/filesystem.hpp>
#include <iostream> 
#include <fstream> 

// Select game version here
#define JABIA
//#define JAC

#if defined(JABIA)
static char ProcessName[] = "GameJABiA.exe";
#elif defined(JAC)
static char ProcessName[] = "GameJACrossfire.exe";
#else
#error Need to define either JABIA or JAC in game_version.h.
#endif

template <class parameters>
void save(std::string filepath, parameters params) 
{ 	
	std::ofstream file(filepath); 
	boost::archive::xml_oarchive oa(file); 		
	oa & BOOST_SERIALIZATION_NVP(params); 	
} 

template <class parameters>
void load(std::string filepath, parameters & dr) 
{ 
	boost::filesystem::path working_dir = boost::filesystem::current_path();
	boost::filesystem::path modpath(filepath);
	boost::filesystem::path fullpath = working_dir / modpath;
	if ( !(boost::filesystem::exists(fullpath) && boost::filesystem::is_regular_file(fullpath)) )    // does p actually exist and is p a regular file?   
	{
		OutputDebugString("templated, Creating xml on load");
		parameters d;
		save(fullpath.string(), d);
	}

	std::ifstream file(fullpath.string()); 
	boost::archive::xml_iarchive ia(file);   
	ia >> BOOST_SERIALIZATION_NVP(dr); 
	OutputDebugString("templated, Done loading xml");
}


#endif /* GAME_VERSION */

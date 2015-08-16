/*
@author: sbobovyc
*/

/*
Copyright (C) 2015 Stanislav Bobovych

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

#ifndef LOOT_DROP
#define LOOT_DROP
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <iostream> 
#include <fstream> 

#define PATH_TO_LOOT_DROP_XML ".\\mods\\loot_drop\\JABIA_loot_drop.xml"

class JABIA_LOOT_DROP_parameters {
public:
	float weapon_drop_chance;
	float item_drop_chance;

	JABIA_LOOT_DROP_parameters() :
		weapon_drop_chance(1.0),
		item_drop_chance(1.0) 
	{

	}

	// take care of serilization to xml
	template<class Archive>
	void serialize(Archive& archive, const unsigned int version)
	{
		archive & BOOST_SERIALIZATION_NVP(weapon_drop_chance);
		archive & BOOST_SERIALIZATION_NVP(item_drop_chance);
	}
};

#endif
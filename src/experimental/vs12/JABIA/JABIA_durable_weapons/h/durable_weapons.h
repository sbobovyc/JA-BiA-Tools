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

#ifndef DURABLE_WEAPONS
#define DURABLE_WEAPONS
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <iostream> 
#include <fstream> 

#define PATH_TO_DURABLE_WEAPONS_XML "\\mods\\durable_weapons\\JABIA_durable_weapons.xml"

class JABIA_DURABLE_WEAPONS_parameters { 
public:
	
	float new_max_durability_multiplier;

	// initializer list to use copy constructor instead of default constructor
    JABIA_DURABLE_WEAPONS_parameters() : 	
		new_max_durability_multiplier(0.5)
    {
	}
	
		
	// TODO add pretty print 
    friend std::ostream& operator << (std::ostream& out, JABIA_DURABLE_WEAPONS_parameters& d) 
    {
        /*out << "day: " << d.m_day 
              << " month: " << d.m_month
	<< " year: " << d.m_year;
        */return out;
    }

	// take care of serilization to xml
    template<class Archive>
    void serialize(Archive& archive, const unsigned int version)
    {
		archive & BOOST_SERIALIZATION_NVP(new_max_durability_multiplier);
    }
};

#endif
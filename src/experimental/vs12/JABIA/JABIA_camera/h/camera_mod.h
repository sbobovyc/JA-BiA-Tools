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

#ifndef CAMERA_MOD
#define CAMERA_MOD
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <iostream> 
#include <fstream> 

#define PATH_TO_CAMERA_XML "\\mods\\camera\\JABIA_camera.xml"
#define CAMERA_PARAMS_COUNT 4

typedef struct JABIA_camera_parameters { 
	int last_used;
	float camera_min[CAMERA_PARAMS_COUNT];
	float camera_max[CAMERA_PARAMS_COUNT];
	float min_angle[CAMERA_PARAMS_COUNT];  // 2.0 is 90 degree, ie directly overhead
	float max_angle_delta[CAMERA_PARAMS_COUNT]; // min + delta = max angle

	// initializer list to use copy constructor instead of default constructor
    JABIA_camera_parameters() :
		last_used(0)
    {
		for(int i = 0; i < CAMERA_PARAMS_COUNT; i++)
		{
			camera_min[i] = 130.0f;
			camera_max[i] = 520.0f;
			min_angle[i] = 1.1f;
			max_angle_delta[i] = 0.8f;
		}
	}
	
	
	
	// TODO add pretty print 
    friend std::ostream& operator << (std::ostream& out, JABIA_camera_parameters& d) 
    {
		int last_used = d.last_used;
		out << "last_used: " << last_used
			<< "camera_min: " << d.camera_min[last_used]
			<< " camera_max: " << d.camera_max[last_used]
			<< " min_angle: " << d.min_angle[last_used]
			<< " max_angle_delta: " << d.max_angle_delta[last_used];
        return out;
    }

	// take care of serilization to xml
    template<class Archive>
    void serialize(Archive& archive, const unsigned int version)
    {
		archive & BOOST_SERIALIZATION_NVP(last_used);
		archive & BOOST_SERIALIZATION_NVP(camera_min);
		archive & BOOST_SERIALIZATION_NVP(camera_max);
		archive & BOOST_SERIALIZATION_NVP(min_angle);
		archive & BOOST_SERIALIZATION_NVP(max_angle_delta);
    }
} JABIA_camera_parameters;



#endif /* CAMERA_MOD */

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

#ifndef XPMOD
#define XPMOD
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <iostream> 
#include <fstream> 

#define PATH_TO_XPMOD_XML ".\\mods\\xpmod\\JABIA_xpmod.xml"

class JABIA_XPMOD_parameters { 
public:
	double medical_scaler;
	double medical_intel_scaler;
	double medical_learning_time;

	double explosives_scaler;
	double explosives_intel_scaler;

	double marksmanship_scaler;
	double marksmanship_intel_scaler;
	double marksmanship_learning_time;

	unsigned int stealth_modulo;	// how often do we update stealth (default is every 10 stealth related actions)
	double stealth_kills_to_counterstealth_ratio_modifier;
	double stealth_damage_ratio_modifier;

	double mechanical_scaler;
	double mechanical_intel_scaler;
	double mechanical_multiplier;

	// initializer list to use copy constructor instead of default constructor
    JABIA_XPMOD_parameters() : 	
		medical_scaler(15000.), medical_intel_scaler(150.), medical_learning_time(0.1),
		explosives_scaler(500.), explosives_intel_scaler(150.),
		marksmanship_scaler(0.5), marksmanship_intel_scaler(150.), marksmanship_learning_time(0.1),
		stealth_modulo(10), stealth_kills_to_counterstealth_ratio_modifier(1), stealth_damage_ratio_modifier(0.35),
		mechanical_scaler(70000.), mechanical_intel_scaler(130.), mechanical_multiplier(100.)
    {
	}
	
	
	
	// TODO add pretty print 
    friend std::ostream& operator << (std::ostream& out, JABIA_XPMOD_parameters& d) 
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
		archive & BOOST_SERIALIZATION_NVP(medical_scaler);
		archive & BOOST_SERIALIZATION_NVP(medical_learning_time);

		archive & BOOST_SERIALIZATION_NVP(explosives_scaler);
		archive & BOOST_SERIALIZATION_NVP(explosives_intel_scaler);

		archive & BOOST_SERIALIZATION_NVP(marksmanship_scaler);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_intel_scaler);		
		archive & BOOST_SERIALIZATION_NVP(marksmanship_learning_time);

		archive & BOOST_SERIALIZATION_NVP(stealth_kills_to_counterstealth_ratio_modifier);
		archive & BOOST_SERIALIZATION_NVP(stealth_damage_ratio_modifier);

		archive & BOOST_SERIALIZATION_NVP(mechanical_scaler);
		archive & BOOST_SERIALIZATION_NVP(mechanical_intel_scaler);
		archive & BOOST_SERIALIZATION_NVP(mechanical_multiplier);
    }
};

unsigned int calc_medical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_explosives(JABIA_XPMOD_parameters * params, JABIA_Character * ptr, unsigned int total_explosives_actions);
unsigned int calc_marksmanship(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_stealth(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_mechanical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);

#endif
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

#define PATH_TO_XPMOD_XML "\\mods\\xpmod\\JABIA_xpmod.xml"

class JABIA_XPMOD_parameters { 
public:
	// all modifiers have to do with intelligence
	unsigned int medical_modulo;	// how often do we update medical (default is every 100 heal points)
	unsigned int medical_norm_modulo;	// sets the bounds of computation (default is 0 to 1000)
	double medical_a;
	double medical_b;
	double medical_xoffset;
	std::vector<double> medical_modifier;

	unsigned int explosives_modulo;	// how often do we update medical (default is every 10 explosives actions)
	unsigned int explosives_norm_modulo;	// sets the bounds of computation (default is 0 to 200)
	double explosives_a;
	double explosives_b;
	double explosives_xoffset;
	std::vector<double> explosives_modifier;

	unsigned int marksmanship_modulo;	// how often do we update marksmanship (default is every five kills)
	unsigned int marksmanship_norm_modulo;	// sets the bounds of computation (default is 0 to 100)
	double marksmanship_a;
	double marksmanship_b;
	double marksmanship_xoffset;
	std::vector<double> marksmanship_accuracy_modifier;

	unsigned int stealth_modulo;	// how often do we update stealth (default is every 10 stealth related actions)
	double stealth_kills_to_counterstealth_ratio_modifier;
	double stealth_damage_ratio_modifier;

	unsigned int mechanical_modulo;	// how often do we update mechanical (default is every 5 mechanical actions)
	unsigned int mechanical_norm_modulo;	// sets the bounds of computation (default is 0 to 100)
	double mechanical_a;
	double mechanical_b;
	double mechanical_xoffset;
	std::vector<double> mechanical_modifier;

	// initializer list to use copy constructor instead of default constructor
    JABIA_XPMOD_parameters() : 	
		medical_modulo(100), medical_norm_modulo(1000), medical_a(0.004), medical_b(4.5), medical_xoffset(-2), medical_modifier(2),
		explosives_modulo(10), explosives_norm_modulo(200), explosives_a(0.015), explosives_b(3.0), explosives_xoffset(-1.5), explosives_modifier(3),
		marksmanship_modulo(5), marksmanship_norm_modulo(100), marksmanship_a(0.042), marksmanship_b(5.0), marksmanship_xoffset(-2.0), marksmanship_accuracy_modifier(2),
		stealth_modulo(10), stealth_kills_to_counterstealth_ratio_modifier(1), stealth_damage_ratio_modifier(0.35),
		mechanical_modulo(5), mechanical_norm_modulo(100), mechanical_a(0.025), mechanical_b(4.0), mechanical_xoffset(-1.5), mechanical_modifier(3)
    {
		medical_modifier[0] = 1.25;
		medical_modifier[1] = 1.0;

		explosives_modifier[0] = 1.25;
		explosives_modifier[1] = 1;
		explosives_modifier[2] = 0.7;

		marksmanship_accuracy_modifier[0] = 1.25;
		marksmanship_accuracy_modifier[1] = 0.7;

		mechanical_modifier[0] = 1.25;
		mechanical_modifier[1] = 0.7;
		mechanical_modifier[2] = 0.6;
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
		archive & BOOST_SERIALIZATION_NVP(medical_modulo);
		archive & BOOST_SERIALIZATION_NVP(medical_norm_modulo);
		archive & BOOST_SERIALIZATION_NVP(medical_a);
		archive & BOOST_SERIALIZATION_NVP(medical_b);
		archive & BOOST_SERIALIZATION_NVP(medical_xoffset);
		archive & BOOST_SERIALIZATION_NVP(medical_modifier); 

		archive & BOOST_SERIALIZATION_NVP(explosives_modulo);
		archive & BOOST_SERIALIZATION_NVP(explosives_norm_modulo);		
		archive & BOOST_SERIALIZATION_NVP(explosives_a);
		archive & BOOST_SERIALIZATION_NVP(explosives_b);
		archive & BOOST_SERIALIZATION_NVP(explosives_xoffset);
		archive & BOOST_SERIALIZATION_NVP(explosives_modifier); 

		archive & BOOST_SERIALIZATION_NVP(marksmanship_modulo);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_norm_modulo);		
		archive & BOOST_SERIALIZATION_NVP(marksmanship_a);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_b);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_xoffset);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_accuracy_modifier); 

		archive & BOOST_SERIALIZATION_NVP(stealth_kills_to_counterstealth_ratio_modifier);
		archive & BOOST_SERIALIZATION_NVP(stealth_damage_ratio_modifier);

		archive & BOOST_SERIALIZATION_NVP(mechanical_modulo);
		archive & BOOST_SERIALIZATION_NVP(mechanical_norm_modulo);		
		archive & BOOST_SERIALIZATION_NVP(mechanical_a);
		archive & BOOST_SERIALIZATION_NVP(mechanical_b);
		archive & BOOST_SERIALIZATION_NVP(mechanical_xoffset);
		archive & BOOST_SERIALIZATION_NVP(mechanical_modifier); 
    }
};

unsigned int calc_medical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_explosives(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_marksmanship(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_stealth(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_mechanical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);

#endif
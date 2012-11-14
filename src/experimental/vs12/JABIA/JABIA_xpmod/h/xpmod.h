#ifndef XPMOD
#define XPMOD
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <iostream> 
#include <fstream> 


typedef struct JABIA_XPMOD_parameters { 
	unsigned int medical_modulo;	// how often do we update medical (default is every 100 heal points)
	double medical_a;
	double medical_b;
	double medical_xoffset;
	std::vector<double> medical_modifier;

	unsigned int explosives_modulo;	// how often do we update medical (default is every 10 explosives actions)
	double explosives_a;
	double explosives_b;
	double explosives_xoffset;
	std::vector<double> explosives_modifier;

	unsigned int marksmanship_modulo;	// how often do we update marksmanship (default is every five kills)
	double marksmanship_a;
	double marksmanship_b;
	double marksmanship_xoffset;
	std::vector<double> marksmanship_accuracy_modifier;
	
	// initializer list to use copy constructor instead of default constructor
    JABIA_XPMOD_parameters() : 	
		medical_modulo(100), medical_a(0.004), medical_b(4.5), medical_xoffset(-2), medical_modifier(2),
		explosives_modulo(10), explosives_a(0.015), explosives_b(3), explosives_xoffset(-1.5), explosives_modifier(3),
		marksmanship_modulo(5), marksmanship_a(0.042), marksmanship_b(5), marksmanship_xoffset(-2), marksmanship_accuracy_modifier(2)
    {
		medical_modifier[0] = 1.25;
		medical_modifier[1] = 1.0;

		explosives_modifier[0] = 1.25;
		explosives_modifier[1] = 1;
		explosives_modifier[2] = 0.7;

		marksmanship_accuracy_modifier[0] = 1.25;
		marksmanship_accuracy_modifier[1] = 0.7;
	}
	
	
		
    friend std::ostream& operator << (std::ostream& out, JABIA_XPMOD_parameters& d) 
    {
        /*out << "day: " << d.m_day 
              << " month: " << d.m_month
	<< " year: " << d.m_year;
        */return out;
    }
    template<class Archive>
    void serialize(Archive& archive, const unsigned int version)
    {
		archive & BOOST_SERIALIZATION_NVP(medical_modulo);
		archive & BOOST_SERIALIZATION_NVP(medical_a);
		archive & BOOST_SERIALIZATION_NVP(medical_b);
		archive & BOOST_SERIALIZATION_NVP(medical_xoffset);
		archive & BOOST_SERIALIZATION_NVP(medical_modifier); 

		archive & BOOST_SERIALIZATION_NVP(explosives_modulo);
		archive & BOOST_SERIALIZATION_NVP(explosives_a);
		archive & BOOST_SERIALIZATION_NVP(explosives_b);
		archive & BOOST_SERIALIZATION_NVP(explosives_xoffset);
		archive & BOOST_SERIALIZATION_NVP(explosives_modifier); 

		archive & BOOST_SERIALIZATION_NVP(marksmanship_modulo);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_a);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_b);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_xoffset);
		archive & BOOST_SERIALIZATION_NVP(marksmanship_accuracy_modifier); 


    }
} JABIA_XPMOD_parameters;

void save(void);
void load(JABIA_XPMOD_parameters * dr) ;
unsigned int calc_medical(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_explosives(JABIA_XPMOD_parameters * params, JABIA_Character * ptr);
unsigned int calc_marksmanship(JABIA_XPMOD_parameters * params, unsigned int kills, double accuracy);

#endif
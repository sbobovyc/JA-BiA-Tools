#ifndef CAMERA
#define CAMERA
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <iostream> 
#include <fstream> 

#define PATH_TO_CAMERA_XML "\\mods\\camera\\JABIA_camera.xml"

typedef struct JABIA_camera_parameters { 
	float camera_min;
	float camera_max;
	float min_angle;  // 2.0 is 90 degree, ie directly overhead
	float max_angle_delta; // min + delta = max angle

	// initializer list to use copy constructor instead of default constructor
    JABIA_camera_parameters() : 	
		camera_min(130.0), camera_max(520.0), min_angle(1.1), max_angle_delta(0.8)
    {

	}
	
	
	
	// TODO add pretty print 
    friend std::ostream& operator << (std::ostream& out, JABIA_camera_parameters& d) 
    {
		out << "camera_min: " << d.camera_min 
			<< " camera_max: " << d.camera_max
			<< " min_angle: " << d.min_angle
			<< " max_angle_delta: " << d.max_angle_delta;
        return out;
    }

	// take care of serilization to xml
    template<class Archive>
    void serialize(Archive& archive, const unsigned int version)
    {
		archive & BOOST_SERIALIZATION_NVP(camera_min);
		archive & BOOST_SERIALIZATION_NVP(camera_max);
		archive & BOOST_SERIALIZATION_NVP(min_angle);
		archive & BOOST_SERIALIZATION_NVP(max_angle_delta);
    }
} JABIA_camera_parameters;

typedef struct Camera {
	float unknown1[77];
	float current_angle;
	float unknown2[3];
	float camera_min;
	float camera_max;
	float min_angle;  // 2.0 is 90 degree, ie directly overhead
	float max_angle_delta; // min + delta = max angle
	float current_height;
} Camera;

#endif /* CAMERA */
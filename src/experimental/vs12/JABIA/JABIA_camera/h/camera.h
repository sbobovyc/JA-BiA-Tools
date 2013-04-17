#ifndef CAMERA
#define CAMERA
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
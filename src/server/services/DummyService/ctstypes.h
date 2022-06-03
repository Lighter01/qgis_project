#ifndef __CTSTYPES
#define __CTSTYPES
#include <string>
struct Airports {
    std::string name;
    std::string city;
    std::string country;
//    long double lat;
//    long double lon;
    double lat;
    double lon;
    std::string country_abr;
};
struct City {
    std::string country_abr;
    std::string country_full;
    std::string name;
//    long double lat;
//    long double lon;
    double lat;
    double lon;
    bool is_capital = 0;
};
enum Type {
    Town,
    Airport,
    Undefined = -1,
};

struct Point {
    std::string name;
    Type type = Undefined;
    long double lat;
    long double lon;
//    Point &operator=(const City&);
//    Point &operator=(const Airports&);

Point& operator=(const City& city) {
    name = city.name;
    type = Town;
    lat = city.lat;
    lon = city.lon;
    return *this;
};

Point& operator=(const Airports& airport) {
    name = airport.name;
    type = Airport;
    lat = airport.lat;
    lon = airport.lon;
    return *this;
};



};

//Point &Point::operator=(const City& city) {
//    name = city.name;
//    type = Town;
//    lat = city.lat;
//    lon = city.lon;
//    return *this;
//}
//
//Point &Point::operator=(const Airports& airport) {
//    name = airport.name;
//    type = Airport;
//    lat = airport.lat;
//    lon = airport.lon;
//    return *this;
//}

enum Path_type {
    ground,
    air,
    both,
    undefined = -1,
};

struct Line {
    Point begin;
    Point end;
    long double length;
    Path_type type = undefined;
};

struct Country {
    std::string name;
    Point capital;
    Point airport;
};
#endif
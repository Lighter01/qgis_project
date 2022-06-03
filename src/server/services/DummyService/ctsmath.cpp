#include "ctsmath.h"
#include <cmath>

long double deg2rad(long double deg) {
    return (deg * M_PI / 180);
}

long double rad2deg(long double rad) {
    return (rad * 180 / M_PI);
}

double distanceEarth(long double lat1d, long double lon1d, long double lat2d, long double lon2d) {
    long double lat1r, lon1r, lat2r, lon2r, u, v;
    lat1r = deg2rad(lat1d);
    lon1r = deg2rad(lon1d);
    lat2r = deg2rad(lat2d);
    lon2r = deg2rad(lon2d);
    u = sin((lat2r - lat1r)/2);
    v = sin((lon2r - lon1r)/2);
    return 2.0 * 6371 * asin(sqrt(u * u + cos(lat1r) * cos(lat2r) * v * v));
}
// too much math error
//double Gaversinus(Point& p1, Point& p2) {
//    double R = 6371;
//    double lon = (p2.getX() - p1.getX()) * (M_PI/180);
//    double lat = (p2.getY() - p2.getY()) * (M_PI/180);
//    double res = sin(lat / 2) * sin(lat / 2) + cos(p1.getY() * (M_PI/180))
//                                               * cos(p2.getY() * (M_PI/180)) * sin(lon / 2) * sin(lon / 2);
//    double d = 2 * R * atan2(sqrt(res), sqrt(1 - res));
//    return d;
//}


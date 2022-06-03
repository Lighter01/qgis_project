#include "ctscore.h"
#include "ctsmath.h"
#include <algorithm>
#include <iostream>

City findCapitalInfo(const std::string& name, std::vector<City> capital) { // Здесь возможно добавление отлова ошибки на отсутствие названия города
    bool flag = true;
    std::vector<City>::iterator it = capital.begin();
    for (it = capital.begin(); it < capital.end() && flag; ++it) {
        if (it->name == name) flag = false;
    }
    return *it;
}

Airports findNearestAirport(City start, std::vector<Airports> end) {
    Airports min_port; long double prev_dist = 99999999;
    min_port.country_abr = "zz";
    for (auto it : end) {
        if (it.country_abr == start.country_abr) {
            if (min_port.country_abr != "zz") {
                long double new_dist = distanceEarth(start.lat, start.lon, it.lat, it.lon);
                if (prev_dist > new_dist) {
                    prev_dist = new_dist;
                    min_port = it;
                }
            } else {
                min_port = it; // Я уже даже забыл, что оно работает без перегрузки
            }
        }
    }
    return min_port;
}

std::vector<Country> getCountryData(std::vector<std::string> countries, std::vector<City> capitals, std::vector<Airports> airports) {
    std::vector<Country> res;
    for (auto it : countries) {
        City tmp = findCapitalInfo(it, capitals);
        Airports tmp_air = findNearestAirport(tmp, airports);
        Country dum;
        dum.name = it;
        dum.capital = tmp;
        dum.airport = tmp_air;
        res.push_back(dum);
    }
    return res;
}
std::vector<Line> Path(std::vector<std::string> &countries,
                       std::vector<Airports>& airports,
                       std::vector<City>& capitals)
{
    std::vector<Line> pth;

    bool skip_first = true;

    Point prev_airport, prev_capital;
    for (auto it : countries) {
        Point next_airport, next_capital;
        std::vector<City>::iterator ptr = std::find_if(capitals.begin(), capitals.end(), [&it](City& ptr) { return ptr.country_full == it ;});
        if (ptr != capitals.end()) {
            next_capital = *ptr;

            next_airport = findNearestAirport(*ptr, airports);
            Line air_air, air_ground, ground_air;

            if (!skip_first)
            {
                ground_air.type = ground;
                //debug
                //std::cout << "check lat and lon ground_air-> "<< prev_capital.lat << " " << prev_capital.lon << " " << prev_airport.lat << " " << prev_airport.lon << "\n";
                ground_air.length = distanceEarth(prev_capital.lat, prev_capital.lon, prev_airport.lat, prev_airport.lon);
                //debug
                //std::cout << "check ground_air-> "<< it << " " << ground_air.length << '\n';
                ground_air.begin = prev_capital;
                ground_air.end = prev_airport;

                air_air.type = air;
                air_air.length = distanceEarth(prev_airport.lat, prev_airport.lon, next_airport.lat, next_airport.lon);
                air_air.begin = prev_airport;
                air_air.end = next_airport;

                pth.push_back(ground_air);
                pth.push_back(air_air);
            }

            air_ground.type = ground;
            //debug
            //std::cout << "check lat and lon air_ground-> "<< next_capital.lat << " " << next_capital.lon << " " << next_airport.lat << " " << next_airport.lon << "\n";
            air_ground.length = distanceEarth(next_capital.lat, next_capital.lon, next_airport.lat, next_airport.lon);
            //debug
            //std::cout << "check air_ground-> "<< it << " " << air_ground.length << '\n';
            if (!skip_first) {
                air_ground.begin = next_airport;
                air_ground.end = next_capital;
            } else {
                air_ground.begin = next_capital;
                air_ground.end = next_airport;
                skip_first = false;
            }

            pth.push_back(air_ground);

            prev_airport = next_airport;
            prev_capital = next_capital;
        } else {
            std::cout << "No such country, skip to next.\n";
        }
    }
    if (pth.size() > 1) pth.erase(pth.begin());

    return pth;
}
long double getPathLength(std::vector<Line>& Path, Path_type state) { // both == Ground + Air
    long double res = 0;
    for (auto it : Path) {
        if (it.type == state || state == both) {
            res += it.length;
        }
    }
    return res;
}

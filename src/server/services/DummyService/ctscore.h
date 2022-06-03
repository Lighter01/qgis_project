#ifndef __CTSCORE
#define __CTSCORE
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include "ctstypes.h"

City findCapitalInfo(const std::string& name, std::vector<City> capital);
Airports findNearestAirport(City start, std::vector<Airports> end);
std::vector<Country> getCountryData(std::vector<std::string> countries, std::vector<City> capitals, std::vector<Airports> airports);
std::vector<Line> Path(std::vector<std::string> &countries,
                       std::vector<Airports>& airports,
                       std::vector<City>& capitals);
long double getPathLength(std::vector<Line>& Path, Path_type state);





#endif
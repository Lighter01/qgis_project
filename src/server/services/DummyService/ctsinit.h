#ifndef __CTSINIT
#define __CTSINIT
#include "ctstypes.h"
#include <vector>
#include <string>
#include <fstream>
#include <sstream>


void readCity(std::ifstream& in, std::vector<City>& city);
void readAirports(std::ifstream& f, std::vector<Airports>& airports);
void readCapital(std::ifstream& in, std::vector<City>& capital);
#endif

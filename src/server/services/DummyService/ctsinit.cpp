#include "ctsinit.h"
#include <QString>
void readCity(std::ifstream& in, std::vector<City>& city) {
    std::vector<std::string> data;
    std::string str;
    while (std::getline(in, str)) {
        std::stringstream tmp(str);
        while (std::getline(tmp, str, ',')) {
            data.push_back(str);
        }
        City temp;
        temp.country_abr = data[0];
        temp.name = data[1];
        temp.lat = std::stold(data[2]);
        temp.lon = std::stold(data[3]);
        temp.is_capital = std::stoi(data[4]);
        city.push_back(temp);
        data.clear();
    }
}



void readAirports(std::ifstream& f, std::vector<Airports>& airports) {
    std::vector<std::string> data;
    std::string str;
    while (std::getline(f, str)) {
        std::stringstream tmp(str);
        while (std::getline(tmp, str, ',')) {
            data.push_back(str);
        }
        Airports temp_air;
        temp_air.name = data[0];
        temp_air.city = data[1];
        temp_air.country = data[2];
//        temp_air.lat = std::stold(data[3]);
//        temp_air.lon = std::stold(data[4]);
        temp_air.lat = (QString::fromUtf8(data[3].c_str())).QString::toDouble();
        temp_air.lon = (QString::fromUtf8(data[4].c_str())).QString::toDouble();
        temp_air.country_abr = data[5];
        airports.push_back(temp_air);
        data.clear();
    }
}
void readCapital(std::ifstream& in, std::vector<City>& capital) {
    std::vector<std::string> data;
    std::string str;
    while (std::getline(in, str)) {
        std::stringstream tmp(str);
        while (std::getline(tmp, str, ',')) {
            data.push_back(str);
        }
        City temp;
        temp.country_full = data[0];
        temp.name = data[1];
//        temp.lat = std::stold(data[2]);
//        temp.lon = std::stold(data[3]);
        temp.lat = (QString::fromUtf8(data[2].c_str())).QString::toDouble();
        temp.lon = (QString::fromUtf8(data[3].c_str())).QString::toDouble();
        temp.country_abr = data[4];
        temp.is_capital = true;
        capital.push_back(temp);
        data.clear();
    }
}

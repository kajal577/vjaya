#ifndef GPS_MODULE_H
#define GPS_MODULE_H

#include <Arduino.h>

struct GPSData {
    double latitude;
    double longitude;
    float altitude;
    uint32_t satellites;

    bool locationValid;
    bool altitudeValid;
    bool satellitesValid;
};

void initGPS();
void updateGPS(GPSData &data);

#endif
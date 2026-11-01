#ifndef GPS_NAVIGATION_H
#define GPS_NAVIGATION_H

void initGPS();
void updateGPS();

bool gpsAvailable();

double getLatitude();
double getLongitude();

double getDistanceTo(
  double targetLat,
  double targetLon
);

double getBearingTo(
  double targetLat,
  double targetLon
);

#endif
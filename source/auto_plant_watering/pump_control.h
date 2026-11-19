#ifndef PUMP_CONTROL_H
#define PUMP_CONTROL_H

void initPump();
void updatePump(bool wateringRequired);
bool isPumpRunning();

#endif
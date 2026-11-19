
#include "balance.h"
#include "servo_control.h"
#include "config.h"

void standPosition() {

    setServoAngle(LEFT_HIP_ROLL, 90);
    setServoAngle(LEFT_HIP_PITCH, 90);
    setServoAngle(LEFT_KNEE, 90);

    setServoAngle(RIGHT_HIP_ROLL, 90);
    setServoAngle(RIGHT_HIP_PITCH, 90);
    setServoAngle(RIGHT_KNEE, 90);
}

void resetPosition() {

    standPosition();
}

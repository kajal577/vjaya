#include "balance_controller.h"
#include "balance_config.h"

static float integral = 0.0f;

void resetPID() {
  integral = 0.0f;
}

int calculateBalanceOutput(
  float angle,
  float gyroRate,
  float targetAngle,
  float dt
) {
  float error = targetAngle - angle;

  integral += error * dt;
  integral = constrain(integral, -30.0f, 30.0f);

  // Gyroscope supplies the derivative/damping term.
  float output = PID_KP * error
               + PID_KI * integral
               - PID_KD * gyroRate;

  output = constrain(
    output,
    -(float)MAX_MOTOR_POWER,
    (float)MAX_MOTOR_POWER
  );

  return (int)output;
}
#include "motor.h"
#include "balance_config.h"

static void driveOneMotor(
  int pwmPin, int inA, int inB,
  int power, int direction
) {
  power *= direction;
  power = constrain(power, -255, 255);

  if (power > 0) {
    digitalWrite(inA, HIGH);
    digitalWrite(inB, LOW);
    analogWrite(pwmPin, power);
  } else if (power < 0) {
    digitalWrite(inA, LOW);
    digitalWrite(inB, HIGH);
    analogWrite(pwmPin, -power);
  } else {
    analogWrite(pwmPin, 0);
    digitalWrite(inA, LOW);
    digitalWrite(inB, LOW);
  }
}

void initMotors() {
  pinMode(MOTOR_ENA, OUTPUT);
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);

  pinMode(MOTOR_ENB, OUTPUT);
  pinMode(MOTOR_IN3, OUTPUT);
  pinMode(MOTOR_IN4, OUTPUT);

  stopMotors();
}

void setMotors(int leftPower, int rightPower) {
  driveOneMotor(
    MOTOR_ENA, MOTOR_IN1, MOTOR_IN2,
    leftPower, LEFT_MOTOR_DIRECTION
  );

  driveOneMotor(
    MOTOR_ENB, MOTOR_IN3, MOTOR_IN4,
    rightPower, RIGHT_MOTOR_DIRECTION
  );
}

void stopMotors() {
  setMotors(0, 0);
}
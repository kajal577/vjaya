
#include "servo_control.h"
#include "config.h"

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

static Adafruit_PWMServoDriver pwm(
    PCA9685_ADDRESS
);

static int currentAngles[SERVO_COUNT] = {
    90, 90, 90, 90, 90, 90
};

static bool initialized = false;

static uint16_t angleToPulse(int angle) {

    angle = constrain(
        angle,
        SERVO_MIN_ANGLE,
        SERVO_MAX_ANGLE
    );

    return map(
        angle,
        0,
        180,
        SERVO_MIN_US,
        SERVO_MAX_US
    );
}

void initServos() {

    Wire.begin(I2C_SDA, I2C_SCL);

    if (!pwm.begin()) {
        Serial.println("PCA9685 initialization failed!");
        return;
    }

    pwm.setPWMFreq(SERVO_FREQUENCY);

    delay(20);

    initialized = true;

    Serial.println("PCA9685 ready");
    Serial.println("6 SG90 servo channels configured");
}

void setServoAngle(uint8_t channel, int angle) {

    if (!initialized || channel >= SERVO_COUNT) {
        return;
    }

    angle = constrain(
        angle,
        SERVO_MIN_ANGLE,
        SERVO_MAX_ANGLE
    );

    uint16_t pulse = angleToPulse(angle);

    uint16_t ticks =
        ((uint32_t)pulse * 4096UL) / 20000UL;

    pwm.setPWM(channel, 0, ticks);

    currentAngles[channel] = angle;
}

void moveServoSmooth(
    uint8_t channel,
    int targetAngle,
    int stepDelay
) {

    if (!initialized || channel >= SERVO_COUNT) {
        return;
    }

    targetAngle = constrain(
        targetAngle,
        SERVO_MIN_ANGLE,
        SERVO_MAX_ANGLE
    );

    int startAngle = currentAngles[channel];

    int direction =
        (targetAngle > startAngle) ? 1 : -1;

    for (
        int angle = startAngle;
        angle != targetAngle;
        angle += direction
    ) {

        setServoAngle(channel, angle);
        delay(stepDelay);
    }

    setServoAngle(channel, targetAngle);
}

void setAllServos(int angle) {

    for (int i = 0; i < SERVO_COUNT; i++) {
        setServoAngle(i, angle);
    }
}

void disableServos() {

    if (!initialized) return;

    for (int i = 0; i < SERVO_COUNT; i++) {
        pwm.setPWM(i, 0, 4096);
    }
}

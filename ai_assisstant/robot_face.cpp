#include "robot_face.h"
#include "display.h"

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED object is defined in display.cpp
extern Adafruit_SSD1306 display;


// =====================================================
// SHOW ROBOT FACE
// =====================================================

void showRobotFace()
{
    display.clearDisplay();

    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);

    // LEFT EYE
    display.fillRoundRect(
        18, 18,
        32, 25,
        5,
        SSD1306_WHITE
    );

    // RIGHT EYE
    display.fillRoundRect(
        78, 18,
        32, 25,
        5,
        SSD1306_WHITE
    );

    // LEFT PUPIL
    display.fillCircle(
        34, 30,
        6,
        SSD1306_BLACK
    );

    // RIGHT PUPIL
    display.fillCircle(
        94, 30,
        6,
        SSD1306_BLACK
    );

    // MOUTH
    display.drawRoundRect(
        42, 48,
        44, 8,
        3,
        SSD1306_WHITE
    );

    display.display();
}
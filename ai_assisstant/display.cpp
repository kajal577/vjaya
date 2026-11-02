#include "display.h"
#include "config.h"
#include "robot_face.h"

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


// =====================================================
// OLED OBJECT
// =====================================================

Adafruit_SSD1306 display(
    OLED_WIDTH,
    OLED_HEIGHT,
    &Wire,
    OLED_RESET
);


// =====================================================
// REMOVE MARKDOWN
// =====================================================

String cleanMarkdown(String text)
{
    // Remove bold **
    text.replace("**", "");

    // Remove italic *
    text.replace("*", "");

    // Remove backticks
    text.replace("`", "");

    // Remove markdown heading #
    text.replace("#", "");

    // Replace non-breaking spaces
    text.replace("\xC2\xA0", " ");

    // Replace some common Unicode punctuation
    text.replace("\xE2\x80\x93", "-");
    text.replace("\xE2\x80\x94", "-");

    // Remove carriage return
    text.replace("\r", "");

    return text;
}


// =====================================================
// INITIALIZE OLED
// =====================================================

void initDisplay()
{
    Wire.begin(
        OLED_SDA,
        OLED_SCL
    );

    if (!display.begin(
            SSD1306_SWITCHCAPVCC,
            OLED_ADDRESS))
    {
        Serial.println("OLED initialization failed");

        while (true)
        {
            delay(1000);
        }
    }

    display.clearDisplay();

    display.setTextColor(
        SSD1306_WHITE
    );

    display.setTextSize(1);

    display.setCursor(0, 0);

    display.println(
        "AI Text Assistant"
    );

    display.println();

    display.println(
        "Starting..."
    );

    display.display();

    Serial.println(
        "OLED initialized"
    );
}


// =====================================================
// CLEAR OLED
// =====================================================

void clearDisplay()
{
    display.clearDisplay();
    display.display();
}


// =====================================================
// DISPLAY STATUS
// =====================================================

void displayStatus(
    const String &line1,
    const String &line2,
    const String &line3
)
{
    display.clearDisplay();

    display.setTextColor(
        SSD1306_WHITE
    );

    display.setTextSize(1);

    display.setCursor(0, 0);

    display.println(
        line1
    );

    if (line2.length() > 0)
    {
        display.println(
            line2
        );
    }

    if (line3.length() > 0)
    {
        display.println(
            line3
        );
    }

    display.display();
}


// =====================================================
// WORD WRAP
// =====================================================

void addWrappedLine(
    String &lines,
    String line
)
{
    line.trim();

    if (line.length() == 0)
    {
        lines += "\n";
        return;
    }

    while (line.length() > 21)
    {
        int breakPosition = 21;

        for (int i = 21; i > 0; i--)
        {
            if (line.charAt(i) == ' ')
            {
                breakPosition = i;
                break;
            }
        }

        String part =
            line.substring(
                0,
                breakPosition
            );

        part.trim();

        lines += part;
        lines += "\n";

        line =
            line.substring(
                breakPosition
            );

        line.trim();
    }

    if (line.length() > 0)
    {
        lines += line;
        lines += "\n";
    }
}


// =====================================================
// PREPARE TEXT
// =====================================================

String prepareText(
    const String &input
)
{
    String text =
        cleanMarkdown(input);

    String result = "";

    String currentLine = "";

    for (unsigned int i = 0;
         i < text.length();
         i++)
    {
        char c = text.charAt(i);

        if (c == '\n')
        {
            addWrappedLine(
                result,
                currentLine
            );

            currentLine = "";
        }
        else
        {
            currentLine += c;
        }
    }

    if (currentLine.length() > 0)
    {
        addWrappedLine(
            result,
            currentLine
        );
    }

    return result;
}


// =====================================================
// DISPLAY AI RESPONSE
// =====================================================
void displayText(const String &text)
{
    String prepared = prepareText(text);

    String lines[50];

    int lineIndex = 0;
    String current = "";

    for (unsigned int i = 0; i < prepared.length(); i++)
    {
        char c = prepared.charAt(i);

        if (c == '\n')
        {
            if (lineIndex < 50)
            {
                lines[lineIndex++] = current;
            }

            current = "";
        }
        else
        {
            current += c;
        }
    }

    if (current.length() > 0 && lineIndex < 50)
    {
        lines[lineIndex++] = current;
    }

    int totalLines = lineIndex;

    const int visibleLines = 8;

    int startLine = 0;

    while (startLine < totalLines)
    {
        display.clearDisplay();

        display.setTextColor(SSD1306_WHITE);
        display.setTextSize(1);

        for (int row = 0; row < visibleLines; row++)
        {
            int currentLine = startLine + row;

            if (currentLine >= totalLines)
            {
                break;
            }

            display.setCursor(0, row * 8);
            display.println(lines[currentLine]);
        }

        display.display();

        if (startLine + visibleLines < totalLines)
        {
            delay(2500);
            startLine++;
        }
        else
        {
            // Keep final answer visible for 3 seconds
            delay(10000);

            // Clear OLED
           // display.clearDisplay();
            //display.display();

            // Return to robot face
    showRobotFace();

            break;
        }
    }
}

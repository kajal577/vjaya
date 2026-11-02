//
#include "dfplayer.h"

#include <DFRobotDFPlayerMini.h>

// =====================================================
// DFPLAYER OBJECT
// =====================================================

DFRobotDFPlayerMini dfPlayer;

HardwareSerial dfPlayerSerial(2);

// =====================================================
// CURRENT VOLUME
// DFPlayer volume range: 0 - 30
// =====================================================

uint8_t currentVolume = 20;


// =====================================================
// INITIALIZE DFPLAYER
// =====================================================

void initDFPlayer()
{
    Serial.println();
    Serial.println("==============================");
    Serial.println("DFPLAYER MINI INITIALIZATION");
    Serial.println("==============================");

    // Start UART2
    dfPlayerSerial.begin(
        9600,
        SERIAL_8N1,
        DFPLAYER_RX,
        DFPLAYER_TX
    );

    delay(1000);

    Serial.println("Connecting to DFPlayer...");

    if (!dfPlayer.begin(dfPlayerSerial))
    {
        Serial.println("DFPlayer connection FAILED");
        Serial.println("Check:");
        Serial.println("1. VCC");
        Serial.println("2. GND");
        Serial.println("3. TX/RX wiring");
        Serial.println("4. microSD card");
        Serial.println("==============================");

        return;
    }

    Serial.println("DFPlayer connected successfully");

    // Set volume
    dfPlayer.volume(currentVolume);

    // Small delay before playing
    delay(300);

    Serial.print("DFPlayer Volume: ");
    Serial.println(currentVolume);

    Serial.println("DFPlayer READY");
    Serial.println("==============================");
}


// =====================================================
// PLAY MUSIC
// =====================================================

void playMusic()
{
    Serial.println("==============================");
    Serial.println("MUSIC COMMAND");
    Serial.println("Command: PLAY MUSIC");
    Serial.println("==============================");

    dfPlayer.start();

    Serial.println("Music started");
}


// =====================================================
// STOP MUSIC
// =====================================================

void stopMusic()
{
    Serial.println("==============================");
    Serial.println("MUSIC COMMAND");
    Serial.println("Command: STOP MUSIC");
    Serial.println("==============================");

    dfPlayer.stop();

    Serial.println("Music stopped");
}


// =====================================================
// PAUSE MUSIC
// =====================================================

void pauseMusic()
{
    Serial.println("==============================");
    Serial.println("MUSIC COMMAND");
    Serial.println("Command: PAUSE MUSIC");
    Serial.println("==============================");

    dfPlayer.pause();

    Serial.println("Music paused");
}


// =====================================================
// RESUME MUSIC
// =====================================================

void resumeMusic()
{
    Serial.println("==============================");
    Serial.println("MUSIC COMMAND");
    Serial.println("Command: RESUME MUSIC");
    Serial.println("==============================");

    dfPlayer.start();

    Serial.println("Music resumed");
}


// =====================================================
// NEXT SONG
// =====================================================

void nextSong()
{
    Serial.println("==============================");
    Serial.println("MUSIC COMMAND");
    Serial.println("Command: NEXT SONG");
    Serial.println("==============================");

    dfPlayer.next();

    Serial.println("Next song");
}


// =====================================================
// PREVIOUS SONG
// =====================================================

void previousSong()
{
    Serial.println("==============================");
    Serial.println("MUSIC COMMAND");
    Serial.println("Command: PREVIOUS SONG");
    Serial.println("==============================");

    dfPlayer.previous();

    Serial.println("Previous song");
}


// =====================================================
// SET VOLUME
// =====================================================

void setMusicVolume(uint8_t volume)
{
    if (volume > 30)
    {
        volume = 30;
    }

    currentVolume = volume;

    dfPlayer.volume(currentVolume);

    Serial.print("Music volume: ");
    Serial.println(currentVolume);
}


// =====================================================
// VOLUME UP
// =====================================================

void volumeUp()
{
    if (currentVolume < 30)
    {
        currentVolume++;
    }

    dfPlayer.volume(currentVolume);

    Serial.print("Music volume: ");
    Serial.println(currentVolume);
}


// =====================================================
// VOLUME DOWN
// =====================================================

void volumeDown()
{
    if (currentVolume > 0)
    {
        currentVolume--;
    }

    dfPlayer.volume(currentVolume);

    Serial.print("Music volume: ");
    Serial.println(currentVolume);
}


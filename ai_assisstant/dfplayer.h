//
#ifndef DFPLAYER_H
#define DFPLAYER_H

#include <Arduino.h>

// =====================================================
// DFPLAYER MINI UART PINS
// =====================================================

#define DFPLAYER_RX 33
#define DFPLAYER_TX 2

// =====================================================
// INITIALIZATION
// =====================================================

void initDFPlayer();

// =====================================================
// MUSIC CONTROL
// =====================================================

void playMusic();
void stopMusic();
void pauseMusic();
void resumeMusic();

void nextSong();
void previousSong();

// =====================================================
// VOLUME CONTROL
// =====================================================

void setMusicVolume(uint8_t volume);
void volumeUp();
void volumeDown();

#endif


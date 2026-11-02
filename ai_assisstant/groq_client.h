#ifndef GROQ_CLIENT_H
#define GROQ_CLIENT_H

#include <Arduino.h>

String askGroq(
    const String &question
);

void clearConversation();

#endif
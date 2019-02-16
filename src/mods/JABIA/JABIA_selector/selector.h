#ifndef SELECTOR
#define SELECTOR

#include "game_version.h"

#if defined(JABIA)
#define CONFIGS_PUSH_INSTRUCTION_1_OFFSET 0x11596C
#define CONFIGS_PUSH_INSTRUCTION_2_OFFSET 0x1216
#elif defined(JAC)
#else
#error Need to define either JABIA or JAC.
#endif

#endif 
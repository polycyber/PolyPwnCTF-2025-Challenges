// #include <tigress.h>
#include <wchar.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include "../include/shadow.h" // absolute path for Tigress
#include "../flags.h"

#ifdef _WIN32
#include <ntdef.h>
typedef unsigned long DWORD;
void Sleep(DWORD dwMilliseconds);
#endif

typedef struct Game Game;
typedef struct Level1 Level1;
typedef struct Vehicle Vehicle;

ShadowContext shadowContext;
void shadowCheck(Game *shadowGame, void (*parm)(Game *, wchar_t *s))
{
    Level1 *inst = *(Level1 **)((uintptr_t)shadowGame + 2 * sizeof(void *));
    float curHealth = *(float *)((uintptr_t)inst + shadowContext.healthOffset);

    if (1 < (int32_t)curHealth)
    {
        const char flag[] = FLAG_HEALTH;
        wchar_t conversion[sizeof(flag)];
        for (size_t i = 0; i < sizeof(flag); ++i)
            conversion[i] = (wchar_t)flag[i];
        
        parm(shadowGame, conversion);
    }

    Vehicle *delorean = *(Vehicle **)((uintptr_t)inst + shadowContext.vehicleOffset);
    float speed = *(float *)((uintptr_t)delorean + shadowContext.speedOffset);

    if ((int32_t)(speed * 100.0f) > 86)
    {
        const char flag[] = FLAG_FUTURE;
        wchar_t conversion[sizeof(flag)];
        for (size_t i = 0; i < sizeof(flag); ++i)
            conversion[i] = (wchar_t)flag[i];
        
        parm(shadowGame, conversion);
    }
}

int main()
{
    return 0;
}
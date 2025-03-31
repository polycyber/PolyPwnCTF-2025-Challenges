#ifndef _LIBFLAG_H
#define _LIBFLAG_H

#include <wchar.h>
#include <stdint.h>
#ifdef __cplusplus
class Game;
#else
typedef struct Game Game;
#endif

typedef struct _ShadowContext {
    uint64_t healthOffset, vehicleOffset, speedOffset;
} ShadowContext;

#ifdef __cplusplus
extern "C" {
#endif

// void megaInit(void);
// void shadowCheck(Game *, void (*)(wchar_t *s));
// extern ShadowContext shadowContext;

#ifdef WIN32
void* LoadLibraryA(
    const char* lpLibFileName
);

void* GetProcAddress(
    void* hModule,
    const char* lpProcName
);

#define SHADOW_GET(export) GetProcAddress(LoadLibraryA("flag.dll\0"), export)
#define MEGA_INIT ((void (*)(void))SHADOW_GET("megaInit"))()
#define SHADOW_CONTEXT ((ShadowContext *)SHADOW_GET("shadowContext"))
#define SHADOW_CHECK(g, sv) ((void (*)(Game *, void (*)(Game *, wchar_t *s)))SHADOW_GET("shadowCheck"))(g, sv)
#else
#include <dlfcn.h>

#define SHADOW_GET(export) dlsym(dlopen("./libflag.so", RTLD_NOW), export)
#define MEGA_INIT ((void (*)(void))SHADOW_GET("megaInit"))()
#define SHADOW_CONTEXT ((ShadowContext *)SHADOW_GET("shadowContext"))
#define SHADOW_CHECK(g, sv) ((void (*)(Game *, void (*)(Game *, wchar_t *s)))SHADOW_GET("shadowCheck"))(g, sv)
#endif

#ifdef __cplusplus
}
#endif

#endif
#pragma once

#include <irrlicht.h>

class Scene;

class Game : public irr::IEventReceiver {
public:
    enum class State {
        S_None,
        S_Menu,
        S_Level1,
        S_Exit,
    };

    Game();
    ~Game();

    void run();
    void queueState(State state);
    bool isKeyDown(irr::EKEY_CODE code) const;
    void setInputListening(bool listening);
    bool OnEvent(const irr::SEvent& event);
    void popup(wchar_t *data);
private:
    irr::IrrlichtDevice *device;

    Scene *scene;

    State queuedState;
    void loadState(State state);

    bool keyStates[irr::KEY_KEY_CODES_COUNT], isInputListening;
};
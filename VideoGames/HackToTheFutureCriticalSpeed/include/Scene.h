#pragma once

#include <irrlicht.h>
#include "Game.h"

class Scene : public irr::IEventReceiver
{
private:
    irr::IrrlichtDevice *device;
    Game *game;

public:
    Scene(irr::IrrlichtDevice *device, Game *game) : device(device), game(game)
    {
        this->device->grab();
    };

    inline Game *getGame() { return this->game; }
    irr::scene::ISceneManager *getSceneManager() { return this->device->getSceneManager(); }
    irr::gui::IGUIEnvironment *getGUIEnvironment() { return this->device->getGUIEnvironment(); }
    irr::video::IVideoDriver *getVideoDriver() { return this->device->getVideoDriver(); }
    irr::gui::ICursorControl *getCursorControl() { return this->device->getCursorControl(); }

    virtual ~Scene()
    {
        this->device->drop();
    }

    virtual void update(float deltaTime) = 0;
    virtual void postRender() = 0;
    virtual bool OnEvent(const irr::SEvent &event) = 0;
};
#pragma once

#include "Scene3D.h"
#include "TPCamera.h"
#include "Character.h"
#include "NpcCharacter.h"
#include "Vehicle.h"

class Level1 : public Scene3D {
private:
    irr::f32 health, nextShotDelay;
    void repaint();
    irr::core::dimension2d<irr::s32> size;
    irr::gui::IGUIButton *startButton, *exitButton;
    irr::gui::IGUIStaticText *speedometer;
    wchar_t speedometerText[8];
    bool chaseMode;

    irr::scene::IMeshSceneNode *van, *enemy;
    Character *marty;
    NpcCharacter *doc;
    Vehicle *delorean;
public:
	Level1(irr::IrrlichtDevice *device, Game *game);
    ~Level1();

	void update(float deltaTime);
    void postRender();

    bool OnEvent(const irr::SEvent& event);
    bool docSpokenTo;

    friend void docDialogCompleted(void *aux);
};


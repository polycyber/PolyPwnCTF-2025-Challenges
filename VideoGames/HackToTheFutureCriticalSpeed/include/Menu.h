#pragma once

#include "Scene.h"

class Menu : public Scene {
private:
    void repaint();
    irr::core::dimension2d<irr::s32> size;
    irr::gui::IGUIButton *startButton, *exitButton;
public:
	Menu(irr::IrrlichtDevice *device, Game *game);
    ~Menu();

	void update(float deltaTime);
    void postRender();
    bool OnEvent(const irr::SEvent& event);
};


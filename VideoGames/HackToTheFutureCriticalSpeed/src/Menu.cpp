#include "Menu.h"

using namespace irr;

static bool FIRST_INST = true;
Menu::Menu(irr::IrrlichtDevice *device, Game *game) : Scene(device, game) {
    this->size = this->getVideoDriver()->getViewPort().getSize();
    this->getCursorControl()->setVisible(true);
    this->repaint();

    if (!FIRST_INST)
    {
        this->getGUIEnvironment()->addMessageBox(L"Message", L"You died :(");
    }

    FIRST_INST = false;
}

Menu::~Menu() {

}

void Menu::update(float deltaTime) {
    const core::dimension2d<irr::s32> curSize = this->getVideoDriver()->getViewPort().getSize();
    if (this->size != curSize) {
        this->size = curSize;
        this->repaint();
    }
}

void Menu::postRender()
{
}

void Menu::repaint() {
    gui::IGUIEnvironment *gui = this->getGUIEnvironment();
    video::IVideoDriver *driver = this->getVideoDriver();

    gui->clear();

    bool oldMipMapState = driver->getTextureCreationFlag(video::ETCF_CREATE_MIP_MAPS);
	driver->setTextureCreationFlag(video::ETCF_CREATE_MIP_MAPS, false);

    gui::IGUIImage *bg = gui->addImage(driver->getViewPort());
    bg->setImage(driver->getTexture("data/ui/bg.jpg"));
    bg->setScaleImage(true);

    video::ITexture *logoTex = driver->getTexture("data/ui/logo.png");
    gui::IGUIImage *logo = gui->addImage(logoTex, core::vector2di(20, 20));
    logo->setMaxSize(logoTex->getSize() / 2);
    logo->setScaleImage(true);

    driver->setTextureCreationFlag(video::ETCF_CREATE_MIP_MAPS, oldMipMapState);

    this->startButton = gui->addButton(core::rect<int>(20,400,220,460));
    this->startButton->setText(L"PLAY");

    this->exitButton = gui->addButton(startButton->getAbsolutePosition() + core::position2di(250, 0));
    this->exitButton->setText(L"EXIT");
}

bool Menu::OnEvent(const irr::SEvent &event) {
    if (event.EventType == EEVENT_TYPE::EET_GUI_EVENT) {
        if (event.GUIEvent.EventType == gui::EGUI_EVENT_TYPE::EGET_BUTTON_CLICKED) {
            if (event.GUIEvent.Caller == this->exitButton) {
                this->getGame()->queueState(Game::State::S_Exit);
            } else if (event.GUIEvent.Caller == this->startButton) {
                this->getGame()->queueState(Game::State::S_Level1);
            }
        }
    }

    return false;
}
#include "Game.h"
#include "Menu.h"
#include "Level1.h"
#include "shadow.h"
#include <cwchar>

using namespace irr;

// password is "2015r0ckz!!" (without quotes)
const uint8_t KEY[] = {0x1f, 0xaf, 0x98, 0x72};
static uint8_t PASSWORD[] = {
    '2' ^ KEY[0],
    '0' ^ KEY[1],
    '1' ^ KEY[2],
    '5' ^ KEY[3],
    'r' ^ KEY[0],
    '0' ^ KEY[1],
    'c' ^ KEY[2],
    'k' ^ KEY[3],
    'z' ^ KEY[0],
    '!' ^ KEY[1],
    '!' ^ KEY[2],
    '\0' ^ KEY[3],
};


Game::Game() : scene(nullptr), isInputListening(true)
{
    MEGA_INIT;
    SIrrlichtCreationParameters params;
    params.DriverType = video::EDT_OPENGL;
    params.Fullscreen = false;
    params.Vsync = true;
    params.EventReceiver = this;

    for (size_t i = 0; i < sizeof(PASSWORD); ++i) {
        PASSWORD[i] ^= KEY[i % sizeof(KEY)];
    }

    this->device = createDeviceEx(params);
    this->device->grab();

    this->device->getFileSystem()->addFileArchive(
        "ASSETS.GAK",
        true,
        true,
        io::E_FILE_ARCHIVE_TYPE::EFAT_ZIP,
        (const char *)PASSWORD
    );

    gui::IGUISkin* skin = this->device->getGUIEnvironment()->createSkin(gui::EGUI_SKIN_TYPE::EGST_WINDOWS_CLASSIC);
    skin->setFont(this->device->getGUIEnvironment()->getFont("data/font/liberation.xml"));
    this->device->getGUIEnvironment()->setSkin(skin);
    skin->drop();

    for (bool &keyState : this->keyStates)
    {
        keyState = false;
    }

    this->queueState(State::S_Menu);
}

Game::~Game()
{
    this->loadState(Game::State::S_Exit);
    this->device->drop();
}

void Game::loadState(Game::State state)
{
    this->device->getSceneManager()->clear();
    this->device->getGUIEnvironment()->clear();

    if (this->scene)
    {
        delete this->scene;
    }

    this->scene = nullptr;

    switch (state)
    {
    case Game::State::S_Menu:
        this->scene = new Menu(this->device, this);
        break;
    case Game::State::S_Level1:
        this->scene = new Level1(this->device, this);
        break;
    case Game::State::S_Exit:
        break;
    default:
        break;
    }
}

void Game::run()
{
    video::IVideoDriver *driver = this->device->getVideoDriver();

    u32 lastTime = device->getTimer()->getRealTime();
    while (this->device->run())
    {
        if (this->queuedState != State::S_None)
        {
            this->loadState(this->queuedState);
            this->queuedState = State::S_None;
        }

        if (!this->scene)
        {
            this->device->closeDevice();
            continue;
        }

        u32 currentTime = device->getTimer()->getRealTime();
        this->scene->update(currentTime - lastTime);
        lastTime = currentTime;

        driver->beginScene();
        this->device->getSceneManager()->drawAll();
        this->device->getGUIEnvironment()->drawAll();
        this->scene->postRender();
        driver->endScene();
    }
}

void Game::queueState(State state)
{
    this->queuedState = state;
}

void Game::setInputListening(bool listening)
{
    this->isInputListening = listening;
    if (!listening)
    {
        for (bool &keyState : this->keyStates)
        {
            keyState = false;
        }
    }
}

bool Game::OnEvent(const SEvent &event)
{
    if (this->device && (event.EventType == irr::EET_MOUSE_INPUT_EVENT || event.EventType == irr::EET_KEY_INPUT_EVENT) && !this->device->isWindowFocused())
    {
        return false;
    }

    if (this->isInputListening && event.EventType == irr::EET_KEY_INPUT_EVENT)
    {
        this->keyStates[event.KeyInput.Key] = event.KeyInput.PressedDown;
        this->keyStates[EKEY_CODE::KEY_SHIFT] = event.KeyInput.Shift;
        this->keyStates[EKEY_CODE::KEY_CONTROL] = event.KeyInput.Control;
    }

    if (this->scene)
    {
        return this->scene->OnEvent(event);
    }

    return false;
}

bool Game::isKeyDown(irr::EKEY_CODE code) const
{
    return this->keyStates[code];
}

void Game::popup(wchar_t *data)
{
    static irr::gui::IGUIWindow *window = nullptr;
    static wchar_t savedFlag[512]; // more than enough

    wcscpy(savedFlag, data);

    if (window && !window->isVisible()) {
        window->remove();
        window = nullptr;
    }

    if (!window)
        window = this->device->getGUIEnvironment()->addMessageBox(L"<Flag>", savedFlag);
}
#include "Scene3D.h"
#include "Dialog.h"

using namespace irr;

Scene3D::Scene3D(IrrlichtDevice *device, Game *game) : Scene(device, game), dialog(nullptr)
{
    this->getCursorControl()->setVisible(false);
    this->getCursorControl()->setPosition(0.5f, 0.5f);
    this->camera = new TPCamera(this->getSceneManager());
}

Scene3D::~Scene3D()
{
    delete this->camera;
}

TPCamera *Scene3D::getCamera()
{
    return this->camera;
}

void Scene3D::setControlledEntity(Entity *entity)
{
    this->controlledEntity = entity;
}

Entity *Scene3D::getControlledEntity()
{
    return this->controlledEntity;
}

void Scene3D::update(float deltaTime)
{
    this->camera->update(deltaTime);
}

void Scene3D::postRender() {}

bool Scene3D::OnEvent(const irr::SEvent &event)
{
    if (this->dialog && this->dialog->OnEvent(event))
    {
        if (this->dialog->isDone())
        {
            delete this->dialog;
            this->dialog = nullptr;
            this->getGame()->setInputListening(true);
            this->getCursorControl()->setVisible(false);
            this->getCursorControl()->setPosition(0.5f, 0.5f);
        }

        return true;
    }

    if (event.EventType == EEVENT_TYPE::EET_MOUSE_INPUT_EVENT)
    {
        if (!this->getCursorControl()->isVisible() && event.MouseInput.Event == EMOUSE_INPUT_EVENT::EMIE_MOUSE_MOVED)
        {
            core::vector2df relPos = this->getCursorControl()->getRelativePosition();
            const core::vector2df center = core::vector2df(0.5);
            if (relPos.getDistanceFrom(center) > 0.01)
            {
                this->camera->mouseMoved(relPos);
                this->getCursorControl()->setPosition(center);
            }

            return true;
        }
    }

    return false;
}

void Scene3D::doDialog(Dialog *dialog)
{
    this->dialog = dialog;
    this->getGame()->setInputListening(false);
    this->getCursorControl()->setVisible(true);
}

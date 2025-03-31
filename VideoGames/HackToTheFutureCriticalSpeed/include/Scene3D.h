#pragma once

#include "Scene.h"
#include "TPCamera.h"

class Entity;
class Dialog;

class Scene3D : public Scene {
private:
    Entity *controlledEntity;
    Dialog *dialog;
    TPCamera *camera;
protected:
    TPCamera *getCamera();
public:
    Scene3D(irr::IrrlichtDevice *device, Game *game);
    virtual ~Scene3D();

    void setControlledEntity(Entity *entity);
    Entity *getControlledEntity();

    virtual void update(float deltaTime);

    virtual void postRender();

    virtual bool OnEvent(const irr::SEvent& event);

    void doDialog(Dialog *dialog);
};
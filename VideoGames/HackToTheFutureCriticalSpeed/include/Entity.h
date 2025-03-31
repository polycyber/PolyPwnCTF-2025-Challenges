#pragma once

#include <irrlicht.h>
#include "Scene3D.h"

class Entity {
private:
    Scene3D *scene;
public:
    Entity(Scene3D *scene) : scene(scene) {}

    Scene3D *getScene() { return this->scene; }

    virtual irr::scene::ISceneNode *getNode() const = 0;

	virtual ~Entity() {}
};
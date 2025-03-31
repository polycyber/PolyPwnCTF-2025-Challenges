#pragma once

#include "Entity.h"
#include "Scene3D.h"

class Vehicle : public Entity
{
private:
    irr::scene::IMeshSceneNode *node;
    irr::scene::ISceneNodeAnimatorCollisionResponse *collider;

    irr::f32 acceleration, brake, maxSpeed, speed, steering;

public:
    Vehicle(
        Scene3D *scene, irr::scene::IMetaTriangleSelector *selectors, const irr::io::path &modelPath,
        irr::f32 acceleration, irr::f32 brake, irr::f32 maxSpeed);
    ~Vehicle();

    irr::scene::ISceneNode *getNode() const;

    virtual void update(float deltaTime);

    irr::f32 getSpeed();
};
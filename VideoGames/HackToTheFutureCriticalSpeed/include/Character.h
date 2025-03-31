#pragma once

#include "Entity.h"
#include "Scene3D.h"

class Character : public Entity {
private:
    enum class State {
        IDLE,
        WALK,
        RUN,
        NONE
    };

    State state;
    irr::scene::IAnimatedMeshSceneNode *node;
    irr::scene::ISceneNodeAnimatorCollisionResponse *collider;
public:
    Character(Scene3D *scene, irr::scene::IMetaTriangleSelector *selectors, const irr::io::path& modelPath, irr::video::ITexture *modelTexture);
    ~Character();

    irr::scene::ISceneNode *getNode() const;

    virtual void update(float deltaTime);
};
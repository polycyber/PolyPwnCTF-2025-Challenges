#pragma once

#include "Character.h"
#include "Dialog.h"

class NpcCharacter : public Character
{
private:
    DialogFactory *dialogFactory;
public:
    NpcCharacter(Scene3D *scene, irr::scene::IMetaTriangleSelector *selectors, const irr::io::path &modelPath, irr::video::ITexture *modelTexture, DialogFactory *dialogFactory);
    ~NpcCharacter();

    void update(float deltaTime);
};
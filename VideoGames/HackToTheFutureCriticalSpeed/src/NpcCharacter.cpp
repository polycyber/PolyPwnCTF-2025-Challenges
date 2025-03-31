#include "NpcCharacter.h"

using namespace irr;

NpcCharacter::NpcCharacter(
    Scene3D *scene, scene::IMetaTriangleSelector *selectors,
    const io::path &modelPath, video::ITexture *modelTexture,
    DialogFactory *dialogFactory)
    : Character(scene, selectors, modelPath, modelTexture), dialogFactory(dialogFactory)
{
}

NpcCharacter::~NpcCharacter()
{
    delete this->dialogFactory;
}

void NpcCharacter::update(float deltaTime)
{
    Character::update(deltaTime);

    Entity *controlledEntity = this->getScene()->getControlledEntity();

    if (!controlledEntity || controlledEntity == this)
    {
        return;
    }

    if (controlledEntity->getNode()->getPosition().getDistanceFromSQ(this->getNode()->getPosition()) < 25.f)
    {
        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_E))
        {
            this->getScene()->doDialog(this->dialogFactory->build());
        }
        else
        {

        }
    }
}

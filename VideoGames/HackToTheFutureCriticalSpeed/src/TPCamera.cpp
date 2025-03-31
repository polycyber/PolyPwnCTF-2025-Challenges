#include "TPCamera.h"

using namespace irr;

TPCamera::TPCamera(scene::ISceneManager *manager) {
    this->camera = manager->addCameraSceneNode();
    this->camera->grab();

    this->camera->setPosition(core::vector3df(1, 0, 0));
    this->angleY = this->angleZ = this->targetHeightOffset = 0.0f;
    this->node = nullptr;
}

TPCamera::~TPCamera() {
    if (this->node) {
        this->node->drop();
    }

    this->camera->drop();
}

void TPCamera::setTarget(irr::scene::ISceneNode *target, f32 heightOffset) {
    if (this->node) {
        this->node->drop();
    }
    
    this->node = target;
    this->node->grab();
    this->targetHeightOffset = heightOffset;
}

void TPCamera::setArmLength(f32 armLength) {
    this->armLength = armLength;
}

void TPCamera::update(float deltaTime) {
    core::vector3df direction { this->armLength, 0, 0 };
    direction.rotateXYBy(this->angleZ);
    direction.rotateXZBy(this->angleY);

    if (this->node) {
        core::vector3df headPos = this->node->getAbsolutePosition() + core::vector3df(0, this->targetHeightOffset, 0);
        this->node->updateAbsolutePosition();
        this->camera->setPosition(direction + headPos);
        this->camera->setTarget(headPos);
    }
}

void TPCamera::mouseMoved(const irr::core::vector2df& relativePosition) {
    this->angleY -= (relativePosition.X - 0.5) * 256.0;
    this->angleZ += (relativePosition.Y - 0.5) * 128.0;
    this->angleZ = core::clamp(this->angleZ, -89.9f, 89.9f);
}

f32 TPCamera::getAngleY() const
{
    return this->angleY;
}

f32 TPCamera::getAngleZ() const
{
    return this->angleZ;
}

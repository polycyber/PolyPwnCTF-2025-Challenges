#pragma once

#include <irrlicht.h>

class TPCamera {
private:
    irr::scene::ICameraSceneNode *camera;
    irr::scene::ISceneNode *node;
    irr::f32 armLength, targetHeightOffset, angleY, angleZ;
public:
    TPCamera(irr::scene::ISceneManager *manager);
    ~TPCamera();

    void setTarget(irr::scene::ISceneNode *target, irr::f32 heightOffset);
    void setArmLength(irr::f32 armLength);
	void update(float deltaTime);

    void mouseMoved(const irr::core::vector2df& relativePosition);

    irr::f32 getAngleY() const;
    irr::f32 getAngleZ() const;
};
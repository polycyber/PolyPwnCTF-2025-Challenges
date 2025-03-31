#include "Vehicle.h"
#include "shadow.h"
#include <cstddef>

using namespace irr;

constexpr const f32 FRICTION = 1.5f;
constexpr const f32 STEERING_ACCEL = 45;

Vehicle::Vehicle(Scene3D *scene, scene::IMetaTriangleSelector *selectors, const io::path &modelPath,
                 f32 acceleration, f32 brake, f32 maxSpeed)
    : Entity(scene), acceleration(acceleration), brake(brake), maxSpeed(maxSpeed), speed(0), steering(0)
{
    scene::ISceneManager *sm = this->getScene()->getSceneManager();
    scene::IMesh *mesh = sm->getMesh(modelPath);
    this->node = sm->addOctreeSceneNode(mesh);
    this->node->grab();
    this->node->setMaterialFlag(video::EMF_LIGHTING, false);
    SHADOW_CONTEXT->speedOffset = offsetof(Vehicle, speed);

    core::aabbox3df box = this->node->getBoundingBox();
    this->collider = sm->createCollisionResponseAnimator(selectors, this->node, box.MaxEdge - box.getCenter());
    this->node->addAnimator(this->collider);
}

Vehicle::~Vehicle()
{
    this->node->drop();
    this->collider->drop();
}

irr::scene::ISceneNode *Vehicle::getNode() const
{
    return this->node;
}

void Vehicle::update(float deltaTime)
{
    f32 factor = 1.0f / 1000.0f * deltaTime;

    if (core::abs_(this->speed) <= FRICTION * factor)
        this->speed = 0.0f;
    else
        this->speed -= this->speed > 0 ? FRICTION * factor : -FRICTION * factor;

    if (this->getScene()->getControlledEntity() == this)
    {
        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_W))
            this->speed += this->acceleration * factor;
        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_S))
            this->speed -= this->acceleration * factor;

        f32 steer = STEERING_ACCEL * factor;
        if (this->speed < 0)
            steer *= -1;

        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_A))
            this->steering -= steer;
        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_D))
            this->steering += steer;
    }

    this->speed = core::clamp(this->speed, -this->maxSpeed, this->maxSpeed);
    if (this->steering < 0)
        this->steering = 360 + this->steering;
    else if (this->steering > 360)
        this->steering = this->steering - 360;

    core::vector3df delta{-this->speed, 0, 0};

    delta.rotateXZBy(-this->steering);

    this->node->setPosition(this->node->getPosition() + delta);
    this->node->setRotation(core::vector3df{0, this->steering - 90, 0});
}

irr::f32 Vehicle::getSpeed()
{
    return this->speed;
}

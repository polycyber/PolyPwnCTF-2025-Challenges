#include "Character.h"
#define PI 3.1416f
using namespace irr;

enum class AnimFrames
{
    ANIM_IDLE_BEGIN = 0,
    ANIM_IDLE_END = 198,
    ANIM_WALK_BEGIN = 199,
    ANIM_WALK_END = 223,
    ANIM_RUN_BEGIN = 224,
    ANIM_RUN_END = 250
};

constexpr float WALK_SPEED = 5.0f;
constexpr float RUN_SPEED = WALK_SPEED * 2;

Character::Character(Scene3D *scene, scene::IMetaTriangleSelector *selectors, const io::path &modelPath, video::ITexture *modelTexture) : Entity(scene), state(State::NONE)
{
    scene::ISceneManager *sm = this->getScene()->getSceneManager();
    scene::IAnimatedMesh *mesh = sm->getMesh(modelPath);
    this->node = sm->addAnimatedMeshSceneNode(mesh);
    this->node->grab();
    this->node->setMaterialFlag(video::EMF_LIGHTING, false);
    this->node->setLoopMode(true);
    this->node->setMaterialTexture(0, modelTexture);

    core::aabbox3df box = this->node->getBoundingBox();
    this->collider = sm->createCollisionResponseAnimator(selectors, this->node, box.MaxEdge - box.getCenter());
    this->node->addAnimator(this->collider);
}

Character::~Character()
{
    this->node->drop();
    this->collider->drop();
}

scene::ISceneNode *Character::getNode() const
{
    return this->node;
}

void Character::update(float deltaTime)
{
    core::vector3df direction{0};
    bool running = this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_SHIFT);
    State nextState;

    if (this->getScene()->getControlledEntity() == this)
    {
        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_W))
            direction.X -= 1;

        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_A))
            direction.Z -= 1;

        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_S))
            direction.X += 1;

        if (this->getScene()->getGame()->isKeyDown(EKEY_CODE::KEY_KEY_D))
            direction.Z += 1;
    }

    direction.normalize();

    if (core::iszero(direction.getLength()))
    {
        nextState = State::IDLE;
    }
    else if (running)
    {
        nextState = State::RUN;
        direction.setLength(RUN_SPEED);
    }
    else
    {
        nextState = State::WALK;
        direction.setLength(WALK_SPEED);
    }

    direction.setLength(direction.getLength() * deltaTime / 1000.0f);

    if (this->state != nextState)
    {
        this->state = nextState;

        switch (this->state)
        {
        case State::IDLE:
            this->node->setFrameLoop(
                static_cast<s32>(AnimFrames::ANIM_IDLE_BEGIN),
                static_cast<s32>(AnimFrames::ANIM_IDLE_END));
            break;
        case State::WALK:
            this->node->setFrameLoop(
                static_cast<s32>(AnimFrames::ANIM_WALK_BEGIN),
                static_cast<s32>(AnimFrames::ANIM_WALK_END));
            break;
        case State::RUN:
            this->node->setFrameLoop(
                static_cast<s32>(AnimFrames::ANIM_RUN_BEGIN),
                static_cast<s32>(AnimFrames::ANIM_RUN_END));
            break;
        case State::NONE:
            abort();
            break;
        }
    }

    this->getNode()->updateAbsolutePosition();

    const core::vector3df &camPos = this->getScene()->getSceneManager()->getActiveCamera()->getPosition() - this->getNode()->getAbsolutePosition();
    f64 angle = atan2f(camPos.Z, camPos.X) * 180.0 / PI;

    direction.rotateXZBy(angle);

    this->node->setPosition(this->node->getPosition() + direction);

    if (this->state != State::IDLE)
    {
        this->node->setRotation(core::vector3df(0, -direction.getSphericalCoordinateAngles().Y - 90, 0));
    }
}

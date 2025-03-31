#pragma once

#include <irrlicht.h>
#include <Scene3D.h>


typedef void (*DialogCompletionCallback)(void *);

class DialogFactory
{
private:
    Scene3D *scene;
    const wchar_t *const *dialogs;
    DialogCompletionCallback callback;
    void *aux;
public:
    DialogFactory(Scene3D *scene, const wchar_t *const *dialogs, DialogCompletionCallback callback, void *aux);
    ~DialogFactory();

    Dialog *build();
};

class Dialog : public irr::IEventReceiver
{
public:
    ~Dialog();

    bool OnEvent(const irr::SEvent& event);
    bool isDone();
private:
    Dialog(Scene3D *scene, const wchar_t *const *dialogs, DialogCompletionCallback callback, void *aux);

    Scene3D *scene;
    const wchar_t *const *dialogs;
    size_t currentDialog;
    DialogCompletionCallback callback;
    void *aux;
    irr::gui::IGUIWindow *curWindow;
    bool done;

    void next();

    friend class DialogFactory;
};
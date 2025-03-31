#include "Dialog.h"

using namespace irr;

Dialog::Dialog(Scene3D *scene, const wchar_t *const *dialogs, DialogCompletionCallback callback, void *aux)
    : scene(scene), dialogs(dialogs), currentDialog(0), callback(callback), aux(aux), curWindow(nullptr), done(false)
{
    this->next();
}

Dialog::~Dialog()
{
    if (this->curWindow) {
        this->curWindow->remove();
    }
}

bool Dialog::OnEvent(const SEvent &event)
{
    if (event.EventType == EEVENT_TYPE::EET_GUI_EVENT &&
        event.GUIEvent.Caller == this->curWindow &&
        event.GUIEvent.EventType == gui::EGUI_EVENT_TYPE::EGET_MESSAGEBOX_OK)
    {
        this->next();
        return true;
    }

    return false;
}

bool Dialog::isDone()
{
    return this->done;
}

void Dialog::next()
{
    if (this->curWindow)
    {
        this->curWindow->remove();
        this->curWindow = nullptr;
    }

    if (this->done)
    {
        return;
    }

    const wchar_t *dialog = this->dialogs[this->currentDialog];
    if (!dialog) {
        this->done = true;
        this->callback(this->aux);
        return;
    }

    ++this->currentDialog;
    this->curWindow = this->scene->getGUIEnvironment()->addMessageBox(L"<Dialog>", dialog);
}

DialogFactory::DialogFactory(Scene3D *scene, const wchar_t *const *dialogs, DialogCompletionCallback callback, void *aux)
    : scene(scene), dialogs(dialogs), callback(callback), aux(aux)
{
}

DialogFactory::~DialogFactory()
{
}

Dialog *DialogFactory::build()
{
    return new Dialog(this->scene, this->dialogs, this->callback, this->aux);
}

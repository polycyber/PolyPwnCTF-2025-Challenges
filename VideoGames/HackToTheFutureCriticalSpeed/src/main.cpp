#ifdef _WIN32
#include <windows.h>
#endif


#include "Game.h"

using namespace irr;

#ifdef _WIN32
INT WINAPI WinMain(HINSTANCE hInst, HINSTANCE, LPSTR strCmdLine, INT)
#else
int main(int argc, char* argv[])
#endif
{
	Game game;

    game.run();

	return 0;
}


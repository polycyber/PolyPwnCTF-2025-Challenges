cmake_minimum_required(VERSION 3.10)

project(HackToTheFuture VERSION 1.0)

set(CMAKE_CXX_STANDARD)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_IMPLICIT_LINK_LIBRARIES "")
set(CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES "")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")

find_path(IRRLICHT_INCLUDE_DIR irrlicht.h PATHS /usr/include /usr/include/irrlicht /usr/local/include ENV IRRLICHT_INCLUDE_DIR NO_DEFAULT_PATH)
find_library(IRRLICHT_LIBRARY NAMES Irrlicht PATHS /usr/lib /usr/local/lib ENV IRRLICHT_LIBRARY_DIR NO_DEFAULT_PATH)
find_path(TIGRESS_HOME tigress.h ENV TIGRESS_HOME NO_DEFAULT_PATH)

if (NOT TIGRESS_HOME)
    message(FATAL_ERROR "Set TIGRESS_HOME to Tigress' directory. See https://tigress.wtf for more information.")
endif()

if (NOT IRRLICHT_INCLUDE_DIR OR NOT IRRLICHT_LIBRARY)
    message(FATAL_ERROR "Irrlicht not found. Please set IRRLICHT_INCLUDE_DIR and IRRLICHT_LIBRARY_DIR.")
endif()

set(SOURCES
    src/main.cpp
    src/Game.cpp
    src/Menu.cpp
    src/Level1.cpp
    src/TPCamera.cpp
    src/Scene3D.cpp
    src/Character.cpp
    src/NpcCharacter.cpp
    src/Dialog.cpp
    src/Vehicle.cpp
)

if (WIN32)
    find_program(WSL wsl REQUIRED)
    set(LINUX_CC "x86_64-w64-mingw32-gcc")
    execute_process(COMMAND wsl ${LINUX_CC} --version OUTPUT_QUIET)
    set(TIGRESS_EXTRA_FLAGS --Environment=x86_64:Windows:Gcc:1 --Compiler=${LINUX_CC})
    set(RUNNER "${WSL}")
    execute_process(COMMAND cp "${TIGRESS_HOME}/machdeps_json/x86_64_Windows_Msvc_0.json" "${TIGRESS_HOME}/machdeps_json/x86_64_Windows_Gcc_0.json")
    execute_process(COMMAND wsl wslpath "${TIGRESS_HOME}" OUTPUT_VARIABLE TIGRESS_HOME_LINUX OUTPUT_STRIP_TRAILING_WHITESPACE)
    execute_process(COMMAND wsl wslpath "${CMAKE_SOURCE_DIR}" OUTPUT_VARIABLE SOURCE_DIR_LINUX OUTPUT_STRIP_TRAILING_WHITESPACE)
    execute_process(COMMAND wsl wslpath "${CMAKE_BINARY_DIR}" OUTPUT_VARIABLE TARGET_BIN_DIR_LINUX OUTPUT_STRIP_TRAILING_WHITESPACE)
    set(TARGET_LIB_LINUX "${TARGET_BIN_DIR_LINUX}/bin/flag.dll")
else()
    set(TIGRESS_HOME_LINUX "${TIGRESS_HOME}")
    set(SOURCE_DIR_LINUX "${CMAKE_SOURCE_DIR}")
    set(TARGET_LIB_LINUX "${CMAKE_BINARY_DIR}/bin/libflag.so")
    set(LINUX_CC "cc")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -s")
endif()

add_custom_command(
    OUTPUT "${CMAKE_SOURCE_DIR}/src/shadow_obfs.c"
    COMMAND ${CMAKE_COMMAND} -E env TIGRESS_HOME="${TIGRESS_HOME_LINUX}" WSLENV=TIGRESS_HOME
        bash "${TIGRESS_HOME_LINUX}/tigress"
            ${TIGRESS_EXTRA_FLAGS}
            --Transform=InitEntropy
            --Transform=InitOpaque
                --Functions=shadowCheck
                --InitOpaqueCount=100
                --InitOpaqueStructs=list,array,env,plugin
            --Transform=InitBranchFuns
                --Functions=shadowCheck
                --InitBranchFunsCount=30
                --InitBranchFunsObfuscate=true
            --Transform=EncodeLiterals
                --Functions=shadowCheck
            --Transform=AntiAliasAnalysis
                --Functions=shadowCheck
            --Transform=Flatten
                --Functions=shadowCheck
            --Transform=AddOpaque
                --Functions=shadowCheck
                --AddOpaqueKinds=call,bug,true,junk,question
                --AddOpaqueSplitKinds=top,block,deep,recursive,level
                --AddOpaqueCount=1
            --Transform=EncodeArithmetic
                --Functions=shadowCheck
            --Transform=CleanUp
                --CleanUpDoNotRename=shadowCheck,shadowContext,megaInit
                --CleanUpKinds=names,annotations,noMain
            --out="${SOURCE_DIR_LINUX}/src/shadow_obfs.c" "${SOURCE_DIR_LINUX}/src/shadow.c"
    DEPENDS
        "${CMAKE_SOURCE_DIR}/src/shadow.c"
)

add_custom_target(ShadowObfs
    DEPENDS "${CMAKE_SOURCE_DIR}/src/shadow_obfs.c"
    COMMAND ${CMAKE_COMMAND} -E env LINUX_CC="${LINUX_CC}" WSLENV=LINUX_CC
        "${RUNNER}" "${LINUX_CC}" -s -fPIC -shared -o ${TARGET_LIB_LINUX} "${SOURCE_DIR_LINUX}/src/shadow_obfs.c"
)

add_executable(${PROJECT_NAME} WIN32 ${SOURCES})
add_dependencies(${PROJECT_NAME} ShadowObfs)

target_include_directories(${PROJECT_NAME} PRIVATE "${CMAKE_SOURCE_DIR}/include" ${IRRLICHT_INCLUDE_DIR} ${TIGRESS_HOME})
target_link_libraries(${PROJECT_NAME}
    ${IRRLICHT_LIBRARY}
)

set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND 7z a ${CMAKE_BINARY_DIR}/bin/ASSETS.GAK "${CMAKE_SOURCE_DIR}/data" -tzip -mem=AES256 -mx9 -p"2015r0ckz!!"
)
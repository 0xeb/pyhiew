cmake_minimum_required(VERSION 3.12)

project(pyhiew)

find_package(Python REQUIRED COMPONENTS Interpreter Development)

# Define the source files for the C++ program
set(SOURCE_FILES src/pyhiew.cpp src/pyhiew.rc src/util.cpp src/util.h
                 hiewsdk/HiewGate.c hiewsdk/Hem.h)

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})

target_link_libraries(${PROJECT_NAME} ${Python_LIBRARIES})
target_include_directories(${PROJECT_NAME} PRIVATE ${Python_INCLUDE_DIRS})

target_compile_options(${PROJECT_NAME} PRIVATE
    $<$<OR:$<CONFIG:Release>,$<CONFIG:RelWithDebInfo>>:/MT>
)

target_link_options(${PROJECT_NAME} PRIVATE $<$<CONFIG:Debug>:/DYNAMICBASE:NO>)

set_target_properties(${PROJECT_NAME} PROPERTIES
        OUTPUT_NAME ${PROJECT_NAME} SUFFIX ".hem")

set(HEM_BIN ${CMAKE_SOURCE_DIR}/bin)

set_target_properties(${PROJECT_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${HEM_BIN}
        RUNTIME_OUTPUT_DIRECTORY_DEBUG ${HEM_BIN}
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${HEM_BIN}
        RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO ${HEM_BIN})

if (MSVC)
    set(HIEW_EXE ${CMAKE_SOURCE_DIR}/bin/hiew32.exe)
    get_filename_component(PYTHON_DIR ${Python_INCLUDE_DIRS} DIRECTORY)
    file(TO_NATIVE_PATH "${PYTHON_DIR}" PYTHON_DIR)
    file(TO_NATIVE_PATH "${HIEW_EXE}" HIEW_EXE)
    set(HIEW_ARGS ${HIEW_EXE})

    set_target_properties(${PROJECT_NAME} PROPERTIES VS_DEBUGGER_ENVIRONMENT "PATH=${PYTHON_DIR};%PATH%")
    set_target_properties(${PROJECT_NAME} PROPERTIES VS_DEBUGGER_COMMAND_ARGUMENTS ${HIEW_ARGS})
    set_target_properties(${PROJECT_NAME} PROPERTIES VS_DEBUGGER_COMMAND ${HIEW_ARGS})
endif()
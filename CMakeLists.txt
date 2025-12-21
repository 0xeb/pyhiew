cmake_minimum_required(VERSION 3.16)

project(pyhiew
    VERSION 0.4.0
    DESCRIPTION "Python wrapper for Hiew hex editor"
    LANGUAGES C CXX
)

# =============================================================================
# Platform Check - Hiew is Windows-only, 32-bit only
# =============================================================================
if(NOT WIN32)
    message(FATAL_ERROR "pyhiew is Windows-only (Hiew is a Windows application)")
endif()

if(MSVC)
    if(NOT CMAKE_GENERATOR_PLATFORM STREQUAL "Win32" AND NOT CMAKE_SIZEOF_VOID_P EQUAL 4)
        message(WARNING
            "Hiew is a 32-bit application. For pyhiew to work, build with:\n"
            "  cmake -A Win32 .."
        )
    endif()
endif()

# =============================================================================
# Add Hiew SDK as submodule
# =============================================================================
add_subdirectory(hiew-sdk-cpp)

# =============================================================================
# Python Configuration
# =============================================================================
# Hint paths for common 32-bit Python installations
set(PYTHON32_HINT_PATHS
    "C:/Python312-32"
    "C:/Python311-32"
    "C:/Python310-32"
    "$ENV{LOCALAPPDATA}/Programs/Python/Python312-32"
    "$ENV{LOCALAPPDATA}/Programs/Python/Python311-32"
    "$ENV{LOCALAPPDATA}/Programs/Python/Python310-32"
)

# Set hints for find_package
list(APPEND CMAKE_PREFIX_PATH ${PYTHON32_HINT_PATHS})

find_package(Python 3.10 REQUIRED COMPONENTS Interpreter Development)

# Verify 32-bit Python when building for 32-bit
if(CMAKE_SIZEOF_VOID_P EQUAL 4)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -c "import struct; print(struct.calcsize('P') * 8)"
        OUTPUT_VARIABLE PYTHON_BITS
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
    )
    if(NOT PYTHON_BITS EQUAL 32)
        message(FATAL_ERROR
            "Architecture mismatch: Building 32-bit but Python is ${PYTHON_BITS}-bit.\n"
            "pyhiew requires 32-bit Python. Please:\n"
            "  1. Install Python 3.10+ 32-bit from python.org\n"
            "  2. Set Python_ROOT_DIR to point to 32-bit installation:\n"
            "     cmake -A Win32 -DPython_ROOT_DIR=C:/Python312-32 ..\n"
            "\n"
            "Current Python: ${Python_EXECUTABLE}"
        )
    endif()
endif()

message(STATUS "Found Python ${Python_VERSION} at ${Python_EXECUTABLE}")
message(STATUS "Python include: ${Python_INCLUDE_DIRS}")
message(STATUS "Python library dirs: ${Python_LIBRARY_DIRS}")

# =============================================================================
# pyhiew HEM module
# =============================================================================
set(SOURCE_FILES
    src/pyhiew.cpp
    src/pyhiew.rc
    src/util.cpp
    src/util.h
)

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})

# Link to Hiew C SDK from submodule
target_link_libraries(${PROJECT_NAME} PRIVATE hiew::sdk)

# Python includes
target_include_directories(${PROJECT_NAME} PRIVATE ${Python_INCLUDE_DIRS})

# Find and link python3.lib (stable ABI)
find_library(PYTHON3_STABLE_LIB
    NAMES python3
    PATHS "${Python_LIBRARY_DIRS}"
    NO_DEFAULT_PATH
)

if(NOT PYTHON3_STABLE_LIB)
    # Fallback: look in Python root
    get_filename_component(PYTHON_ROOT "${Python_EXECUTABLE}" DIRECTORY)
    find_library(PYTHON3_STABLE_LIB
        NAMES python3
        PATHS "${PYTHON_ROOT}/libs"
        NO_DEFAULT_PATH
    )
endif()

if(PYTHON3_STABLE_LIB)
    message(STATUS "Using Python Stable ABI: ${PYTHON3_STABLE_LIB}")
    target_link_libraries(${PROJECT_NAME} PRIVATE ${PYTHON3_STABLE_LIB})
    # Define stable ABI version (Python 3.10+)
    target_compile_definitions(${PROJECT_NAME} PRIVATE Py_LIMITED_API=0x030A0000)
else()
    message(WARNING "python3.lib not found, falling back to version-specific library")
    target_link_libraries(${PROJECT_NAME} PRIVATE ${Python_LIBRARIES})
endif()

# =============================================================================
# Compiler Settings
# =============================================================================
if(MSVC)
    # Static runtime for release builds
    target_compile_options(${PROJECT_NAME} PRIVATE
        $<$<OR:$<CONFIG:Release>,$<CONFIG:RelWithDebInfo>>:/MT>
    )
    # Debug: disable ASLR for easier debugging
    target_link_options(${PROJECT_NAME} PRIVATE
        $<$<CONFIG:Debug>:/DYNAMICBASE:NO>
    )
    # Note: hem.h handles struct packing via #pragma pack internally
endif()

# =============================================================================
# Output Configuration
# =============================================================================
set_target_properties(${PROJECT_NAME} PROPERTIES
    OUTPUT_NAME ${PROJECT_NAME}
    SUFFIX ".hem"
    PREFIX ""
)

set(HEM_BIN ${CMAKE_SOURCE_DIR}/bin)

set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${HEM_BIN}
    RUNTIME_OUTPUT_DIRECTORY_DEBUG ${HEM_BIN}
    RUNTIME_OUTPUT_DIRECTORY_RELEASE ${HEM_BIN}
    RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO ${HEM_BIN}
)

# =============================================================================
# Visual Studio Debugger Settings
# =============================================================================
if(MSVC)
    set(HIEW_EXE ${CMAKE_SOURCE_DIR}/bin/hiew32.exe)
    get_filename_component(PYTHON_DIR ${Python_INCLUDE_DIRS} DIRECTORY)
    file(TO_NATIVE_PATH "${PYTHON_DIR}" PYTHON_DIR)
    file(TO_NATIVE_PATH "${HIEW_EXE}" HIEW_EXE)

    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=${PYTHON_DIR};%PATH%"
        VS_DEBUGGER_COMMAND_ARGUMENTS ${HIEW_EXE}
        VS_DEBUGGER_COMMAND ${HIEW_EXE}
    )
endif()

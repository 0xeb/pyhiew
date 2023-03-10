#include <Python.h>
#include <Windows.h>

//--------------------------------------------------------------------------
bool PyAddSysPath(char* path)
{
    char tmp[MAX_PATH * 2];
    _snprintf(tmp, sizeof(tmp),
        "import sys\n"
        "sys.path.append(r\"%s\")", path);
    return PyRun_SimpleString(tmp) == 0;
}

//--------------------------------------------------------------------------
bool PyRunFile(char* filename)
{
    char tmp[MAX_PATH * 2];
    _snprintf(tmp, sizeof(tmp),
        R"(exec(compile(open(r"%s", "rb").read(), r"%s", 'exec'), globals()))",
        filename, filename);
    return PyRun_SimpleString(tmp) == 0;
}

//--------------------------------------------------------------------------
bool GetModulePath(char* modname, char* path, size_t sz)
{
    // Get HEM path
    HMODULE hMod = GetModuleHandle(modname);
    if (hMod == NULL)
        return false;

    GetModuleFileName(hMod, path, DWORD(sz));
    char* p = strrchr(path, '\\');
    if (p == NULL)
        return false;
    *p = '\0';
    return true;
}

//--------------------------------------------------------------------------
bool DirExists(char* path)
{
    DWORD attr = GetFileAttributes(path);
    return (attr != INVALID_FILE_ATTRIBUTES) && ((attr & FILE_ATTRIBUTE_DIRECTORY) != 0);
}
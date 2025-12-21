// Python Stable ABI - must be defined BEFORE Python.h
#define Py_LIMITED_API 0x030A0000
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <Windows.h>

//--------------------------------------------------------------------------
// PyRun_SimpleString is not in the stable ABI, so we implement it using exec()
static int PyRunSimpleString_StableABI(const char* code)
{
    // Get __main__ module and its globals
    PyObject* main_module = PyImport_ImportModule("__main__");
    if (!main_module)
        return -1;

    PyObject* globals = PyModule_GetDict(main_module);
    Py_DECREF(main_module);
    if (!globals)
        return -1;

    // Get exec() builtin
    PyObject* builtins = PyEval_GetBuiltins();
    if (!builtins)
        return -1;

    PyObject* exec_func = PyDict_GetItemString(builtins, "exec");
    if (!exec_func)
        return -1;

    // Create code string
    PyObject* code_obj = PyUnicode_FromString(code);
    if (!code_obj)
        return -1;

    // Call exec(code, globals)
    PyObject* result = PyObject_CallFunctionObjArgs(exec_func, code_obj, globals, NULL);
    Py_DECREF(code_obj);

    if (!result)
    {
        PyErr_Print();
        return -1;
    }

    Py_DECREF(result);
    return 0;
}

//--------------------------------------------------------------------------
bool PyAddSysPath(char* path)
{
    char tmp[MAX_PATH * 2];
    _snprintf(tmp, sizeof(tmp),
        "import sys\n"
        "sys.path.append(r\"%s\")", path);
    return PyRunSimpleString_StableABI(tmp) == 0;
}

//--------------------------------------------------------------------------
bool PyRunFile(char* filename)
{
    char tmp[MAX_PATH * 2];
    _snprintf(tmp, sizeof(tmp),
        R"(exec(compile(open(r"%s", "rb").read(), r"%s", 'exec'), globals()))",
        filename, filename);
    return PyRunSimpleString_StableABI(tmp) == 0;
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

#ifndef __UTIL__
#define __UTIL__

bool PyAddSysPath(char *path);
bool PyRunFile(char *filename);
bool GetModulePath(char *modname, char *path, size_t sz);
bool DirExists(char *path);

#endif
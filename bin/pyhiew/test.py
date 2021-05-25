# --------------------------------------------------------------------------
# PyHiew - test script
# (c) Elias Bachaalany
import hiew
import _hiew



def testMain():
    hiew.Message("testMain()")


print(dir(_hiew))
print(_hiew.__name__)
hiew.Message("Info", "Hello world!")
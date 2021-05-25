import hiew
from hiew import Names
from hiew import Data

def testMain():
    msg = []

    offs = Data.GetCurrentOffset()

    Names.AddGlobal(offs, "Hello %s" % offs)

    msg.append("Local:%d Global:%d" % (Names.CountLocal(), Names.CountGlobal()))

    Names.AddGlobalComment(offs, "This is a comment")
    Names.AddLocalComment(offs + 1, "Local comment")
    Names.AddGlobalComment(offs + 2, "Global comment")

    offs = offs + 100
    Names.AddGlobal(offs, "GlobalName")
    Names.AddLocal(offs + 1, "LocalName")


    # find any name
    x = Names.FindName("LocalName")
    msg.append("FindName->%s" % str(x))

    # find local
    x = Names.FindLocalName("LocalName")
    msg.append("Found local name at %s" % x)

    # find global
    x = Names.FindGlobalName("GlobalName")
    msg.append("Found global name at %s" % x)

    # search unexisting global
    x = Names.FindGlobalName("xGlobalName")
    msg.append("Found xglobal name at %s" % x)

    # search unexisting local
    x = Names.FindGlobalName("xLocalName")
    msg.append("Found xlocal name at %s" % x)

    # search local as global
    x = Names.FindGlobalName("LocalName")
    msg.append("Found local as global at %s" % x)

    # search global as local
    x = Names.FindLocalName("GlobalName")
    msg.append("Found global as local at %s" % x)

    hiew.Window.FromString("Info", msg)

    hiew.ReturnOffset(offs)
    hiew.ReturnMode(hiew.HEM_RETURN_MODE_HEX)


testMain()
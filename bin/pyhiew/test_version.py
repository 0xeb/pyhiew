import hiew

hiew.Window.FromString(" Information ", '\n'.join(
    [
       "Hiew version: %d.%d" % (hiew.VERSION['major'], hiew.VERSION['minor']),
       "Hiew SDK version: %d.%d" % (hiew.VERSION['sdkmajor'], hiew.VERSION['sdkminor']),
       "PyHiew version: %d.%d" % (hiew.PYHIEW_VERSION['major'], hiew.PYHIEW_VERSION['minor']),
    ]) )
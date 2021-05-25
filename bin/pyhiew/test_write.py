import hiew

rc = hiew.FileOpenForWrite()
hiew.Message("openforwrite", "rc=%d" % rc)

# Overwrite at offset 0

rc = hiew.FileWrite(0, b"Hello world")
hiew.Message("write", "rc=%d" % rc)

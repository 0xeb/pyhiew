import hiew

dbg = hiew.dbg

# -----------------------------------------------------------------------
def test1():
    w = hiew.Window()
    r = w.Create(
        title = "Window title",
        lines = ["Line %d" % i for i in range(0, 10)],
        width = 80,
        main_keys = {1: "Help"},
        alt_keys = {5: "Reload", 1: "AHelp"})

    w.Show()

# -----------------------------------------------------------------------
def test2():
    hiew.Window.FromString("Info", "Hello\nworld\n")

# -----------------------------------------------------------------------
test1()
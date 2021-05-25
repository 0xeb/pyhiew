import hiew

dbg = hiew.dbg
m = hiew.Menu()
r = m.Create(
    title = "Menu title",
    lines = ["Line %d" % i for i in range(0, 10)],
    width = 30,
    main_keys = {1: "-Help", 4: "-Disabled"},
    alt_keys = {4: "Reload", 1: "AHelp"})

n = 0
while True:
    n, k = m.Show(n)
    hiew.Message("Selection", "n=%s k=%s" % (n, k))
    if n == -1:
        break

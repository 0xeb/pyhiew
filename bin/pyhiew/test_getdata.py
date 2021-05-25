import hiew

dbg = hiew.dbg

d = hiew.GetData()

hiew.Window.FromString("Title",
  (f"filename={d.filename}\n"
   f"offsetMark1={d.offsetMark1:x}\n"
   f"offsetMark2={d.offsetMark2:x}\n"
   f"offsetCurrent={d.offsetCurrent:x}\n"))


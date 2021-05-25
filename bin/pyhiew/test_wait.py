import hiew
import time

dbg = hiew.dbg

hiew.MessageWaitOpen("Waiting....")
time.sleep(1)
hiew.MessageWaitClose()

hiew.MessageWaitOpen()
while not hiew.IsKeyBreak():
    time.sleep(1)

if hiew.AskYesNo("Are you sure?"):
	hiew.Message("Info", "Gotcha!")

hiew.MessageWaitClose()

import hiew

def testMain():
    global FIRST_RUN
    try:
        FIRST_RUN
    except:
        FIRST_RUN = 1
        hiew.Message("Startup script", "First time executed!")

    hiew.Message("Startup script", "Hello! I am invoked because of SetStartupScript()")

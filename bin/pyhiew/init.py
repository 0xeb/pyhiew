import hiew

DOCGEN, DEVMODE, RELEASE = range(3)

mode = RELEASE

# Set startup script information

if mode == DOCGEN:
    hiew.SetStartupScript('_gendocs.py', globals(), 'docgen')
elif mode == DEVMODE:
    hiew.SetStartupScript('_test_startup.py', globals(), 'testMain')
else:  # RELEASE or any other mode
    # Use the default script browser
    hiew.SetStartupScript('scriptbrowser.py', globals(), 'ScriptBrowserMain')

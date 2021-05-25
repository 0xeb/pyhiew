import hiew

DEVMODE = False

# Set startup script information

if DEVMODE:
	hiew.SetStartupScript('test_startup.py', globals(), 'testMain')
else:
	# Use the default script browser
	hiew.SetStartupScript('scriptbrowser.py', globals(), 'ScriptBrowserMain')
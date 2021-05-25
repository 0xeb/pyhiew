"""
Sample Hiew based Python statement prompt
"""
import hiew
import traceback

while True:
	s = hiew.GetString("Enter python statement", 100)
	if not s:
		break
		
	try:
	    r = exec(s, globals())
	    
	except Exception as e:
	    hiew.Window.FromString(
	        'statement error',
	        str(e) + "\n" + traceback.format_exc())
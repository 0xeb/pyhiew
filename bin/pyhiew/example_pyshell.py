"""Example: Interactive Python shell in Hiew."""
import hiew
import traceback

hiew.Message("PyShell", "Enter Python statements. Press ESC to exit.")

while True:
    stmt = hiew.GetString(">>> ", 100)
    if not stmt:
        break

    try:
        # Try to evaluate as expression first
        try:
            result = eval(stmt, globals())
            if result is not None:
                hiew.Message("Result", str(result))
        except SyntaxError:
            # If not an expression, execute as statement
            exec(stmt, globals())
    except Exception as e:
        hiew.Window.FromString(
            "Error",
            f"{e}\n{traceback.format_exc()}",
            width=70
        )

"""Test startup script for development."""
import hiew

_first_run = True


def testMain() -> None:
    global _first_run

    if _first_run:
        _first_run = False
        hiew.Message("Startup", "First time executed!")

    hiew.Message("Startup", "Hello from SetStartupScript()!")

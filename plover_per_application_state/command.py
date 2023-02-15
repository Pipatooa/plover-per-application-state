from plover.engine import StenoEngine
from plover_application_controls import WindowTracker

from plover_per_application_state import PerApplicationStateExtension


def command(engine: StenoEngine, arg: str) -> None:
    subcommand, *args = arg.split(":")
    if not subcommand:
        raise KeyError("No subcommand specified")
    _COMMAND_MAP[subcommand](engine, *args)


def clear(engine: StenoEngine) -> None:
    engine.clear_translator_state()


def clear_all(engine: StenoEngine) -> None:
    PerApplicationStateExtension.get_state_manager().clear()
    engine.clear_translator_state()


def clear_window(engine: StenoEngine) -> None:
    handle_hash = WindowTracker.current_window_details.handle_hash
    PerApplicationStateExtension.get_state_manager().clear_window(handle_hash)
    engine.clear_translator_state()


_COMMAND_MAP = {
    "clear": clear,
    "clear_all": clear_all,
    "clear_window": clear_window
}

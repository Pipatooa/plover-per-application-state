from plover.engine import StenoEngine

from plover_per_application_state.state import StateManager


def command(engine: StenoEngine, arg: str) -> None:
    subcommand, *args = arg.split(":")
    if not subcommand:
        raise KeyError("No subcommand specified")
    _COMMAND_MAP[subcommand](engine, *args)


def clear(engine: StenoEngine) -> None:
    engine.clear_translator_state()


def clear_all(engine: StenoEngine) -> None:
    StateManager.clear()
    engine.clear_translator_state()


def clear_window(engine: StenoEngine) -> None:
    StateManager.clear_window_state()
    engine.clear_translator_state()


_COMMAND_MAP = {
    "clear": clear,
    "clear_all": clear_all,
    "clear_window": clear_window
}

from typing import Tuple

from plover.engine import StenoEngine
from plover_application_controls import WindowTracker

from plover_per_application_state.state.manager import StateManager


class PerApplicationStateExtension:
    def __init__(self, engine: StenoEngine) -> None:
        self._on = False
        self._engine = engine
        WindowTracker.add_callback(True, self.on_window_callback)

    def start(self) -> None:
        self._on = True

    def stop(self) -> None:
        self._on = False
        StateManager.switch_states(self._engine, hash(None), "")

    def on_window_callback(self, _, handle_hash: int, details: Tuple[str, str, str]) -> None:
        if not self._on:
            return

        _, _, title = details
        StateManager.switch_states(self._engine, handle_hash, title)

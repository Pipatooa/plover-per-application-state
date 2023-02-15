from __future__ import annotations

from typing import Tuple

from plover.engine import StenoEngine
from plover_application_controls import WindowTracker

from plover_per_application_state.state.manager import StateManager
import plover_per_application_state.transition_handler as handlers


class PerApplicationStateExtension:
    _instance: 'PerApplicationStateExtension' = None

    def __init__(self, engine: StenoEngine) -> None:
        PerApplicationStateExtension._instance = self
        self._on = False
        self._engine = engine

        self._state_manager = StateManager([
            handlers.DefaultWindowTransitionHandler(engine)
        ])
        self._last_details = (hash(None), ("", "", ""))

        WindowTracker.add_callback(True, self.on_window_callback)

    def start(self) -> None:
        self._on = True

    def stop(self) -> None:
        self._on = False

    def on_window_callback(self, _, handle_hash: int, details: Tuple[str, str, str]) -> None:
        new_details = (handle_hash, details)
        if not self._on:
            self._last_details = new_details
            return

        self._state_manager.on_transition(self._engine, self._last_details, new_details)
        self._last_details = new_details

    @staticmethod
    def get_state_manager() -> StateManager | None:
        if PerApplicationStateExtension._instance is None:
            return None
        return PerApplicationStateExtension._instance._state_manager

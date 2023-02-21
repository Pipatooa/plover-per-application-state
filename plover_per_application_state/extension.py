from __future__ import annotations

from plover.engine import StenoEngine
from plover_application_controls.window import WindowTracker, WindowDetails

from plover_per_application_state.state.manager import StateManager
import plover_per_application_state.transition.handler as handlers
from plover_per_application_state.transition import TransitionDetails


class PerApplicationStateExtension:
    _instance: 'PerApplicationStateExtension' = None

    def __init__(self, engine: StenoEngine) -> None:
        PerApplicationStateExtension._instance = self
        self._on = False
        self._engine = engine

        self._state_manager = StateManager([
            handlers.DynamicTitleTransitionHandler(engine),
            handlers.DefaultTransitionHandler(engine)
        ])
        self._last_details = WindowTracker.BLANK_DETAILS

        WindowTracker.add_callback(True, self.on_window_callback)

    def start(self) -> None:
        self._on = True

    def stop(self) -> None:
        self._on = False

    def on_window_callback(self, _, details: WindowDetails) -> None:
        if not self._on:
            self._last_details = details
            return

        self._state_manager.on_transition(self._engine, TransitionDetails(self._last_details, details))
        self._last_details = details

    @staticmethod
    def get_state_manager() -> StateManager | None:
        if PerApplicationStateExtension._instance is None:
            return None
        return PerApplicationStateExtension._instance._state_manager

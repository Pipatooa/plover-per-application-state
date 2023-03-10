from __future__ import annotations

import time

from plover.engine import StenoEngine
from plover.formatting import _Action
from plover_application_controls.window import WindowTracker

import plover_per_application_state.state.manager as _state_manager
from plover_per_application_state.transition.details import TransitionDetails
from plover_per_application_state.transition.handler.handler import TransitionHandler


class DynamicTitleTransitionHandler(TransitionHandler):

    TITLE_CHANGE_TIMEOUT = WindowTracker.CHECK_INTERVAL * 2
    MERGE_PREVENTION_TIMEOUT = TITLE_CHANGE_TIMEOUT

    _last_merge_prevention = 0

    def __init__(self, engine: StenoEngine, priority=100):
        super().__init__(engine, priority)
        self._changes = False
        self._change_timestamp = 0
        engine.hook_connect("translated", self.on_translated)

    def handle_transition(self, state_manager: _state_manager.StateManager,
                          engine: StenoEngine,
                          details: TransitionDetails) -> bool:
        changes = self._changes
        self._changes = False

        if not changes or details.window_changed:
            return False

        current_time = time.time()

        if current_time - DynamicTitleTransitionHandler._last_merge_prevention \
                < DynamicTitleTransitionHandler.MERGE_PREVENTION_TIMEOUT:
            return False

        if current_time - self._change_timestamp \
                > DynamicTitleTransitionHandler.TITLE_CHANGE_TIMEOUT:
            return False

        stored_state = state_manager.get_state(details.new_details.handle_hash, details.new_details.title, False)
        return not stored_state or stored_state == engine.translator_state

    def on_translated(self, old: [_Action], new: [_Action]) -> None:
        for action in new:
            if action.command and action.command.startswith("application:"):
                return

        self._changes = True
        self._change_timestamp = time.time()

    @staticmethod
    def prevent_merge():
        DynamicTitleTransitionHandler._last_merge_prevention = time.time()

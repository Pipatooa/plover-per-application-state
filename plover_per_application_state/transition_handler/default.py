from __future__ import annotations

from typing import Tuple

from plover.engine import StenoEngine

import plover_per_application_state.state.manager as _state_manager
from plover_per_application_state.transition_handler.handler import WindowTransitionHandler


class DefaultWindowTransitionHandler(WindowTransitionHandler):
    def handle_transition(self, state_manager: _state_manager.StateManager, engine: StenoEngine,
                          old_details: Tuple[int, Tuple[str, str, str]],
                          new_details: Tuple[int, Tuple[str, str, str]]) -> bool:

        old_handle_hash, (old_app, old_class, old_title) = old_details
        new_handle_hash, (new_app, new_class, new_title) = new_details

        stored_state = state_manager.get_state(new_handle_hash, new_title)
        state_manager.store_state(old_handle_hash, old_title, engine.translator_state)
        engine.translator_state = stored_state

        return True

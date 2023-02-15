from __future__ import annotations

from plover.engine import StenoEngine

import plover_per_application_state.state.manager as _state_manager
from plover_per_application_state.transition.details import TransitionDetails
from plover_per_application_state.transition.handler.handler import TransitionHandler


class DefaultTransitionHandler(TransitionHandler):
    def handle_transition(self, state_manager: _state_manager.StateManager,
                          engine: StenoEngine,
                          details: TransitionDetails) -> bool:

        stored_state = state_manager.get_state(details.new_details.handle_hash, details.new_details.title)
        state_manager.store_state(details.old_details.handle_hash, details.old_details.title, engine.translator_state)
        engine.translator_state = stored_state
        return True

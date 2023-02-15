from __future__ import annotations

import abc
from functools import total_ordering
from typing import Tuple, final

from plover.engine import StenoEngine

import plover_per_application_state.state.manager as _state_manager


@total_ordering
class WindowTransitionHandler(abc.ABC):
    def __init__(self, engine: StenoEngine, priority=0):
        self._engine = engine
        self._priority = priority

    @abc.abstractmethod
    def handle_transition(self, state_manager: _state_manager.StateManager, engine: StenoEngine,
                          old_details: Tuple[int, Tuple[str, str, str]],
                          new_details: Tuple[int, Tuple[str, str, str]]) -> bool:
        return False

    @final
    def __eq__(self, other: 'WindowTransitionHandler') -> bool:
        return self._priority == other._priority

    @final
    def __gt__(self, other: 'WindowTransitionHandler') -> bool:
        return self._priority > other._priority

from __future__ import annotations

import abc
from functools import total_ordering
from typing import final

from plover.engine import StenoEngine

import plover_per_application_state.state.manager as _state_manager
from plover_per_application_state.transition.details import TransitionDetails


@total_ordering
class TransitionHandler(abc.ABC):
    def __init__(self, engine: StenoEngine, priority=0):
        self._engine = engine
        self._priority = priority

    @abc.abstractmethod
    def handle_transition(self, state_manager: _state_manager.StateManager,
                          engine: StenoEngine,
                          details: TransitionDetails) -> bool:
        raise NotImplementedError()

    @final
    def __eq__(self, other: 'TransitionHandler') -> bool:
        return self._priority == other._priority

    @final
    def __gt__(self, other: 'TransitionHandler') -> bool:
        return self._priority > other._priority

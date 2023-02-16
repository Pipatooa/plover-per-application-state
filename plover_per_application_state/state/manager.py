from __future__ import annotations

from plover.engine import StenoEngine
from plover.translation import _State

from plover_per_application_state.state.window_state_collection import WindowStateCollection
import plover_per_application_state.transition.handler.handler as transition_handler
from plover_per_application_state.transition import TransitionDetails


class StateManager:
    WINDOW_LIMIT = (50, 10)

    def __init__(self, handlers: [transition_handler.TransitionHandler]):
        self._window_state_collections = {}
        self._window_state_collection_count = 0
        self._next_timestamp = -1

        self._transition_handlers = handlers
        self._transition_handlers.sort(reverse=True)

    def add_transition_handlers(self, handlers: [transition_handler.TransitionHandler]) -> None:
        self._transition_handlers.extend(handlers)
        self._transition_handlers.sort(reverse=True)

    def remove_transition_handlers(self, handlers: [transition_handler.TransitionHandler]) -> None:
        for handler in handlers:
            self._transition_handlers.remove(handler)

    def on_transition(self, engine: StenoEngine, details: TransitionDetails) -> None:
        for handler in self._transition_handlers:
            if handler.handle_transition(self, engine, details):
                break

    def store_state(self, handle_hash: int, title: str, state: _State) -> None:
        self._get_window_state_collection(handle_hash)[title] = state
        self._check_eviction()

    def get_state(self, handle_hash: int, title: str, default=True) -> _State | None:
        state_collection = self._get_window_state_collection(handle_hash)
        if not default and title not in state_collection:
            return None
        return state_collection[title]

    def _timestamp(self) -> int:
        self._next_timestamp += 1
        return self._next_timestamp

    def _get_window_state_collection(self, handle_hash: int) -> WindowStateCollection:
        timestamp = self._timestamp()
        try:
            state_collection = self._window_state_collections[handle_hash][0]
        except KeyError:
            state_collection = WindowStateCollection(handle_hash)
            self._window_state_collection_count += 1
        self._window_state_collections[handle_hash] = (state_collection, timestamp)
        return state_collection

    def _check_eviction(self) -> None:
        if self._window_state_collection_count > sum(StateManager.WINDOW_LIMIT):
            self._evict(StateManager.WINDOW_LIMIT[1])

    def _evict(self, n: int) -> None:
        candidates = sorted(self._window_state_collections.items(), key=lambda x: x[1][1])
        for (handle_hash, (window_state_collection, _)), _ in zip(candidates, range(n)):
            window_state_collection.clear()
            del self._window_state_collections[handle_hash]
        self._window_state_collection_count -= n

    def clear(self) -> None:
        for window_state_collection, _ in self._window_state_collections.values():
            window_state_collection.clear()
        self._window_state_collections.clear()
        self._window_state_collection_count = 0

    def clear_window(self, handle_hash: int) -> None:
        self._get_window_state_collection(handle_hash).clear()

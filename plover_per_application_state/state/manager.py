from __future__ import annotations

from plover.engine import StenoEngine

from plover_per_application_state.state.window_state_collection import WindowStateCollection


class StateManager:
    WINDOW_LIMIT = (50, 10)

    _current_handle_hash = hash(None)
    _current_title = ""
    _window_state_collections = {}
    _window_state_collection_count = 0

    _next_timestamp = -1

    @staticmethod
    def _timestamp() -> int:
        StateManager._next_timestamp += 1
        return StateManager._next_timestamp

    @staticmethod
    def switch_states(engine: StenoEngine, handle_hash: int, title: str) -> None:
        retrieved_state = StateManager._get_window_state_collection(handle_hash)[title]
        current_state_collection = StateManager._get_window_state_collection(StateManager._current_handle_hash)
        current_state_collection[StateManager._current_title] = engine.translator_state
        StateManager._current_handle_hash = handle_hash
        StateManager._current_title = title
        engine.translator_state = retrieved_state
        StateManager._check_eviction()

    @staticmethod
    def _get_window_state_collection(handle_hash: int) -> WindowStateCollection:
        timestamp = StateManager._timestamp()
        try:
            state_collection = StateManager._window_state_collections[handle_hash][0]
        except KeyError:
            state_collection = WindowStateCollection(handle_hash)
            StateManager._window_state_collection_count += 1
        StateManager._window_state_collections[handle_hash] = (state_collection, timestamp)
        return state_collection

    @staticmethod
    def _check_eviction() -> None:
        if StateManager._window_state_collection_count > sum(StateManager.WINDOW_LIMIT):
            StateManager._evict(StateManager.WINDOW_LIMIT[1])

    @staticmethod
    def _evict(n: int) -> None:
        candidates = sorted(StateManager._window_state_collections.items(), key=lambda x: x[1][1])
        for (handle_hash, _), _ in zip(candidates, range(n)):
            StateManager._window_state_collections[handle_hash][0].clear()
            del StateManager._window_state_collections[handle_hash]
        StateManager._window_state_collection_count -= n

from plover.translation import _State


class WindowStateCollection:
    GLOBAL_LIMIT = (75, 15)
    WINDOW_LIMIT = (25, 5)

    _all_states = {}
    _all_states_count = 0

    _next_timestamp = -1

    def __init__(self, handle_hash: int):
        self._handle_hash = handle_hash
        self._states = {}
        self._state_count = 0

    @staticmethod
    def _timestamp() -> int:
        WindowStateCollection._next_timestamp += 1
        return WindowStateCollection._next_timestamp

    def __getitem__(self, title: str) -> _State:
        try:
            state = self._states[title][0]
            timestamp = WindowStateCollection._timestamp()
            self._states[title] = (state, timestamp)
            global_key = (self._handle_hash, title)
            WindowStateCollection._all_states[global_key] = (self, timestamp)
        except KeyError:
            return _State()

    def __setitem__(self, title: str, state: _State) -> None:
        timestamp = WindowStateCollection._timestamp()
        new_entry = title not in self._states
        self._states[title] = (state, timestamp)
        global_key = (self._handle_hash, title)
        WindowStateCollection._all_states[global_key] = (self, timestamp)
        if new_entry:
            self._state_count += 1
            WindowStateCollection._all_states_count += 1
        self._check_eviction()
        WindowStateCollection._check_global_eviction()

    def __delitem__(self, title: str) -> None:
        del self._states[title]
        self._state_count -= 1
        global_key = (self._handle_hash, title)
        del WindowStateCollection._all_states[global_key]
        WindowStateCollection._all_states_count -= 1

    def clear(self) -> None:
        for title in self._states:
            global_key = (self._handle_hash, title)
            del WindowStateCollection._all_states[global_key]
        WindowStateCollection._all_states_count -= self._state_count
        self._states = {}
        self._state_count = 0

    def _check_eviction(self) -> None:
        if self._state_count > sum(WindowStateCollection.WINDOW_LIMIT):
            self._evict(WindowStateCollection.WINDOW_LIMIT[1])

    def _evict(self, n: int) -> None:
        candidates = sorted(self._states.items(), key=lambda x: x[1][1])
        for (title, _), _ in zip(candidates, range(n)):
            del self._states[title]
            global_key = (self._handle_hash, title)
            del WindowStateCollection._all_states[global_key]

        self._state_count -= n
        WindowStateCollection._all_states_count -= n

    @staticmethod
    def _check_global_eviction() -> None:
        if WindowStateCollection._all_states_count > sum(WindowStateCollection.GLOBAL_LIMIT):
            WindowStateCollection._global_evict(WindowStateCollection.GLOBAL_LIMIT[1])

    @staticmethod
    def _global_evict(n: int) -> None:
        candidates = sorted(WindowStateCollection._all_states.items(), key=lambda x: x[1][1])
        for ((_, title), (cls, _)), _ in zip(candidates, range(n)):
            del cls[title]

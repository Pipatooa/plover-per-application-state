from dataclasses import dataclass

from plover_application_controls.window import WindowDetails


@dataclass
class TransitionDetails:
    old_details: WindowDetails
    new_details: WindowDetails

    @property
    def window_changed(self) -> bool:
        return self.old_details.handle_hash != self.new_details.handle_hash

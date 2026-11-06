"""Event-handling logic. Knows nothing about Tkinter, so it can be tested without a window."""

from typing import Protocol

from tattoo_heal_timer.healing import DailyCare, HealingGuide, HealingPhase, parse_day

MAX_DAY = 999


class HealingView(Protocol):
    """What the controller needs from the GUI."""

    def show_care(self, care: DailyCare) -> None: ...

    def show_input_error(self, message: str) -> None: ...

    def set_day_text(self, text: str) -> None: ...


class HealingController:
    def __init__(self, guide: HealingGuide, view: HealingView) -> None:
        self.guide = guide
        self.view = view
        self.day = 0

    def start(self) -> None:
        self._select_day(0)

    def on_day_typed(self, raw: str) -> None:
        """Runs on every keystroke, so a half-typed value must not overwrite the field."""
        day = parse_day(raw)
        if day is None:
            self.view.show_input_error("Kérlek, nemnegatív egész számot adj meg!")
        elif day > MAX_DAY:
            self.view.show_input_error(f"Legfeljebb {MAX_DAY} napot adhatsz meg.")
        else:
            self.day = day
            self.view.show_care(self.guide.care_for(day))

    def on_step(self, delta: int) -> None:
        self._select_day(self.day + delta)

    def on_phase_selected(self, phase: HealingPhase) -> None:
        self._select_day(phase.first_day)

    def _select_day(self, day: int) -> None:
        self.day = max(0, min(day, MAX_DAY))
        self.view.set_day_text(str(self.day))
        self.view.show_care(self.guide.care_for(self.day))

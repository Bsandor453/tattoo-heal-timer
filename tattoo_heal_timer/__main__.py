"""Entry point: ``python -m tattoo_heal_timer``."""

from tattoo_heal_timer.controller import HealingController
from tattoo_heal_timer.healing import HealingGuide
from tattoo_heal_timer.ui import HealingWindow


def main() -> None:
    window = HealingWindow()
    controller = HealingController(HealingGuide(), window)
    window.bind_events(controller)
    controller.start()
    window.run()


if __name__ == "__main__":
    main()

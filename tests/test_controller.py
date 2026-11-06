import unittest

from tattoo_heal_timer.controller import MAX_DAY, HealingController
from tattoo_heal_timer.healing import PHASES, HealingGuide


class FakeView:
    def __init__(self):
        self.care = None
        self.error = None
        self.day_text = None

    def show_care(self, care):
        self.care = care
        self.error = None

    def show_input_error(self, message):
        self.error = message

    def set_day_text(self, text):
        self.day_text = text


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.view = FakeView()
        self.controller = HealingController(HealingGuide(), self.view)
        self.controller.start()

    def test_starts_on_day_zero(self):
        self.assertEqual(self.view.care.day, 0)
        self.assertEqual(self.view.day_text, "0")

    def test_typing_a_valid_day_updates_care_immediately(self):
        self.controller.on_day_typed("7")
        self.assertEqual(self.view.care.day, 7)
        self.assertIsNone(self.view.error)

    def test_invalid_typing_shows_error_and_keeps_day(self):
        self.controller.on_day_typed("7")
        self.controller.on_day_typed("7x")
        self.assertIsNotNone(self.view.error)
        self.assertEqual(self.controller.day, 7)
        self.assertEqual(self.view.care.day, 7)

    def test_typing_above_the_limit_is_rejected(self):
        self.controller.on_day_typed(str(MAX_DAY + 1))
        self.assertIsNotNone(self.view.error)
        self.assertEqual(self.controller.day, 0)

    def test_step_buttons_change_day_and_field(self):
        self.controller.on_step(1)
        self.controller.on_step(1)
        self.controller.on_step(-1)
        self.assertEqual(self.controller.day, 1)
        self.assertEqual(self.view.day_text, "1")

    def test_step_stops_at_limits(self):
        self.controller.on_step(-1)
        self.assertEqual(self.controller.day, 0)
        self.controller.on_day_typed(str(MAX_DAY))
        self.controller.on_step(1)
        self.assertEqual(self.controller.day, MAX_DAY)

    def test_step_after_invalid_typing_recovers_the_field(self):
        self.controller.on_day_typed("5")
        self.controller.on_day_typed("")
        self.controller.on_step(1)
        self.assertEqual(self.view.day_text, "6")
        self.assertIsNone(self.view.error)

    def test_phase_button_jumps_to_first_day_of_phase(self):
        self.controller.on_phase_selected(PHASES[2])
        self.assertEqual(self.controller.day, PHASES[2].first_day)
        self.assertEqual(self.view.day_text, str(PHASES[2].first_day))


if __name__ == "__main__":
    unittest.main()

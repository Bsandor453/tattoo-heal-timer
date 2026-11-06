import unittest

from tattoo_heal_timer.healing import PHASES, HealingGuide, parse_day


class PhaseTests(unittest.TestCase):
    def test_phase_boundaries(self):
        guide = HealingGuide()
        expected = {
            0: "Friss seb",
            3: "Friss seb",
            4: "Hámlás és viszketés",
            14: "Hámlás és viszketés",
            15: "Regenerálódás",
            30: "Regenerálódás",
            31: "Hosszú távú ápolás",
            5000: "Hosszú távú ápolás",
        }
        for day, name in expected.items():
            with self.subTest(day=day):
                self.assertEqual(guide.phase_for(day).name, name)

    def test_phases_cover_every_day_without_gaps(self):
        for earlier, later in zip(PHASES, PHASES[1:]):
            self.assertEqual(earlier.last_day + 1, later.first_day)
        self.assertEqual(PHASES[0].first_day, 0)
        self.assertIsNone(PHASES[-1].last_day)


class TipTests(unittest.TestCase):
    def test_every_day_has_tips(self):
        guide = HealingGuide()
        for day in range(0, 60):
            with self.subTest(day=day):
                self.assertTrue(guide.tips_for(day))

    def test_tips_are_filtered_by_day(self):
        guide = HealingGuide()
        bandage_tip = next(tip for tip in guide.tips_for(0) if "kötést" in tip)
        self.assertNotIn(bandage_tip, guide.tips_for(1))

    def test_care_for_combines_phase_and_tips(self):
        guide = HealingGuide()
        care = guide.care_for(7)
        self.assertEqual(care.day, 7)
        self.assertEqual(care.phase, guide.phase_for(7))
        self.assertEqual(care.tips, guide.tips_for(7))


class ParseDayTests(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(parse_day("0"), 0)
        self.assertEqual(parse_day(" 12 "), 12)

    def test_invalid_input(self):
        for raw in ("", "   ", "-1", "2.5", "abc", "²", "٣"):
            with self.subTest(raw=raw):
                self.assertIsNone(parse_day(raw))


if __name__ == "__main__":
    unittest.main()

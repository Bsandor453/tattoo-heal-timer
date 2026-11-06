"""Healing data and the logic that filters it by day. No GUI code lives here.

User-facing text is in Hungarian because that is the app's audience.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HealingPhase:
    name: str
    day_label: str
    description: str
    first_day: int
    last_day: Optional[int]  # None means open-ended

    def includes(self, day: int) -> bool:
        return self.first_day <= day and (self.last_day is None or day <= self.last_day)


@dataclass(frozen=True)
class CareTip:
    text: str
    first_day: int
    last_day: Optional[int]  # None means open-ended

    def applies_on(self, day: int) -> bool:
        return self.first_day <= day and (self.last_day is None or day <= self.last_day)


@dataclass(frozen=True)
class DailyCare:
    """Everything the UI needs to show for one day."""

    day: int
    phase: HealingPhase
    tips: tuple[str, ...]


PHASES = (
    HealingPhase(
        "Friss seb",
        "0–3. nap",
        "A bőr vörös, duzzadt és érzékeny lehet, a tetoválás nedvezhet. "
        "Ilyenkor a legfontosabb a tisztaság.",
        0,
        3,
    ),
    HealingPhase(
        "Hámlás és viszketés",
        "4–14. nap",
        "A felszín száradni és hámlani kezd, közben viszkethet. "
        "A színek átmenetileg fakónak tűnhetnek.",
        4,
        14,
    ),
    HealingPhase(
        "Regenerálódás",
        "15–30. nap",
        "A felszín többnyire már zárt, de a mélyebb rétegek még gyógyulnak. "
        "A bőr fokozatosan visszanyeri az eredeti állapotát.",
        15,
        30,
    ),
    HealingPhase(
        "Hosszú távú ápolás",
        "31. naptól",
        "A tetoválás jellemzően begyógyult. Már csak a színek és a bőr megóvása a feladat.",
        31,
        None,
    ),
)

CARE_TIPS = (
    CareTip("A kötést a tetoválód utasítása szerint vedd le, tiszta kézzel.", 0, 0),
    CareTip(
        "Minden érintés előtt moss kezet szappannal, és csak tiszta törölközőt vagy papírtörlőt használj.",
        0,
        14,
    ),
    CareTip("Naponta 2–3-szor mosd le óvatosan langyos vízzel és illatmentes szappannal.", 0, 3),
    CareTip("Mosás után itatással szárítsd, ne dörzsöld.", 0, 14),
    CareTip("Vékony rétegben kend be a tetoválód által javasolt krémmel, hogy lélegezhessen a bőr.", 0, 3),
    CareTip("Viselj laza, tiszta, pamut ruhát, ami nem dörzsöli a területet.", 0, 14),
    CareTip("Naponta 1–2-szer mosd le langyos vízzel és illatmentes szappannal.", 4, 14),
    CareTip("Ne vakard, és ne kapard le a hámló részeket vagy a pörköt: ez fertőzést és színvesztést okozhat.", 4, 14),
    CareTip("Viszketésnél vékonyan kend be illatmentes hidratálóval.", 4, 14),
    CareTip("Rövid zuhany rendben van, de ne áztasd a tetoválást.", 0, 14),
    CareTip("Kerüld a kádfürdőt, a medencét, a szaunát és a nyílt vizet.", 0, 30),
    CareTip("Tartsd távol a közvetlen napfénytől és a szoláriumtól.", 0, 30),
    CareTip("Kerüld az erős izzadást és azt, hogy a tetoválás edzés közben súrlódjon.", 0, 14),
    CareTip("Naponta hidratáld illatmentes krémmel.", 15, 30),
    CareTip("Ha egy rész még hámlik vagy érzékeny, azt továbbra is kíméld.", 15, 30),
    CareTip("Napozás előtt használj magas faktorszámú (SPF 50) naptejet.", 31, None),
    CareTip("A rendszeres hidratálás segít megőrizni a színeket.", 31, None),
    CareTip("Ha egy rész foltos maradt, kérdezd meg a tetoválódat az esetleges javításról.", 31, None),
)

WARNING_SIGNS = (
    "Fordulj orvoshoz, ha lázas vagy, ha genny jelenik meg, ha a bőrpír vagy a duzzanat "
    "terjed vagy erősödik, ha vörös csíkok indulnak a tetoválástól, vagy ha a fájdalom "
    "nem enyhül. A tanácsok tájékoztató jellegűek, nem helyettesítik az orvosi véleményt."
)


class HealingGuide:
    """Filters the healing data down to what applies on a given day."""

    def __init__(
        self,
        phases: tuple[HealingPhase, ...] = PHASES,
        tips: tuple[CareTip, ...] = CARE_TIPS,
    ) -> None:
        self.phases = phases
        self.tips = tips

    def phase_for(self, day: int) -> HealingPhase:
        for phase in self.phases:
            if phase.includes(day):
                return phase
        raise ValueError(f"No healing phase covers day {day}")

    def tips_for(self, day: int) -> tuple[str, ...]:
        return tuple(tip.text for tip in self.tips if tip.applies_on(day))

    def care_for(self, day: int) -> DailyCare:
        return DailyCare(day, self.phase_for(day), self.tips_for(day))


def parse_day(raw: str) -> Optional[int]:
    """Return the day number typed by the user, or None if it isn't a valid day."""
    text = raw.strip()
    # isascii + isdigit rejects "-1", "2.5" and non-ASCII digits like "²" that int() may choke on.
    if not (text.isascii() and text.isdigit()):
        return None
    return int(text)

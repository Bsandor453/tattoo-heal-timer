"""The Tkinter window. Only draws widgets and forwards events to the controller."""

import tkinter as tk

from tattoo_heal_timer.controller import HealingController
from tattoo_heal_timer.healing import PHASES, WARNING_SIGNS, DailyCare

FONT = "Segoe UI"
BACKGROUND = "#f7f4f1"
CARD = "#ffffff"
INK = "#2b2626"
MUTED = "#6f6663"
ACCENT = "#a8324a"
ACCENT_SOFT = "#f6e4e7"
BORDER = "#e0d9d4"
ERROR = "#b3261e"
WARNING_BACKGROUND = "#fff4e0"
WARNING_INK = "#6b4400"


class HealingWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Tetoválás gyógyulási időzítő")
        self.root.geometry("600x760")
        self.root.minsize(600, 760)  # the longest tip list (day 0) needs this much room
        self.root.configure(bg=BACKGROUND)

        self.day_text = tk.StringVar()
        # Set while the program itself writes the field, so that isn't handled as typing.
        self._updating_day_text = False
        self.phase_buttons: dict[str, tk.Button] = {}

        self._build_header()
        self._build_day_picker()
        self._build_phase_buttons()
        self._build_warning()  # packed before the card so it stays visible when space is short
        self._build_care_card()

    def _build_header(self) -> None:
        tk.Label(
            self.root,
            text="Tetoválás gyógyulási időzítő",
            font=(FONT, 20, "bold"),
            bg=BACKGROUND,
            fg=INK,
        ).pack(pady=(20, 0))
        tk.Label(
            self.root,
            text="Napi ápolási teendők a friss tetoválásodhoz",
            font=(FONT, 11),
            bg=BACKGROUND,
            fg=MUTED,
        ).pack(pady=(2, 14))

    def _build_day_picker(self) -> None:
        tk.Label(
            self.root,
            text="Hány nap telt el a tetoválás óta?",
            font=(FONT, 11),
            bg=BACKGROUND,
            fg=INK,
        ).pack()

        row = tk.Frame(self.root, bg=BACKGROUND)
        row.pack(pady=(6, 0))
        self.minus_button = self._step_button(row, "−")
        self.minus_button.pack(side="left")
        self.day_entry = tk.Entry(
            row,
            textvariable=self.day_text,
            width=5,
            justify="center",
            font=(FONT, 20, "bold"),
            fg=INK,
            bg=CARD,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self.day_entry.pack(side="left", padx=8, ipady=3)
        self.plus_button = self._step_button(row, "+")
        self.plus_button.pack(side="left")

        self.error_label = tk.Label(
            self.root, text="", font=(FONT, 10), bg=BACKGROUND, fg=ERROR
        )
        self.error_label.pack(pady=(4, 4))

    def _step_button(self, parent: tk.Widget, text: str) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            width=3,
            font=(FONT, 16, "bold"),
            fg=ACCENT,
            bg=CARD,
            activebackground=ACCENT_SOFT,
            activeforeground=ACCENT,
            relief="flat",
            highlightthickness=0,
            cursor="hand2",
        )

    def _build_phase_buttons(self) -> None:
        row = tk.Frame(self.root, bg=BACKGROUND)
        row.pack(fill="x", padx=24, pady=(0, 12))
        for column, phase in enumerate(PHASES):
            row.columnconfigure(column, weight=1, uniform="phase")
            button = tk.Button(
                row,
                text=phase.day_label,
                font=(FONT, 10),
                relief="flat",
                pady=6,
                cursor="hand2",
            )
            button.grid(row=0, column=column, sticky="ew", padx=2)
            self.phase_buttons[phase.name] = button

    def _build_care_card(self) -> None:
        card = tk.Frame(
            self.root, bg=CARD, highlightthickness=1, highlightbackground=BORDER
        )
        card.pack(fill="both", expand=True, padx=26, pady=(0, 12))

        self.phase_label = tk.Label(
            card, font=(FONT, 15, "bold"), bg=CARD, fg=ACCENT, anchor="w"
        )
        self.phase_label.pack(fill="x", padx=16, pady=(14, 2))
        self.description_label = tk.Label(
            card, font=(FONT, 10), bg=CARD, fg=MUTED, anchor="w", justify="left"
        )
        self.description_label.pack(fill="x", padx=16)
        tk.Label(
            card,
            text="Mai teendők",
            font=(FONT, 11, "bold"),
            bg=CARD,
            fg=INK,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(12, 2))
        self.tips_label = tk.Label(
            card, font=(FONT, 10), bg=CARD, fg=INK, anchor="nw", justify="left"
        )
        self.tips_label.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        # Keep the text wrapped to the card's current width when the window is resized.
        card.bind("<Configure>", self._rewrap_card_text)

    def _rewrap_card_text(self, event: tk.Event) -> None:
        width = event.width - 34
        self.description_label.configure(wraplength=width)
        self.tips_label.configure(wraplength=width)

    def _build_warning(self) -> None:
        warning = tk.Label(
            self.root,
            text=WARNING_SIGNS,
            font=(FONT, 9),
            bg=WARNING_BACKGROUND,
            fg=WARNING_INK,
            justify="left",
            anchor="w",
            padx=12,
            pady=8,
        )
        warning.pack(side="bottom", fill="x", padx=26, pady=(0, 18))
        warning.bind(
            "<Configure>", lambda event: warning.configure(wraplength=event.width - 26)
        )

    def bind_events(self, controller: HealingController) -> None:
        self.minus_button.configure(command=lambda: controller.on_step(-1))
        self.plus_button.configure(command=lambda: controller.on_step(1))
        for phase in PHASES:
            self.phase_buttons[phase.name].configure(
                command=lambda selected=phase: controller.on_phase_selected(selected)
            )
        self.day_text.trace_add(
            "write", lambda *_: self._handle_typing(controller)
        )
        self.day_entry.bind("<Up>", lambda _: controller.on_step(1))
        self.day_entry.bind("<Down>", lambda _: controller.on_step(-1))

    def _handle_typing(self, controller: HealingController) -> None:
        if not self._updating_day_text:
            controller.on_day_typed(self.day_text.get())

    def show_care(self, care: DailyCare) -> None:
        self.error_label.configure(text="")
        self.phase_label.configure(text=f"{care.day}. nap · {care.phase.name}")
        self.description_label.configure(text=care.phase.description)
        self.tips_label.configure(text="\n".join(f"•  {tip}" for tip in care.tips))
        for name, button in self.phase_buttons.items():
            selected = name == care.phase.name
            button.configure(
                bg=ACCENT if selected else CARD,
                fg="white" if selected else INK,
                activebackground=ACCENT if selected else ACCENT_SOFT,
                activeforeground="white" if selected else INK,
            )

    def show_input_error(self, message: str) -> None:
        self.error_label.configure(text=message)

    def set_day_text(self, text: str) -> None:
        self._updating_day_text = True
        self.day_text.set(text)
        self._updating_day_text = False

    def run(self) -> None:
        self.day_entry.focus_set()
        self.root.mainloop()

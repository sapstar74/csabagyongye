"""A kvízmenet logikája – Streamlit nélkül is tesztelhető."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .answers import Verdict, check, typeable
from .catalog import Question


class Input(str, Enum):
    CHOICE = "choice"   # négy lehetőség közül
    TYPE = "type"       # szabad szöveges beírás

    @property
    def label(self) -> str:
        return {"choice": "Választás", "type": "Beírás"}[self.value]

    @property
    def hint(self) -> str:
        return {
            "choice": "Négy lehetőség közül választasz.",
            "type": "Magad írod be a választ. Az ékezet- és kisebb elírási hibát elfogadjuk; "
                    "ahol a válasz túl hosszú lenne, ott választani kell.",
        }[self.value]


class Mode(str, Enum):
    SERIES = "series"   # adott számú kérdés
    SUDDEN = "sudden"   # az első hibáig tart

    @property
    def label(self) -> str:
        return {"series": "Kérdéssor", "sudden": "Hirtelen halál"}[self.value]

    @property
    def hint(self) -> str:
        return {
            "series": "Annyi kérdés, amennyit beállítasz.",
            "sudden": "Addig megy, amíg nem hibázol. Meddig jutsz?",
        }[self.value]


class Feedback(str, Enum):
    NOW = "now"         # minden válasz után kiderül, jó-e (magyarázattal)
    END = "end"         # csak a menet végén

    @property
    def label(self) -> str:
        return {"now": "Rögtön a válasz után", "end": "Csak a végén"}[self.value]


@dataclass
class Item:
    """Egy kérdés a menetben, megkevert válaszokkal."""
    question: Question
    order: list[int]                    # order[i] = eredeti index az i. helyen
    picked: Optional[int] = None        # a megjelenített sorrend szerinti index; -1 = hibás beírás
    typed: Optional[str] = None         # a beírt válasz szövege
    verdict: Optional[Verdict] = None   # beírásnál: pontos / elfogadott / hibás
    hinted: bool = False                # beírás helyett megnézte a lehetőségeket

    @property
    def options(self) -> list[str]:
        return [self.question.options[i] for i in self.order]

    @property
    def correct_pos(self) -> int:
        return self.order.index(self.question.correct)

    @property
    def answered(self) -> bool:
        return self.picked is not None

    @property
    def is_correct(self) -> bool:
        return self.picked == self.correct_pos

    @property
    def your_answer(self) -> str:
        if self.typed is not None:
            return self.typed
        return self.options[self.picked] if self.picked is not None and self.picked >= 0 else ""


@dataclass
class Session:
    mode: Mode
    items: list[Item]
    reserve: list[Question] = field(default_factory=list)  # hirtelen halálhoz
    cursor: int = 0
    seed: int = 0
    input: Input = Input.CHOICE
    feedback: Feedback = Feedback.NOW

    @property
    def instant(self) -> bool:
        return self.feedback is Feedback.NOW

    def typing_now(self) -> bool:
        """Az aktuális kérdésnél beviteli mezőt mutatunk-e."""
        it = self.current
        return bool(it and self.input is Input.TYPE and not it.hinted and typeable(it.question))

    # -- állapot ----------------------------------------------------------
    @property
    def current(self) -> Optional[Item]:
        return self.items[self.cursor] if self.cursor < len(self.items) else None

    @property
    def answered_items(self) -> list[Item]:
        return [it for it in self.items if it.answered]

    @property
    def score(self) -> int:
        return sum(1 for it in self.items if it.is_correct)

    @property
    def finished(self) -> bool:
        return self.cursor >= len(self.items)

    @property
    def total(self) -> int:
        return len(self.items)

    # -- műveletek --------------------------------------------------------
    def answer_text(self, text: str) -> bool:
        it = self.current
        if it is None or it.answered or not text.strip():
            return False
        q = it.question
        others = []
        for i, o in enumerate(it.options):
            if i != it.correct_pos:
                others += [o] + q.aliases.get(o, [])
        it.typed = text.strip()
        it.verdict = check(text, q.correct_text, others, q.aliases.get(q.correct_text, []))
        return self.answer(it.correct_pos if it.verdict is not Verdict.WRONG else -1)

    def answer(self, pos: int) -> bool:
        it = self.current
        if it is None or it.answered:
            return False
        it.picked = pos
        # Hirtelen halálban helyes válasz után a tartalékból bővítünk.
        if self.mode is Mode.SUDDEN and it.is_correct and self.cursor == len(self.items) - 1 and self.reserve:
            self.items.append(_make_item(self.reserve.pop(), random.Random(self.seed + len(self.items))))
        return it.is_correct

    def advance(self) -> None:
        if self.mode is Mode.SUDDEN and self.current and self.current.answered and not self.current.is_correct:
            # vége: a kurzor a hibás kérdésen marad, a `finished` igaz
            self.items = self.items[: self.cursor + 1]
            self.cursor = len(self.items)
            return
        self.cursor += 1

    def by_topic(self) -> dict[str, tuple[int, int]]:
        """téma → (helyes, összes) a megválaszolt kérdésekből."""
        out: dict[str, list[int]] = {}
        for it in self.answered_items:
            c = out.setdefault(it.question.topic, [0, 0])
            c[1] += 1
            c[0] += int(it.is_correct)
        return {k: (v[0], v[1]) for k, v in out.items()}

    def mistakes(self) -> list[Question]:
        return [it.question for it in self.answered_items if not it.is_correct]


def _make_item(q: Question, rng: random.Random) -> Item:
    order = list(range(len(q.options)))
    rng.shuffle(order)
    return Item(question=q, order=order)


def build_session(
    bank: dict[str, list[Question]],
    topics: list[str],
    count: int,
    mode: Mode,
    seed: Optional[int] = None,
    only: Optional[list[Question]] = None,
    input: Input = Input.CHOICE,
    feedback: Feedback = Feedback.NOW,
) -> Session:
    """Új menet.

    A kérdéseket a témák között egyenletesen osztja szét, így egy nagy téma
    (pl. világtörténelem) nem szorítja ki a kicsiket.
    """
    seed = seed if seed is not None else random.randrange(1 << 30)
    rng = random.Random(seed)

    if only is not None:
        pool = list(only)
        rng.shuffle(pool)
        picked, reserve = pool, []
    else:
        per_topic = {t: rng.sample(bank[t], len(bank[t])) for t in topics if bank.get(t)}
        picked: list[Question] = []
        target = count if mode is not Mode.SUDDEN else min(10, count)
        # körforgó húzás
        while len(picked) < target and any(per_topic.values()):
            for t in list(per_topic):
                if per_topic[t] and len(picked) < target:
                    picked.append(per_topic[t].pop())
        rng.shuffle(picked)
        reserve = [q for qs in per_topic.values() for q in qs]
        rng.shuffle(reserve)

    items = [_make_item(q, rng) for q in picked]
    return Session(mode=mode, items=items, reserve=reserve if mode is Mode.SUDDEN else [], seed=seed, input=input, feedback=feedback)

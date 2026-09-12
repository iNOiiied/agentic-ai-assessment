import math
import statistics
from collections import defaultdict

SCALE_LABELS = {
    "E": "Extraversion",
    "A": "Agreeableness",
    "C": "Conscientiousness",
    "N": "Neuroticism",
    "O": "Openness / Intellect",
    "AI_ADOPT": "AI Adoption Attitude",
    "AI_CRIT": "Critical AI Use",
}

# Mini-IPIP 20 items (Donnellan et al., 2006).
PERSONALITY_ITEMS = [
    ("P01", "Am the life of the party.", "E", False),
    ("P02", "Sympathize with others' feelings.", "A", False),
    ("P03", "Get chores done right away.", "C", False),
    ("P04", "Have frequent mood swings.", "N", False),
    ("P05", "Have a vivid imagination.", "O", False),
    ("P06", "Don't talk a lot.", "E", True),
    ("P07", "Am not interested in other people's problems.", "A", True),
    ("P08", "Often forget to put things back in their proper place.", "C", True),
    ("P09", "Am relaxed most of the time.", "N", True),
    ("P10", "Am not interested in abstract ideas.", "O", True),
    ("P11", "Talk to a lot of different people at parties.", "E", False),
    ("P12", "Feel others' emotions.", "A", False),
    ("P13", "Like order.", "C", False),
    ("P14", "Get upset easily.", "N", False),
    ("P15", "Have difficulty understanding abstract ideas.", "O", True),
    ("P16", "Keep in the background.", "E", True),
    ("P17", "Am not really interested in others.", "A", True),
    ("P18", "Make a mess of things.", "C", True),
    ("P19", "Seldom feel blue.", "N", True),
    ("P20", "Do not have a good imagination.", "O", True),
]

# Exploratory, self-authored items for this challenge; not a validated instrument.
ATTITUDE_ITEMS = [
    ("A01", "AI tools can help me learn complex topics more efficiently.", "AI_ADOPT", False),
    ("A02", "I am willing to experiment with new AI tools when they may be useful.", "AI_ADOPT", False),
    ("A03", "I would use AI to generate options before making a difficult decision.", "AI_ADOPT", False),
    ("A04", "I avoid AI tools even when they could save me time.", "AI_ADOPT", True),
    ("A05", "I would rather not learn how to use new AI tools.", "AI_ADOPT", True),
    ("A06", "Using AI usually makes learning less effective for me.", "AI_ADOPT", True),
    ("A07", "I check important claims before relying on an AI-generated answer.", "AI_CRIT", False),
    ("A08", "I compare AI suggestions with other evidence when the decision matters.", "AI_CRIT", False),
    ("A09", "I tend to accept AI-generated information without checking it.", "AI_CRIT", True),
    ("A10", "If an AI answer sounds confident, I assume it is correct.", "AI_CRIT", True),
]

ALL_ITEMS = PERSONALITY_ITEMS + ATTITUDE_ITEMS
ITEM_BY_ID = {item[0]: item for item in ALL_ITEMS}


def score_response(raw_value: int, reverse_keyed: bool) -> int:
    if raw_value not in (1, 2, 3, 4, 5):
        raise ValueError("Responses must be integers from 1 to 5.")
    return 6 - raw_value if reverse_keyed else raw_value


def calculate_scale_scores(raw_answers: dict[str, int]) -> dict[str, float]:
    grouped = defaultdict(list)
    for item_id, raw in raw_answers.items():
        if item_id not in ITEM_BY_ID:
            raise ValueError(f"Unknown item: {item_id}")
        _, _, scale, reverse_keyed = ITEM_BY_ID[item_id]
        grouped[scale].append(score_response(int(raw), reverse_keyed))
    expected_counts = {"E": 4, "A": 4, "C": 4, "N": 4, "O": 4, "AI_ADOPT": 6, "AI_CRIT": 4}
    for scale, count in expected_counts.items():
        if len(grouped[scale]) != count:
            raise ValueError(f"Incomplete scale {scale}: expected {count} responses.")
    return {scale: round(sum(values) / len(values), 3) for scale, values in grouped.items()}


def cronbach_alpha(rows: list[list[float]]) -> float | None:
    if len(rows) < 2 or not rows or len(rows[0]) < 2:
        return None
    k = len(rows[0])
    if any(len(row) != k for row in rows):
        return None
    try:
        item_variances = [statistics.variance(col) for col in zip(*rows)]
        totals = [sum(row) for row in rows]
        total_variance = statistics.variance(totals)
    except statistics.StatisticsError:
        return None
    if total_variance <= 0:
        return None
    return round((k / (k - 1)) * (1 - sum(item_variances) / total_variance), 3)


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 3:
        return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return None
    return round(num / (den_x * den_y), 3)

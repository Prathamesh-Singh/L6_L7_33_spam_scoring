import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ---------------- score_message ----------------

def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


def test_spam_word_adds_two():
    # "free" and "winner!" (punctuation stripped) are spam words
    assert score_message("free winner!", False, 0) == 4


def test_shouting_word_adds_one():
    # "HELLO" is all uppercase and longer than 3 characters
    assert score_message("HELLO friend", False, 0) == 1


def test_many_links_add_four():
    assert score_message("check this", False, 5) == 4


def test_few_links_add_one():
    assert score_message("check this", False, 2) == 1


def test_known_sender_score_floored_at_zero():
    # score 0 - 3 would be negative, so it is clamped to 0
    assert score_message("hello", True, 0) == 0


# ---------------- classify ----------------

def test_high_score_is_spam():
    assert classify(10) == "spam"


def test_mid_score_is_suspicious():
    assert classify(5) == "suspicious"


def test_low_score_is_clean():
    assert classify(1) == "clean"


# ---------------- filter_inbox ----------------

def test_filter_inbox_counts_labels():
    messages = [
        ("free cash prize winner", False, 0),   # 8  -> spam
        ("free cash", False, 0),                # 4  -> suspicious
        ("hello there", False, 0),              # 0  -> clean
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


# ---------------- inbox_status ----------------

def test_empty_inbox():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_flooded_inbox():
    assert inbox_status({"spam": 6, "suspicious": 2, "clean": 2}) == "flooded"


def test_noisy_inbox():
    assert inbox_status({"spam": 3, "suspicious": 2, "clean": 5}) == "noisy"


def test_healthy_inbox():
    assert inbox_status({"spam": 1, "suspicious": 1, "clean": 8}) == "healthy"

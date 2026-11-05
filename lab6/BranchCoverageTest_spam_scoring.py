import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ---------------- score_message ----------------
# Branches: for-loop (enters / skips), spam-word if (T/F), shouting elif (T/F),
# link_count > 3 (T/F), link_count > 0 (T/F), sender_known (T/F),
# score < 0 after penalty (T/F)

def test_empty_text_skips_loop():
    # for-loop body never executes
    assert score_message("", False, 0) == 0


def test_plain_message_scores_zero():
    # neither spam word nor shouting word -> both if/elif False
    assert score_message("hello there", False, 0) == 0


def test_spam_word_adds_two():
    assert score_message("free winner!", False, 0) == 4


def test_spam_word_is_case_insensitive_and_strips_punctuation():
    assert score_message("CASH, Prize.", False, 0) == 4


def test_shouting_word_adds_one():
    assert score_message("HELLO friend", False, 0) == 1


def test_short_uppercase_word_not_counted():
    # isupper() True but len <= 3 -> elif False
    assert score_message("OK BYE", False, 0) == 0


def test_no_links_adds_nothing():
    assert score_message("hi", False, 0) == 0


def test_one_link_adds_one():
    assert score_message("hi", False, 1) == 1


def test_three_links_boundary_adds_one():
    assert score_message("hi", False, 3) == 1


def test_four_links_boundary_adds_four():
    assert score_message("hi", False, 4) == 4


def test_unknown_sender_no_penalty():
    assert score_message("free", False, 0) == 2


def test_known_sender_score_floored_at_zero():
    # score < 0 after penalty -> True branch
    assert score_message("hello", True, 0) == 0


def test_known_sender_score_stays_positive():
    # score >= 0 after penalty -> False branch of inner if
    # free(2) + cash(2) + prize(2) + 5 links(4) = 10 - 3 = 7
    assert score_message("free cash prize", True, 5) == 7


def test_known_sender_score_exactly_zero():
    # 2 + 1 = 3 - 3 = 0 -> not < 0
    assert score_message("free", True, 1) == 0


# ---------------- classify ----------------

def test_high_score_is_spam():
    assert classify(10) == "spam"


def test_boundary_eight_is_spam():
    assert classify(8) == "spam"


def test_boundary_seven_is_suspicious():
    assert classify(7) == "suspicious"


def test_boundary_four_is_suspicious():
    assert classify(4) == "suspicious"


def test_boundary_three_is_clean():
    assert classify(3) == "clean"


def test_low_score_is_clean():
    assert classify(1) == "clean"


# ---------------- filter_inbox ----------------

def test_filter_inbox_empty_list():
    # for-loop never executes
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}


def test_filter_inbox_counts_labels():
    messages = [
        ("free cash prize winner", False, 0),   # 8  -> spam
        ("free cash", False, 0),                # 4  -> suspicious
        ("hello there", False, 0),              # 0  -> clean
        ("URGENT free offer", True, 5),         # 2+2+4-3 = 5 -> suspicious
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 2, "clean": 1}


# ---------------- inbox_status ----------------

def test_empty_inbox():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_flooded_inbox():
    assert inbox_status({"spam": 6, "suspicious": 2, "clean": 2}) == "flooded"


def test_exactly_half_spam_is_noisy():
    # ratio == 0.5 -> not > 0.5
    assert inbox_status({"spam": 5, "suspicious": 0, "clean": 5}) == "noisy"


def test_noisy_inbox():
    assert inbox_status({"spam": 3, "suspicious": 2, "clean": 5}) == "noisy"


def test_exactly_twenty_percent_spam_is_healthy():
    # ratio == 0.2 -> not > 0.2
    assert inbox_status({"spam": 2, "suspicious": 0, "clean": 8}) == "healthy"


def test_healthy_inbox():
    assert inbox_status({"spam": 1, "suspicious": 1, "clean": 8}) == "healthy"


def test_status_from_filtered_inbox():
    counts = filter_inbox([("free cash prize winner", False, 0)])
    assert inbox_status(counts) == "flooded"

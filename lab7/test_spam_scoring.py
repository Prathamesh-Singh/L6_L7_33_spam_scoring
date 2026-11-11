from hypothesis import given, settings, strategies as st
from spam_scoring import sender_domain, first_link, shout_ratio


# ---------------- No-crash fuzz tests ----------------
# Hypothesis feeds random Unicode strings (and None) to each function.
# A robust function must never raise an exception, whatever the input.

@settings(max_examples=500)
@given(st.text() | st.none())
def test_sender_domain_no_crash(s):
    try:
        sender_domain(s)
    except Exception as e:
        assert False, f"sender_domain crashed with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_first_link_no_crash(s):
    try:
        first_link(s)
    except Exception as e:
        assert False, f"first_link crashed with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_shout_ratio_no_crash(s):
    try:
        shout_ratio(s)
    except Exception as e:
        assert False, f"shout_ratio crashed with: {type(e).__name__}: {e}"


# ---------------- Property-based fuzz tests ----------------
# Beyond "does not crash", check that the output always makes sense.

@given(st.text() | st.none())
def test_sender_domain_returns_clean_string(s):
    result = sender_domain(s)
    assert isinstance(result, str)
    assert "@" not in result
    assert result == result.lower()


@given(st.text(), st.text())
def test_sender_domain_extracts_domain(local, domain):
    # For any "local@domain" with no '@' in domain, the domain part is returned
    domain = domain.replace("@", "")
    assert sender_domain(f"{local}@{domain}") == domain.strip().lower()


@given(st.text() | st.none())
def test_first_link_is_link_or_empty(s):
    result = first_link(s)
    assert isinstance(result, str)
    if result:
        assert result.startswith("http")
        assert result in s
        assert not any(c.isspace() for c in result)


@given(st.text() | st.none())
def test_shout_ratio_between_zero_and_one(s):
    result = shout_ratio(s)
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


# ---------------- Example-based checks for known inputs ----------------

def test_examples():
    assert sender_domain("offers@Deals.com") == "deals.com"
    assert sender_domain("no-at-sign") == ""
    assert first_link("visit http://x.com now") == "http://x.com"
    assert first_link("no link here") == ""
    assert shout_ratio("FREE prizes") == 0.4
    assert shout_ratio("1234 !!!") == 0.0

def sender_domain(email):
    """Return the lower-cased domain of an email address, or "" if invalid."""
    if not isinstance(email, str) or "@" not in email:
        return ""
    # Take the part after the LAST '@' so "a@b@c.com" gives "c.com"
    domain = email.rsplit("@", 1)[1]
    return domain.strip().lower()


def first_link(text):
    """Return the first word starting with 'http' in text, or "" if none."""
    if not isinstance(text, str):
        return ""
    start = text.find("http")
    if start == -1:
        return ""
    end = start
    # Stop at any whitespace (space, tab, newline, ...), not only ' '
    while end < len(text) and not text[end].isspace():
        end += 1
    return text[start:end]


def shout_ratio(text):
    """Return the fraction of letters that are uppercase (0.0 if no letters)."""
    if not isinstance(text, str):
        return 0.0
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    upper = [c for c in letters if c.isupper()]
    return len(upper) / len(letters)


def main():
    print("==== Running sender_domain ====")
    user_input = input("Enter a sender email (e.g. offers@Deals.com): ")
    result = sender_domain(user_input)
    if result:
        print("Sender Domain:", result)
    else:
        print("Sender Domain: <invalid email - no domain found>")

    print("\n==== Running first_link ====")
    user_input = input("Enter a message containing a link: ")
    result = first_link(user_input)
    if result:
        print("First Link:", result)
    else:
        print("First Link: <no link found>")

    print("\n==== Running shout_ratio ====")
    user_input = input("Enter a message (e.g. FREE prize NOW): ")
    result = shout_ratio(user_input)
    print("Uppercase Ratio:", result)


if __name__ == "__main__":
    main()

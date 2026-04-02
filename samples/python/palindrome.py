def is_palindrome(s: str) -> bool:
    """
    Checks if a string is a palindrome.
    Tests string manipulation and boolean logic.
    """
    newStr = ""
    for c in s:
        if c.isalnum():
            newStr += c.lower()
    return newStr == newStr[::-1]

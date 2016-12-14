import re


def supports_TLS(s):
    if [m for m in re.findall(r"\[\w*(\w)(\w)\2\1\w*\]", s) if len(set(m)) == 2]:
        return False
    return len([ m for m in re.findall(r"(\w)(\w)\2\1", s) if len(set(m)) == 2]) > 0

with open('day7input.txt', 'r') as f:
    print(len([m for m in f.readlines() if supports_TLS(m.strip())]))
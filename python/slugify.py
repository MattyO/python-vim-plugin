from itertools import tee
import string
import re


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def text_parts(text):
    t = re.split("([\s\-A-Z])", text)
    t = [ i for i in t if i != '' ]

    if len(t) == 1:
        return t

    accum = []
    skip_next = False
    pw = list(pairwise(t))
    print(pw)
    for i, (one, two) in enumerate(pw):
        if skip_next:
            skip_next = False
            continue
        if one in string.ascii_uppercase and two not in ['-',' ']:
            accum.append(one + two)
            skip_next = True
        else:
            accum.append(one)
            if i == len(pw) - 1:
                accum.append(two)

    return list(filter(lambda i: i not in [' ', '-'], accum))


def camel(text):
    return "".join(map(lambda t: t.capitalize(),  text_parts(text)))

def snake(text):
    return "_".join(map(lambda t: t.lower(),  text_parts(text)))

def slug(text):
    return "-".join(map(lambda t: t.lower(),  text_parts(text)))



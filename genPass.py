import argparse
import sys
from collections import OrderedDict

# =========================
# v0.5.5 (light mode: w-first)
# =========================

ALL_CHARACTERS = [
    '!', '@', '#', '$', '%', '^',
    '&', '*', '_', '-', '+', '=',
    '.', '(', ')', ';', ':', '~'
]
COMMON_CHARACTERS = [
    '!@#', '@#$', '#$%', '$%^', '%^&', '^&*',
    '!@', '@#', '#$', '$%', '%^', '^&',
    '#@!', '$#@', '%#$', '^$%', '&^%', '*&^'
]

BASE_DIGITS_DEFAULT = [
    '1', '11', '111', '1111', '2', '22', '12', '1212',
    '123', '123123', '12312', '1234', '1324', '123412',
    '1100', '1004', '23', '234', '12345', '10', '100'
]
BASE_DIGITS_LIGHT = ['1', '12', '11', '123']

characters = []
base_digits = list(BASE_DIGITS_DEFAULT)
LIGHT_MODE = False

def _unique(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _normalize_digits(base, extNumber):
    digits = list(base)
    if extNumber is not None:
        if isinstance(extNumber, list):
            digits.extend(str(n) for n in extNumber if n is not None and str(n) != '')
        else:
            s = str(extNumber)
            if s != '':
                digits.append(s)
    return _unique(digits)

def _normalize_tokens(extChar):
    if not extChar:
        return []
    tokens = extChar if isinstance(extChar, list) else [extChar]
    variants = []
    for t in tokens:
        for v in (t, t.upper(), t.capitalize()):
            if v not in variants:
                variants.append(v)
    return variants

def _expand(wordlist, digits, include_plain_word):
    words = _unique(wordlist)
    digits = _unique(digits)

    if LIGHT_MODE:
        # w
        if include_plain_word:
            for w in words:
                yield w
        # w+d
        for w in words:
            for d in digits:
                yield w + d
        # w+c
        for w in words:
            for c in characters:
                yield w + c
        # w+d+c, w+c+d
        for w in words:
            for d in digits:
                for c in characters:
                    yield w + d + c
                    yield w + c + d
        return

    # ===== FULL MODE (기존 동작) =====
    if include_plain_word:
        for w in words:
            yield w

    for w in words:
        for d in digits:
            yield w + d
            yield d + w

    for w in words:
        for c in characters:
            yield w + c
            yield c + w

    for w in words:
        for d in digits:
            for c in characters:
                yield w + d + c
                yield w + c + d
                yield d + w + c
                yield d + c + w
                yield c + w + d
                yield c + d + w

def printError(case, filename):
    if case == 1:
        print("[-] This tool requires a input file; you missed the '-f' flag.")
        sys.exit(1)
    elif case == 2:
        print("[-] This tool requires an output file; you missed the '-o' flag.")
        sys.exit(1)
    elif case == 3:
        print(f'[-] This tool requires four or six string arguments in {filename}.')
        sys.exit(1)

def getArgs():
    parser = argparse.ArgumentParser(
        description="password generator v0.5.5",
        epilog="[Example] genPass.py -f users.txt -o passlist.txt --light -c $$$,&&&",
    )
    parser.add_argument("-f", "--file", required=False, help="Input file that has usernames")
    parser.add_argument("-o", "--output", required=True, help="Output file you want to save")
    parser.add_argument("-n", "--number", type=lambda s: s.split(','), help="Use extra number", default=None)
    parser.add_argument("-c", "--char", type=lambda s: s.split(','), help="Use extra character", default=None)
    parser.add_argument("-L", "--light", action="store_true",
                        help="Generate a lightweight list (w-first only; limited digits; no easy base)")
    args = parser.parse_args()
    return args.file, args.output, args.number, args.char, args.light

def checkOptions(input, output, extNumber, extChar):
    if input is None and (extChar is None or len(extChar) == 0):
        printError(1, input)
    if output is None:
        printError(2, input)

    if input is not None:
        with open(input, 'r') as file:
            userInputFile = [line.strip().split() for line in file.readlines()]

        for idx in range(len(userInputFile)):
            if len(userInputFile[idx]) == 4:
                intCnt = 0
                for item in userInputFile[idx]:
                    try:
                        int(item); intCnt += 1
                    except ValueError:
                        continue
                if intCnt >= 1:
                    printError(3, input)

            elif len(userInputFile[idx]) == 6:
                intCnt = 0
                for item in userInputFile[idx]:
                    try:
                        int(item); intCnt += 1
                    except ValueError:
                        continue
                if intCnt >= 1:
                    printError(3, input)
            else:
                printError(3, input)

def splitName(path):
    with open(path, 'r') as file:
        lst = [line.strip().split() for line in file.readlines()]
    return lst

def makePasswordList(lst):
    result = []
    if len(lst) == 4:
        enFirst, enLast = lst[0], lst[1]
        koFirst, koLast = lst[2], lst[3]
        result.extend([
            enFirst + enLast,
            enFirst.capitalize() + enLast,
            enFirst.capitalize() + enLast.capitalize(),
            koFirst + koLast,
            koFirst.capitalize() + koLast,
            koFirst.capitalize() + koLast.capitalize(),
            enFirst,
            enFirst.capitalize(),
            enLast,
            enLast.capitalize(),
            enFirst[0] + enLast[0],
            enFirst[0].upper() + enLast[0],
            enFirst[0].upper() + enLast[0].upper()
        ])

    elif len(lst) == 6:
        enFirst, enMiddle, enLast = lst[0], lst[1], lst[2]
        koFirst, koMiddle, koLast = lst[3], lst[4], lst[5]
        result.extend([
            koFirst + koMiddle + koLast,
            koFirst.capitalize() + koMiddle + koLast,
            koFirst.capitalize() + koMiddle.capitalize() + koLast.capitalize(),
            koMiddle + koLast,
            koMiddle.capitalize() + koLast,
            koMiddle.upper() + koLast,
            koFirst,
            koFirst.capitalize(),
            koMiddle,
            koMiddle.capitalize(),
            koLast,
            koLast.capitalize(),
            enFirst[0] + enMiddle[0] + enLast[0],
            enFirst[0].upper() + enMiddle[0].upper() + enLast[0].upper(),
            enFirst[0].upper() + enMiddle[0] + enLast[0],
            enFirst + enMiddle + enLast,
            enFirst.capitalize() + enMiddle + enLast,
            enFirst.capitalize() + enMiddle.capitalize() + enLast.capitalize(),
            enFirst.upper() + enMiddle + enLast,
            enFirst.upper() + enMiddle.upper() + enLast.upper(),
            enFirst[0] + enMiddle + enLast,
            enFirst[0].upper() + enMiddle + enLast,
            enFirst[0].upper() + enMiddle.capitalize() + enLast,
            enFirst[0].upper() + enMiddle.capitalize() + enLast.capitalize(),
            enFirst[0].upper() + enMiddle.upper() + enLast,
            enFirst[0].upper() + enMiddle.upper() + enLast.upper(),
            enFirst + enMiddle[0] + enLast[0],
            enFirst.capitalize() + enMiddle[0] + enLast[0],
            enFirst + enMiddle[0].upper() + enLast,
            enFirst.capitalize() + enMiddle[0].upper() + enLast[0].upper(),
            enFirst.upper() + enMiddle[0] + enLast[0],
            enFirst.upper() + enMiddle.upper() + enLast.upper(),
            enMiddle + enLast,
            enMiddle.capitalize() + enLast,
            enMiddle.capitalize() + enLast.capitalize(),
            enMiddle.upper() + enLast,
            enMiddle.upper() + enLast.upper(),
            enMiddle[0] + enLast,
            enMiddle[0].upper() + enLast,
            enFirst,
            enFirst.capitalize(),
            enMiddle,
            enMiddle.capitalize(),
            enLast,
            enLast.capitalize()
        ])
    else:
        printError(3, "(input)")

    return _unique(result)

def addPattern(wordlist, extNumber):
    digits = _normalize_digits(base_digits, extNumber)
    return _expand(wordlist, digits, include_plain_word=True)

def makeExtCharWordlist(extChar, extNumber=None):
    if LIGHT_MODE:
        digits_base = list(BASE_DIGITS_LIGHT)
    else:
        digits_base = [
            '1', '11', '111', '1111', '2', '22', '222', '12', '1212',
            '34', '23', '234', '123', '1234', '1324', '1100', '1004', '12345', '10', '100',
            '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'
        ]
    digits = _normalize_digits(digits_base, extNumber)
    variants = _normalize_tokens(extChar)
    return _expand(variants, digits, include_plain_word=False)

def _dedupe_file_inplace(path):
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    unique_lines = list(OrderedDict.fromkeys(lines))
    if len(unique_lines) != len(lines):
        with open(path, 'w') as f:
            f.write("\n".join(unique_lines))
    return len(lines), len(unique_lines)

def build_characters(light):
    if light:
        return list(ALL_CHARACTERS) + list(COMMON_CHARACTERS)
    out = []
    for c in ALL_CHARACTERS:
        out.append(c)
        out.append(c * 2)
        out.append(c * 3)
    return out + list(COMMON_CHARACTERS)

def main():
    global LIGHT_MODE, characters, base_digits

    input, output, extNumber, extChar, LIGHT_MODE = getArgs()
    checkOptions(input, output, extNumber, extChar)

    characters = build_characters(LIGHT_MODE)
    base_digits = list(BASE_DIGITS_LIGHT) if LIGHT_MODE else list(BASE_DIGITS_DEFAULT)

    splitNameList = splitName(input) if input is not None else []
    wordlist = []
    for part in splitNameList:
        wordlist.extend(makePasswordList(part))
    wordlist = _unique(wordlist)

    with open(output, 'w') as file:
        first = True
        seen = set()

        def _write_line(s):
            nonlocal first, seen
            if s in seen:
                return
            seen.add(s)
            if first:
                file.write(s); first = False
            else:
                file.write("\n"); file.write(s)

        for pw in addPattern(wordlist, extNumber):
            _write_line(pw)

        # FULL 모드에서만 기존 easy 베이스 유지 (LIGHT 모드는 완전 제외)
        if not LIGHT_MODE:
            easyCharactors = [
                'q1w2e3r4', 'qwer', 'qwe', 'qwqw', 'qwqwqw', 'qweqwe', 'qweqweqwe', 'passwd',
                'password', 'P@ssw0rd', 'asd', 'asdf', '1q2w3e4r', 'q1w2e3', '1q2w3e', 'q1w2', '1q2w'
            ]
            for pw in _expand(
                _unique(easyCharactors),
                _unique(['1','11','111','1111','2','22','222','12','1212','34','23','234','123','1234','1324','1100','1004','12345','10','100']),
                include_plain_word=False
            ):
                _write_line(pw)

        if extChar is not None:
            for pw in makeExtCharWordlist(extChar, extNumber):
                _write_line(pw)

    raw_count, uniq_count = _dedupe_file_inplace(output)

    mode = "LIGHT" if LIGHT_MODE else "FULL"
    print('[*] password generator v0.5.5 - Copyright 2025 All rights reserved by mick3y')
    print(f'[+] Mode            : {mode}')
    print(f'[+] output file     : {output}')
    print(f'[+] total candidates: {uniq_count} (raw: {raw_count})')

if __name__ == "__main__":
    main()

import argparse
import sys
from collections import OrderedDict

# 특수문자 패턴 (전역)
allCharacters = [
    '!', '@', '#', '$', '%', '^',
    '&', '*', '_', '-', '+', '=',
    '.', '(', ')', ';', ':', '~'
]
characters = []
commonCharacters = [
    '!@#', '@#$', '#$%', '$%^', '%^&', '^&*',
    '!@', '@#', '#$', '$%', '%^', '^&',
    '#@!', '$#@', '%#$', '^$%', '&^%', '*&^'
]
for c in allCharacters:
    characters.append(c)
    characters.append(c * 2)
    characters.append(c * 3)
characters = characters + commonCharacters  # 구성상 중복 없음

# 이름 기반 기본 숫자 패턴
base_digits = [
    '1', '11', '111', '1111', '2', '22', '12', '1212',
    '123', '123123', '12312', '1234', '1324', '123412',
    '1100', '1004', '23', '234', '12345', '10', '100'
]


# 순서 보존 중복 제거
def _unique(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

# 숫자 패턴 정규화
def _normalize_digits(base, extNumber):
    digits = list(base)
    if extNumber is not None:
        if isinstance(extNumber, list):
            digits.extend(str(n) for n in extNumber if n is not None)
        else:
            digits.append(str(extNumber))
    return _unique(digits)

# -c 토큰 변형(원형/대문자/첫글자 대문자)
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

# 문자(w), 숫자(d), 특수문자(c) 조합 생성
def _expand(wordlist, digits, include_plain_word):
    words = _unique(wordlist)
    digits = _unique(digits)

    # 단어 원문
    if include_plain_word:
        for w in words:
            yield w

    # (w+d), (d+w)
    for w in words:
        for d in digits:
            yield w + d
            yield d + w

    # (w+c), (c+w)
    for w in words:
        for c in characters:
            yield w + c
            yield c + w

    # 3요소 6순열: w+d+c, w+c+d, d+w+c, d+c+w, c+w+d, c+d+w
    for w in words:
        for d in digits:
            for c in characters:
                yield w + d + c
                yield w + c + d
                yield d + w + c
                yield d + c + w
                yield c + w + d
                yield c + d + w


# 에러 출력 함수
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

# 인자 핸들링
def getArgs():
    parser = argparse.ArgumentParser(
        description="password generator v0.5.3",
        epilog="[Example] genPass.py -f users.txt -o passlist.txt -c $$$,&&&",
    )
    parser.add_argument("-f", "--file", required=False, help="Input file that has usernames")
    parser.add_argument("-o", "--output", required=True, help="Output file you want to save")
    parser.add_argument("-n", "--number", type=lambda s: s.split(','), help="Use extra number", default=None)
    parser.add_argument("-c", "--char", type=lambda s: s.split(','), help="Use extra character", default=None)
    args = parser.parse_args()
    return args.file, args.output, args.number, args.char

# 옵션/입력 검증
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

# input 파일 파싱
def splitName(path):
    with open(path, 'r') as file:
        lst = [line.strip().split() for line in file.readlines()]
    return lst

# 이름 기반 기본 워드리스트 생성
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
            enFirst[0] + enMiddle[0] + enLast[0],                               # pyw
            enFirst[0].upper() + enMiddle[0].upper() + enLast[0].upper(),       # PYW
            enFirst[0].upper() + enMiddle[0] + enLast[0],                       # Pyw
            enFirst + enMiddle + enLast,                                        # parkyeonwoo
            enFirst.capitalize() + enMiddle + enLast,                           # Parkyeonwoo
            enFirst.capitalize() + enMiddle.capitalize() + enLast.capitalize(), # ParkYeonWoo
            enFirst.upper() + enMiddle + enLast,                                # PARKyeonwoo
            enFirst.upper() + enMiddle.upper() + enLast.upper(),                # PARKYEONWOO
            enFirst[0] + enMiddle + enLast,                                     # pyeonwoo
            enFirst[0].upper() + enMiddle + enLast,                             # Pyeonwoo  
            enFirst[0].upper() + enMiddle.capitalize() + enLast,                # PYeonwoo  
            enFirst[0].upper() + enMiddle.capitalize() + enLast.capitalize(),   # PYeonWoo  
            enFirst[0].upper() + enMiddle.upper() + enLast,                     # PYEONwoo
            enFirst[0].upper() + enMiddle.upper() + enLast.upper(),             # PYEONWOO
            enFirst + enMiddle[0] + enLast[0],                                  # parkyw
            enFirst.capitalize() + enMiddle[0] + enLast[0],                     # Parkyw
            enFirst + enMiddle[0].upper() + enLast,                             # parkYw
            enFirst.capitalize() + enMiddle[0].upper() + enLast[0].upper(),       # ParkYW
            enFirst.upper() + enMiddle[0] + enLast[0],                          # PARKyw
            enFirst.upper() + enMiddle.upper() + enLast.upper(),                # PARKYW
            enMiddle + enLast,                                                  # yeonwoo
            enMiddle.capitalize() + enLast,                                     # Yeonwoo
            enMiddle.capitalize() + enLast.capitalize(),                        # YeonWoo
            enMiddle.upper() + enLast,                                          # YEONwoo
            enMiddle.upper() + enLast.upper(),                                  # YEONWOO
            enMiddle[0] + enLast,                                               # ywoo
            enMiddle[0].upper() + enLast,                                       # Ywoo
            enFirst,                                                            # park
            enFirst.capitalize(),                                               # Park
            enMiddle,                                                           # yeon
            enMiddle.capitalize(),                                              # Yeon
            enLast,                                                             # woo
            enLast.capitalize(),                                                # Woo
            koFirst + koMiddle + koLast,                                        # qkrdusdn
            koFirst.capitalize() + koMiddle + koLast,                           # Qkrdusdn
            koFirst.capitalize() + koMiddle.capitalize() + koLast.capitalize(), # QkrDusDn
            koMiddle + koLast,                                                  # dusdn
            koMiddle.capitalize() + koLast,                                     # Dusdn
            koMiddle.upper() + koLast,                                          # DUSdn
            koFirst,                                                            # qkr
            koFirst.capitalize(),                                               # Qkr
            koMiddle,                                                           # dus
            koMiddle.capitalize(),                                              # Dus
            koLast,                                                             # dn
            koLast.capitalize(),                                                # Dn
        ])
    else:
        printError(3, "(input)")

    return _unique(result)

# 워드리스트 + 패턴 (이름 기반)
def addPattern(wordlist, extNumber):
    digits = _normalize_digits(base_digits, extNumber)
    return _expand(wordlist, digits, include_plain_word=True)

# 쉬운 패스워드 베이스 + 패턴
def makeEasyPasswordList(wordlist):
    digits = [
        '1', '11', '111', '1111', '2', '22', '222', '12', '1212',
        '34', '23', '234', '123', '1234', '1324', '1100', '1004', '12345', '10', '100'
    ]
    wl = wordlist if isinstance(wordlist, list) else [wordlist]
    wl = _unique(wl)
    # easy는 단독 문자열은 제외(조합만)
    return _expand(wl, digits, include_plain_word=False)

# -c 토큰 + 패턴
def makeExtCharWordlist(extChar, extNumber=None):
    digits = [
        '1', '11', '111', '1111', '2', '22', '222', '12', '1212',
        '34', '23', '234', '123', '1234', '1324', '1100', '1004', '12345', '10', '100',
        '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'
    ]
    digits = _normalize_digits(digits, extNumber)
    variants = _normalize_tokens(extChar)
    # -c도 단독 문자열은 제외(조합만)
    return _expand(variants, digits, include_plain_word=False)

# 최종 파일 중복 제거
def _dedupe_file_inplace(path):
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    unique_lines = list(OrderedDict.fromkeys(lines))
    if len(unique_lines) != len(lines):
        with open(path, 'w') as f:
            f.write("\n".join(unique_lines))
    return len(lines), len(unique_lines)

def main():
    # 인자
    input, output, extNumber, extChar = getArgs()
    # 옵션 검증
    checkOptions(input, output, extNumber, extChar)

    # 이름 파일 파싱 → 기본 워드리스트
    splitNameList = splitName(input) if input is not None else []
    wordlist = []
    for part in splitNameList:
        wordlist.extend(makePasswordList(part))
    wordlist = _unique(wordlist)

    # 쉬운 베이스
    easyCharactors = [
        'q1w2e3r4', 'qwer', 'qwe', 'qwqw', 'qwqwqw', 'qweqwe', 'qweqweqwe', 'passwd',
        'password', 'P@ssw0rd', 'asd', 'asdf', '1q2w3e4r', 'q1w2e3', '1q2w3e', 'q1w2', '1q2w'
    ]

    # 스트리밍 저장(+실시간 중복 제거)
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

        # 이름 기반 생성
        for pw in addPattern(wordlist, extNumber):
            _write_line(pw)

        # 쉬운 베이스 생성
        for pw in makeEasyPasswordList(easyCharactors):
            _write_line(pw)

        # -c 토큰 생성
        if extChar is not None:
            for pw in makeExtCharWordlist(extChar, extNumber):
                _write_line(pw)

    # 최종 dedupe
    raw_count, uniq_count = _dedupe_file_inplace(output)

    print('[*] password generator v0.5.3 - Copyright 2025 All rights reserved by mick3y')
    print('[+] Success generating user password list')
    print(f'[+] output file : {output}')

if __name__ == "__main__":
    main()

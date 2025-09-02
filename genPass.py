import argparse
import sys

# 에러 출력 함수
def printError(case, filename):
    # -f 플래그 미사용
    if case == 1:
        print("[-] This tool requires a input file; you missed the '-f' flag.")
        sys.exit(1)
    # -o 플래그 미사용
    elif case == 2:
        print("[-] This tool requires an output file; you missed the '-o' flag.")
        sys.exit(1)
    # 문자열 인자가 4개 혹은 6개가 아닌 경우
    elif case == 3:
        print(f'[-] This tool requires four or six string arguments in {filename}.')
        sys.exit(1)


# 인자 핸들링
def getArgs():
    parser = argparse.ArgumentParser(description="password generator v0.5.0",epilog="[Example] genPass.py -f users.txt -o passlist.txt -c $$$,&&&",)
    parser.add_argument("-f", "--file", required=True, help="Input file that has usernames")
    parser.add_argument("-o", "--output", required=True, help="Output file you want to save")
    parser.add_argument("-n", "--number", type=lambda s: s.split(','), help="Use extra number", default=None)
    parser.add_argument("-c", "--char", type=lambda s: s.split(','), help="Use extra character", default=None)
    args = parser.parse_args()

    input = args.file
    output = args.output
    extNumber = args.number
    extChar = args.char
    return input, output, extNumber, extChar


# 워드리스트에 숫자/특수문자 패턴 추가 (제너레이터로 변경)
def addPattern(wordlist, extNumber):

    # 숫자 패턴
    digits           = [
                    '1234',  '1324',    '123',   '12',      '11',    '1',       '2',
                    '1100',  '1004',    '1213',  '123412',  '23',    '34',      '234',
                    '10',    '100',     '12345'
                    ]
    # extNumber가 여러 개인 경우 각 원소를 순서대로 추가
    if extNumber is not None:
        if isinstance(extNumber, list):
            for n in extNumber:
                if n is not None:
                    digits.append(str(n))
        else:
            digits.append(str(extNumber))
    
    # 특수문자 패턴
    allCharacters    = [
                    '!',    '@',    '#',    '$',    '%',    '^',
                    '&',    '*',    '_',    '-',    '+',    '=',
                    '.',    '(',    ')',    ';',    ':',    '~'
                    ]
    characters       = []
    commonCharacters = ['!@#',  '!@',   '@#',   '!^',   '@#$']
    for char in allCharacters:
        characters.append(char)
        characters.append(char * 2)
        characters.append(char * 3)
    characters = characters + commonCharacters

    # 문자만
    for word in wordlist:
        yield word

    # 문자 + 숫자 조합 생성
    for word in wordlist:
        for digit in digits:
            yield word + digit

    # 숫자 + 문자 조합 생성
    for digit in digits:
        for word in wordlist:
            yield digit + word
    
    # 문자 + 특수문자 조합 생성
    for word in wordlist:
        for char in characters:
            yield word + char
    
    # 특수문자 + 문자 조합 생성
    for char in characters:
        for word in wordlist:
            yield char + word

    # 문자 + 특수문자 + 숫자 조합 생성 (w + c + d)
    for char in characters:
        for digit in digits:
            for word in wordlist:
                yield word + char + digit

    # 문자 + 숫자 + 특수문자 조합 생성 (w + d + c)
    for digit in digits:
        for char in characters:
            for word in wordlist:
                yield word + digit + char

    # 특수문자 + 숫자 + 문자 조합 생성 (c + d + w)
    for char in characters:
        for digit in digits:
            for word in wordlist:
                yield char + digit + word

    # 특수문자 + 문자 + 숫자 조합 생성 (c + w + d)
    for char in characters:
        for word in wordlist:
            for digit in digits:
                yield char + word + digit

    # 숫자 + 문자 + 특수문자 조합 생성 (d + w + c)
    for digit in digits:
        for word in wordlist:
            for char in characters:
                yield digit + word + char

    # 숫자 + 특수문자 + 문자 조합 생성 (d + c + w)
    for digit in digits:
        for char in characters:
            for word in wordlist:
                yield digit + char + word


# 사용자가 사용한 인자 검증
def checkOptions(input, output, extNumber, extChar):
    # input / output은 필수적으로 들어가야함
    if input is None:
        printError(1, input)
    if output is None:
        printError(2, input)

    # input 파일에 공백 기준 문자열이 6개 미만이면 종료
    with open(input, 'r') as file:
        userInputFile = [line.strip().split() for line in file.readlines()]
        
    for idx in range(len(userInputFile)):

        if len(userInputFile[idx]) == 4:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue
            if intCnt >= 1:
                printError(3, input)
        
        elif len(userInputFile[idx]) == 6:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue
            if intCnt >= 1:
                printError(3, input)
        else:
            printError(3, input)

# 사용자가 입력한 input 파일을 읽어 공백 기준으로 리스트로 생성
def splitName(path):
    with open(path, 'r') as file:
        list = [line.strip().split() for line in file.readlines()]
    return list


# 입력한 input 파일로부터 공백 기준으로 나눠 리스트로 관리한 것을 패스워드 게싱 리스트로 변환
def makePasswordList(list):
    result = []

    # 성 + 이름이 2글자 일 때
    if len(list) == 4:
        enFirst, enLast = list[0], list[1]
        koFirst, koLast = list[2], list[3]

        result.extend([
            enFirst + enLast, # yeonwoo
            enFirst.capitalize() + enLast, # Yeonwoo
            enFirst.capitalize() + enLast.capitalize(), # YeonWoo
            koFirst + koLast, # dusdn
            koFirst.capitalize() + koLast, # Dusdn
            koFirst.capitalize() + koLast.capitalize(), # DusDn
            enFirst, # yeon
            enFirst.capitalize(), # Yeon
            enLast, # woo
            enLast.capitalize(), # Woo
            enFirst[0] + enLast[0], # yw
            enFirst[0].upper() + enLast[0], # Yw
            enFirst[0].upper() + enLast[0].upper() # YW
        ])

    # 성 + 이름이 3글자 일 때
    elif len(list) == 6:
        enFirst, enMiddle, enLast = list[0], list[1], list[2]
        koFirst, koMiddle, koLast = list[3], list[4], list[5]

        result.extend([
            enFirst + enMiddle + enLast, # parkyeonwoo
            enFirst.capitalize() + enMiddle + enLast, # Parkyeonwoo
            enFirst.capitalize() + enMiddle.capitalize() + enLast.capitalize(), #ParkYeonWoo
            koFirst + koMiddle + koLast, # qkrdusdn
            koFirst.capitalize() + koMiddle + koLast, #Qkrdusdn
            koFirst.capitalize() + koMiddle.capitalize() + koLast.capitalize(), # QkrDusDn
            enMiddle + enLast, # yeonwoo
            enMiddle.capitalize() + enLast, # Yeonwoo
            koMiddle + koLast, # dusdn
            koMiddle.capitalize() + koLast, # Dusdn
            koMiddle.upper() + koLast, # DUSdn
            enFirst, # park
            enFirst.capitalize(), # Park
            enMiddle, # yeon
            enMiddle.capitalize(), # Yeon
            enLast, # woo
            enLast.capitalize(), # Woo
            koFirst, # qkr
            koFirst.capitalize(), # Qkr
            koMiddle, # dus
            koMiddle.capitalize(), # Dus
            koLast, # dn
            koLast.capitalize(), # Dn
            enFirst[0] + enMiddle[0] + enLast[0], # pyw
            enFirst[0].upper() + enMiddle[0].upper() + enLast[0].upper(), # PYW
            enFirst[0].upper() + enMiddle[0] + enLast[0] # Pyw
        ])
    else:
        # 원본은 스코프 밖 input을 참조해 NameError; 안전 문자열로 대체
        printError(3, "(input)")

    return result


# 사용자가 -c 옵션을 통해 추가한 문자를 리스트로 생성 (제너레이터로 변경)
def makeExtCharWordlist(extChar, extNumber=None):

    # 특수문자 패턴
    allCharacters    = [
                    '!',    '@',    '#',    '$',    '%',    '^',
                    '&',    '*',    '_',    '-',    '+',    '=',
                    '.',    '(',    ')',    ';',    ':',    '~'
                    ]
    characters       = []
    commonCharacters = ['!@#',  '!@',   '@#',   '!^',   '@#$']
    for char in allCharacters:
        characters.append(char)
        characters.append(char * 2)
        characters.append(char * 3)
    characters = characters + commonCharacters
    
    # 숫자 패턴
    digits      = [
                '1234',   '1324',     '123',      '12',       '11',
                '1',      '2',        '2015',     '2016',     '2017',
                '2018',   '2019',     '2020',     '2021',     '2022',
                '2023',   '2024',     '2025',     '23',       '234',
                '34'   
                  ]
    # extNumber가 여러 개인 경우 각 원소를 순서대로 추가
    if extNumber is not None:
        if isinstance(extNumber, list):
            for n in extNumber:
                if n is not None:
                    digits.append(str(n))
        else:
            digits.append(str(extNumber))

    if not extChar:
        return

    # extChar가 문자열이든 리스트든 모두 리스트로 통일
    tokens = extChar if isinstance(extChar, list) else [extChar]

    # 문자 + 숫자 조합 생성
    for token in tokens:
        for digit in digits:
            yield token + digit
            yield token.capitalize() + digit
            yield token.upper() + digit

    # 숫자 + 문자 조합 생성
    for digit in digits:
        for token in tokens:
            yield digit + token
            yield digit + token.capitalize()
            yield digit + token.upper()
    
    # 문자 + 특수문자 조합 생성
    for token in tokens:
        for char in characters:
            yield token + char
            yield token.capitalize() + char
            yield token.upper() + char
    
    # 특수문자 + 문자 조합 생성
    for char in characters:
        for token in tokens:
            yield char + token
            yield char + token.capitalize()
            yield char + token.upper()

    # 문자 + 숫자 + 특수문자 조합 생성
    for token in tokens:
        for digit in digits:
            for item in (token + digit, token.upper() + digit, token.capitalize() + digit):
                for char in characters:
                    yield item + char

    # 문자 + 특수문자 + 숫자 조합 생성
    for token in tokens:
        for char in characters:
            for item in (token + char, token.upper() + char, token.capitalize() + char):
                for digit in digits:
                    yield item + digit

    # 특수문자 + 문자 + 숫자 조합 생성
    for char in characters:
        for token in tokens:
            for item in (char + token, char + token.upper(), char + token.capitalize()):
                for digit in digits:
                    yield item + digit
    
    # 특수문자 + 숫자 + 문자 조합 생성
    for char in characters:
        for digit in digits:
            item = char + digit
            for token in tokens:
                yield item + token
                yield item + token.upper()
                yield item + token.capitalize()

    # 숫자 + 문자 + 특수문자 조합 생성
    for digit in digits:
        for token in tokens:
            for item in (digit + token, digit + token.upper(), digit + token.capitalize()):
                for char in characters:
                    yield item + char

    # 숫자 + 특수문자 + 문자 조합 생성
    for digit in digits:
        for char in characters:
            item = digit + char
            for token in tokens:
                yield item + token
                yield item + token.upper()
                yield item + token.capitalize()


def main():

    # 사용자가 입력한 인자 핸들링
    input, output, extNumber, extChar = getArgs()

    # 사용자가 입력한 필수 인자 누락 여부 검사
    checkOptions(input, output, extNumber, extChar)

    # 사용자가 인자로 넣은 파일에서 공백을 기준으로 리스트 생성
    splitNameList = splitName(input) 

    # 생성한 리스트를 기반으로 기본 워드리스트 양식 생성
    wordlist = []
    for part in splitNameList:
        wordlist.extend(makePasswordList(part))

    # 자주 사용되는 패스워드 목록
    easyPasswords = [
        'q1w2e3r4',     'qwer1234!',    'password123!',     'Password123!',     '1q2w3e4r', 
        'qwerty123',    '111111',       '12341234',         'qwer!@34',         'qwer12!@',
        '1q2w3e4r#',    'q1w2e3r4@',    'qwer1234@',        '1q2w3e4r!',        '1111',
        '1234',         'asdf1234',     '1q2w3e',           'q1w2e3',           '12345'       
        ]

    # 완성된 목록을 파일로 스트리밍 저장 (마지막 줄 개행 없음)
    with open(output, 'w') as file:
        first = True
        def _write_line(s):
            nonlocal first
            if first:
                file.write(s)
                first = False
            else:
                file.write("\n")
                file.write(s)

        # 워드리스트에 더할 숫자와 특수문자 추가(스트리밍)
        for pw in addPattern(wordlist, extNumber):
            _write_line(pw)

        # easyPasswords 스트리밍
        for pw in easyPasswords:
            _write_line(pw)
        
        # 사용자가 추가로 지정한 회사 이름 등의 문자열 리스트 생성(스트리밍)
        if extChar is not None:
            for pw in makeExtCharWordlist(extChar, extNumber):
                _write_line(pw)

    print(f'[*] password generator v0.5.0 - Copyright 2025 All rights reserved by mick3y')
    print(f'[+] Success generating user password list')
    print(f'[+] output file : {output}')

if __name__ == "__main__":
    main()

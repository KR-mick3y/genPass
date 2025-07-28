import argparse


# 인자 핸들링
def getArgs():
    parser = argparse.ArgumentParser(description="password generator v0.3",epilog="[Example] genPass.py -f users.txt -o passlist.txt -c $$$,&&&",)
    parser.add_argument("-f", "--file", required=True, help="Input file that has usernames", default=None)
    parser.add_argument("-o", "--output", required=True, help="Output file you want to save", default=None)
    parser.add_argument("-n", "--number", help="Use extra number", default=None)
    parser.add_argument("-c", "--char", type=lambda s: s.split(','), help="Use extra charactor", default=None)
    args = parser.parse_args()

    input = args.file
    output = args.output
    extNumber = args.number
    extChar = args.char
    return input, output, extNumber, extChar


# 워드리스트에 숫자/특수문자 패턴 추가
def addExtPattern(wordlist, extNumber):
    charactors = ['!', '@', '#', '!!', '@@', '##', '!@', '!@#', '@#', '^^', '~~', '%', '%%']
    digits = ['1234','1324','123','12','11', '1', '2', '7300']
    
    if extNumber is not None:
        digits.append(extNumber)

    charAndDigits = []
    digitsAndChar = []
    result = []

    # 특수문자 + 숫자 조합 생성
    for char in charactors:
        for digit in digits:
            charAndDigits.append(char + digit)

    # 숫자 + 특수문자 조합 생성
    for digit in digits:
        for char in charactors:
            digitsAndChar.append(digit + char)

    # 생성한 두가지 조합 리스트를 인자로 전달된 리스트와 결합
    exts = charAndDigits + digitsAndChar
    for word in wordlist:
        for ext in exts:
            result.append(word + ext)
    
    return result


# 사용자가 사용한 인자 검증
def checkOptions(input, output, extNumber, extChar):
    # input / output은 필수적으로 들어가야함
    if input is None:
        print("[-] This tool expects a username file, but you missed the '-f' flag.")
        exit()
    if output is None:
        print("[-] This tool expects making output file, but you missed the '-o' flag.")
        exit()

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
                print(f'[-] This tool requires four or six string arguments in {input}.')
                exit()
        
        elif len(userInputFile[idx]) == 6:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue
            if intCnt >= 1:
                print(f'[-] This tool requires four or six string arguments in {input}.')
                exit()
        else:
            print(f'[-] This tool requires four or six string arguments in {input}.')
            exit()

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
            enFirst, # park
            enFirst.capitalize(), # Park
            enMiddle, # yeon
            enMiddle.capitalize(), # Yeon
            enLast, # woo
            enLast.capitalize(), # Woo
            koFirst + koMiddle + koLast, # qkrdusdn
            koFirst.capitalize() + koMiddle + koLast, #Qkrdusdn
            koFirst.capitalize() + koMiddle.capitalize() + koLast.capitalize(), # QkrDusDn
            koFirst, # qkr
            koFirst.capitalize(), # Qkr
            koMiddle, # dus
            koMiddle.capitalize(), # Dus
            koLast, # dn
            koLast.capitalize(), # Dn
            enFirst[0] + enMiddle[0] + enLast[0], # pyw
            enFirst[0].upper() + enMiddle[0].upper() + enLast[0].upper() # PYW
        ])
    else:
        print('[-] It must require four or six arguments for generating')
        print(list)
        exit()

    return result


# 사용자가 추가한 문자를 리스트로 생성
def makeExtCharWordlist(extChar, extNumber=None):
    charactors = ['!', '@', '#', '!!', '@@', '##', '!@', '!@#', '@#', '^^', '~~', '%', '%%', '_']
    digits = ['1234','1324','123','12','11','1','2',
              '2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025',
              '7300']

    result = []
    addedNumber = []
    addedChar = []

    if extNumber is not None:
        digits.append(str(extNumber))  
    if not extChar:
        return result

    # extChar가 문자열이든 리스트든 모두 리스트로 통일
    tokens = extChar if isinstance(extChar, list) else [extChar]

    # 문자 + 숫자 + 특수문자 조합 생성
    for token in tokens:
        for d in digits:
            addedNumber.append(token + d)
            addedNumber.append(token.upper() + d)
            addedNumber.append(token.capitalize() + d)
    for item in addedNumber:
        for ch in charactors:
            result.append(item + ch)

    # 문자 + 특수문자 + 숫자 조합 생성
    for token in tokens:
        for ch in charactors:
            addedChar.append(token + ch)
            addedChar.append(token.upper() + ch)
            addedChar.append(token.capitalize() + ch)
    for item in addedChar:
        for d in digits:
            result.append(item + d)

    return result


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

    # 워드리스트에 더할 숫자와 특수문자 추가
    addedWordlist = addExtPattern(wordlist, extNumber)

    # 자주 사용되는 패스워드 목록
    easyPasswords = ['q1w2e3r4', 'qwer1234!', 'password123!', 'Password123!', '1q2w3e4r', 'qwerty123', '111111', '12341234', 'qwer!@34', 'qwer12!@']
    
    # 사용자가 추가로 지정한 회사 이름 등의 문자열 리스트 생성
    extCharList = makeExtCharWordlist(extChar, extNumber)
    finalWordlist = addedWordlist + easyPasswords + extCharList

    # 완성된 목록을 파일로 저장
    with open(output, 'w') as file:
        file.write("\n".join(finalWordlist))
    print(f'[*] password generator v0.3 - Copyright 2025 All rights reserved by mick3y')
    print(f'[+] Success generating username list')
    print(f'[+] output file : {output}')

if __name__ == "__main__":
    main()

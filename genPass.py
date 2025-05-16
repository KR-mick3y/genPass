import argparse

parser = argparse.ArgumentParser(description="password generator v0.2",epilog="[Example] genPass.py -f users.txt -o passlist.txt -c $$$,&&&",)
parser.add_argument("-f", "--file", required=True, help="Input file that has usernames")
parser.add_argument("-o", "--output", required=True, help="Output file you want to save")
parser.add_argument("-n", "--number", help="Use extra number", default=None)
parser.add_argument("-c", "--charactor", type=lambda s: s.split(','), help="Use extra charactor", default=None)
parser.add_argument("-e", "--easy", help="Use common easy password", action="store_true")
parser.add_argument("-i", "--initial", action="store_true", help="Use initial")
args = parser.parse_args()

userFile = args.file
outputFile = args.output
extNumber = args.number
extCharactor = args.charactor

defaultCharactorList = ['!', '@', '#', '!!', '@@', '##', '!@', '!@#', '@#', '^^']
digits = ['1234','1324','123','123412','132412','12','11']
easyPasswords = ['q1w2e3r4', 'qwer1234!', 'password123!', 'Password123!', '1q2w3e4r', 'qwerty123', '111111', '12341234']

if extNumber is not None:
    digits.append(extNumber)
if extCharactor is not None:
    for char in extCharactor:
        defaultCharactorList.append(char)

def checkOptions():
    if not args.file:
        print("[-] This tool expects a username file, but you missed the '-f' flag.")
        exit()
    if not args.output:
        print("[-] This tool expects making output file, but you missed the '-o' flag.")
        exit()

def checkArguments():
    with open(userFile, 'r') as file:
        userInputFile = [line.strip().split() for line in file.readlines()]
        
    for idx in range(len(userInputFile)):

        if len(userInputFile[idx]) == 1:
            print(f'[-] This tool requires at least two arguments in {userFile}, But there are only one argument.')
            exit()

        elif len(userInputFile[idx]) == 2:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue

            if intCnt >= 1:
                print(f'[-] This tool requires at least two string arguments in {userFile}, But there is only one string argument.')
                exit()

        elif len(userInputFile[idx]) == 3:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue

            if intCnt >= 2:
                print(f'[-] This tool requires at least two string arguments in {userFile}, But there is only one string argument.')
                exit()

        elif len(userInputFile[idx]) == 4:
            if not args.initial:
                print(f"[-] Too many arguments in {userFile}. Did you miss a flag '-i' ?")
                exit()
        else:
            print(f'[-] There is something wrong with {userFile}. Did you get a chance to read README.md ?')
            exit()


def makeList(path):
    with open(path, 'r') as file:
        list = [line.strip().split() for line in file.readlines()]
    return list


def makeUppercase(list):
    res = []
    if len(list) == 2:
        first, last = list[0], list[1]
        res.extend([
            first.capitalize() + last,
            first + last,
        ])
    elif len(list) == 3:
        if not args.initial:
            first, middle, last = list[0], list[1], list[2]
            res.extend([
                first.capitalize() + middle + last,
                middle.capitalize() + last,
                middle + last
            ])
        else:
            first, last, init = list[0], list[1], list[2]
            res.extend([
                first.capitalize() + last,
                first + last,
                first.upper() + last,
                init.upper(),
                init.lower()
            ])
    elif len(list) == 4:
        first, middle, last, init = list[0], list[1], list[2], list[3]
        res.extend([
            first.capitalize() + middle + last,
            first.upper() + middle + last,
            middle.capitalize() + last,
            middle + last,
            init.upper(),
            init.lower() 
        ])
    else:
        print('[-] It must require 2-3 arguments for generating')
        print(list)
        exit()
    return res

def addNumber(upperList):
    addedNumberList = []
    for curWord in upperList:
        for idx in range(len(digits)):
            addedNumberList.append(curWord + digits[idx])
    return addedNumberList

def addCharactor(addedNumberList):
    addedCharactorList = []
    for curWord in addedNumberList:
        for idx in range(len(defaultCharactorList)):
            addedCharactorList.append(curWord + defaultCharactorList[idx])
    return addedCharactorList

def main():
    checkOptions()
    checkArguments()
    wordList = makeList(userFile) 
    upperWordList = []
    for parts in wordList:
        upperWordList.extend(makeUppercase(parts))
    addedNumberWordList = addNumber(upperWordList)
    addedCharactorWordList = addCharactor(addedNumberWordList)
    if args.easy:
        for idx in range(len(easyPasswords)):
            addedCharactorWordList.append(easyPasswords[idx])
    with open(outputFile, 'w') as file:
        file.write("\n".join(addedCharactorWordList))

    print(f'[+] Success generating username list')
    print(f'[+] output file : {outputFile}')

if __name__ == "__main__":
    main()

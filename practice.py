import os
import json
import time
import random
formatting = {
    "reset": '\033[0m',
    "bold": '\033[01m',
    "disable": '\033[02m',
    "underline": '\033[04m',
    "reverse": '\033[07m',
    "strikethrough": '\033[09m',
    "invisible": '\033[08m',
    "fg": {
        'white':    "\033[1;37m",
        'yellow':   "\033[1;33m",
        'green':    "\033[1;32m",
        'blue':     "\033[1;34m",
        'cyan':     "\033[1;36m",
        "pink": '\033[1;95m',
        'red':      "\033[1;31m",
        'purple':  "\033[1;35m",
        'grey':  "\033[0;37m",
        'gray':  "\033[0;37m",
        "darkGrey": '\033[1;90m',
        "darkGray": '\033[1;90m',
        'darkYellow': "\033[0;33m",
        'darkGreen':  "\033[0;32m",
        'darkBlue':   "\033[0;34m",
        'darkCyan':   "\033[0;36m",
        'darkRed':    "\033[0;31m",
        'darkPurple': "\033[0;35m",
        'black':  "\033[0;30m"
    },
    "bg": {
        "black": '\033[40m',
        "red": '\033[41m',
        "green": '\033[42m',
        "yellow": '\033[43m',
        "blue": '\033[44m',
        "purple": '\033[45m',
        "cyan": '\033[46m',
        "lightGrey": '\033[47m',
        "lightGray": '\033[47m'
    }
}


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def loadJson(file):
    with open(file) as f:
        data = json.load(f)
    return data


def saveJson(data, file):
    with open(file, 'w') as f:
        json.dump(data, f)


def loadVocab():
    if not os.path.exists('vocab.json'):
        print('Vocabulary not found. Creating new one...')
        vocab = {}
        saveJson(vocab, 'vocab.json')
    else:
        vocab = loadJson('vocab.json')
    return vocab


def saveVocab(data):
    saveJson(data, 'vocab.json')


def sortVocab(reverse=False):
    global vocab
    return sorted(vocab, key=lambda k: vocab[k]['score'], reverse=False)


def getLastNWords(n):
    global vocab
    words = []
    for word in sortVocab(reverse=True):
        words.append(word)
    return words[-n:]


def shuffleList(l):
    for i in range(len(l)):
        r = random.randint(0, len(l) - 1)
        l[i], l[r] = l[r], l[i]
    return l


def printWordList(reverse=False):
    global vocab
    reset = formatting['reset']
    for word in sortVocab(reverse=reverse):
        color = formatting['fg']['blue']
        if vocab[word]['score'] < 5:
            color = formatting['fg']['red']
        elif vocab[word]['score'] < 10:
            color = formatting['fg']['yellow']
        elif vocab[word]['score'] < 20:
            color = formatting['fg']['green']
        elif vocab[word]['score'] < 30:
            color = formatting['fg']['cyan']
        print(
            f"{color}{word} = {vocab[word]['word']} ({vocab[word]['score']}){reset}")


def addWords():
    global vocab
    shouldExit = False
    while not shouldExit:
        clearScreen()
        printWordList()
        print("____________________________")
        print("Add words to your list, to stop adding words, enter '0'.")
        word = input('English:')
        if word == '0':
            shouldExit = True
        else:
            tWord = input('Thai: ')
            vocab[word] = {
                'word': tWord,
                'streak': 0,
                'lastPracticed': 0,
                'totalCorrect': 0,
                'totalWrong': 0,
                'score': 0
            }
            saveVocab(vocab)


def removeWords():
    global vocab
    shouldExit = False
    while not shouldExit:
        clearScreen()
        printWordList()
        print("____________________________")
        print("Remove words from your list, to stop removing words, enter '0'.")
        word = input('Remove Word:')
        if word == '0':
            shouldExit = True
        else:
            del vocab[word]
            saveVocab(vocab)


def practice():
    global vocab
    print("Practice!")
    while True:
        clearScreen()
        wordsToPractice = shuffleList(getLastNWords(15))
        for word in wordsToPractice:
            vWord = vocab[word]
            answers = [vWord['word']]
            answers.extend(random.sample(vocab.keys(), 3))
            answers = shuffleList(answers)
            print(
                f"{formatting['fg']['yellow']}{word} = ???{formatting['reset']}")
            for i in range(len(answers)):
                print(
                    f"{formatting['fg']['yellow']}{i + 1} = {answers[i]}{formatting['reset']}")
            answer = input('Answer: ')
            if answer == '0':
                return
            if answers[int(answer) - 1] == vWord['word']:
                vWord['streak'] += 1
                vWord['totalCorrect'] += 1
                print(
                    f"{formatting['fg']['green']}Correct!{formatting['reset']}")
            else:
                vWord['streak'] = 0
                vWord['totalWrong'] += 1
                print(f"{formatting['fg']['red']}Wrong!{formatting['reset']}")
            vWord['lastPracticed'] = time.time()
            vWord["score"] = vWord['streak'] + \
                vWord['totalCorrect'] - vWord['totalWrong']
            saveVocab(vocab)


def resetStats():
    global vocab
    for word in vocab:
        vocab[word]['streak'] = 0
        vocab[word]['totalCorrect'] = 0
        vocab[word]['totalWrong'] = 0
        vocab[word]['score'] = 0
        vocab[word]['lastPracticed'] = 0
    saveVocab(vocab)


def mainMenu():
    clearScreen()
    print("Let's burn some vocab into your brain!")
    print("1. Word list.")
    print("2. Add words.")
    print("3. Remove words.")
    print("4. Practice.")
    print("5. Reset stats.")
    print("\n")
    print("0. Exit.")
    print("\n")
    print("Please enter your choice: ", end='')
    choice = input()
    if choice == '1':
        clearScreen()
        printWordList()
        input('Press enter to continue...')
    elif choice == '2':
        addWords()
    elif choice == '3':
        removeWords()
    elif choice == '4':
        practice()
    elif choice == '5':
        resetStats()
    elif choice == '0':
        exit()
    else:
        print("Invalid choice.")
        time.sleep(2)
        mainMenu()


def main():
    global vocab
    vocab = loadVocab()
    while True:
        mainMenu()


main()

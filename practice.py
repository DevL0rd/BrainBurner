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
    sortedVoc = sorted(vocab, key=lambda k: adjustScoreBasedOnTime(
        vocab[k]), reverse=reverse)
    # for vocabWord in sortedVoc:
    #     hoursPassed =
    #     # Reduce the score based on hours pased
    #     vocab[vocabWord]['score'] -= (hoursPassed * 0.3)
    #     vocab[vocabWord]['score'] = int(vocab[vocabWord]['score'])
    return sortedVoc


def adjustScoreBasedOnTime(vWord):
    return vWord['score'] - \
        int(((time.time() - vWord['lastPracticed']) / 3600) * 0.3)


def getPracticeWords(num=15):
    global vocab
    sortedVocab = sortVocab(reverse=True)
    wordsToPractice = []
    i = 0
    while len(wordsToPractice) < num:
        word = sortedVocab[i]
        adjustedScore = adjustScoreBasedOnTime(vocab[word])
        if adjustedScore > 0 and adjustedScore < 30:
            wordsToPractice.append(word)
        else:
            ammountLeft = num - len(wordsToPractice)
            wordsToPractice.extend(sortedVocab[-ammountLeft:])
        i += 1
    return shuffleList(wordsToPractice)


def shuffleList(l):
    for i in range(len(l)):
        r = random.randint(0, len(l) - 1)
        l[i], l[r] = l[r], l[i]
    return l


def centerText(text):
    length = len(text)
    spaceCount = int((42 - length) / 2)
    spacing = ' ' * spaceCount
    text = spacing + text + spacing
    if (length % 2) != 0:
        text += ' '
    return text


def getScoredColor(vocabWord):
    color = formatting['fg']['blue']
    adjustedScore = adjustScoreBasedOnTime(vocabWord)
    if adjustedScore < 1:
        color = formatting['fg']['gray']
    elif adjustedScore < 5:
        color = formatting['fg']['red']
    elif adjustedScore < 10:
        color = formatting['fg']['yellow']
    elif adjustedScore < 20:
        color = formatting['fg']['green']
    elif adjustedScore < 30:
        color = formatting['fg']['cyan']
    return color


def printWordList(reverse=False):
    global vocab
    reset = formatting['reset']
    print("********************************************")
    for word in sortVocab(reverse=reverse):
        text = centerText(f"{word} = {vocab[word]['word']}")
        color = getScoredColor(vocab[word])
        print(f"|{color}{text}{reset}|")


def addWords():
    global vocab
    shouldExit = False
    while not shouldExit:
        clearScreen()
        printWordList()
        print("|------------------------------------------|")
        print("|          Add words to the list.          |")
        print("|------------------------------------------|")
        print("|                 0. Exit.                 |")
        print("********************************************")
        word = input(': ')
        if word == '0':
            shouldExit = True
        else:
            tWord = input(f'{word} = ')
            vocab[word] = {
                'word': tWord,
                'streak': 0,
                'lastPracticed': 0,
                'score': 0
            }
            saveVocab(vocab)


def removeWords():
    global vocab
    shouldExit = False
    while not shouldExit:
        clearScreen()
        printWordList()
        print("|------------------------------------------|")
        print("|       Remove words from the list.        |")
        print("|------------------------------------------|")
        print("|                 0. Exit.                 |")
        print("********************************************")
        word = input(': ')
        if word == '0':
            shouldExit = True
        else:
            del vocab[word]
            saveVocab(vocab)


def practice():
    global vocab
    tWords = []
    for word in vocab:
        tWords.append(vocab[word]["word"])
    while True:
        wordsToPractice = getPracticeWords(15)
        for word in wordsToPractice:
            clearScreen()
            vWord = vocab[word]
            print("********************************************")
            print("|              Practice Mode.              |")
            print("|------------------------------------------|")
            game = random.choice(["multiple choice", "true/false"])
            if game == "true/false":
                print("| 1. True                         2. False |")
                print("|                                          |")

            print("|                 0. Exit.                 |")
            print("|------------------------------------------|")
            print("|                                          |")
            centeredWord = centerText(word)
            color = getScoredColor(vocab[word])
            print(
                f"|{formatting['bold']}{color}{centeredWord}{formatting['reset']}|")
            print("|                                          |")
            print("********************************************")
            adjustedScore = adjustScoreBasedOnTime(vocab[word])
            if adjustedScore >= 5:
                poop = input()
                if poop == '0':
                    return
            else:
                print("")
            print("********************************************")
            tf_correctChoice = "1"
            if game == "multiple choice":
                answers = [vWord['word']]
                answers.extend(random.sample(tWords, 3))
                answers = shuffleList(answers)
                for i in range(len(answers)):
                    centeredAnswer = centerText(f"{i + 1} = {answers[i]}")
                    print(
                        f"|{formatting['fg']['white']}{formatting['bold']}{centeredAnswer}{formatting['reset']}|")
            elif game == "true/false":
                tf_correctChoice = random.choice(["1", "2"])
                centeredAnswer = ""
                if tf_correctChoice == "1":
                    centeredAnswer = centerText(f"{word} = {vWord['word']}")
                else:
                    while True:
                        tWord = random.choice(tWords)
                        if tWord != vWord['word']:
                            centeredAnswer = centerText(
                                f"{word} = {tWord}")
                            break
                print(
                    f"|{formatting['fg']['white']}{formatting['bold']}{centeredAnswer}{formatting['reset']}|")

            print("********************************************")
            answer = input(': ')
            if answer == '0':
                return

            isGoodAnswer = False
            if game == "multiple choice":
                isGoodAnswer = answer and answers[int(
                    answer) - 1] == vWord['word']
            elif game == "true/false":
                isGoodAnswer = answer == tf_correctChoice

            if isGoodAnswer:
                vWord['streak'] += 1
                vWord['score'] += 1
            else:
                vWord['streak'] = 0
                vWord['score'] *= 0.7
                vWord['score'] = int(vWord['score'])
                print(f"{formatting['fg']['red']}Wrong!{formatting['reset']}")
                print(f"{formatting['fg']['red']}The word for {formatting['fg']['white']}{formatting['bold']}'{word}'{formatting['reset']}{formatting['fg']['red']} is {formatting['fg']['white']}{formatting['bold']}'{vWord['word']}'{formatting['fg']['red']}.{formatting['reset']}")
                input()
            vWord['lastPracticed'] = time.time()
            saveVocab(vocab)


def resetStats():
    global vocab
    for word in vocab:
        vocab[word]['streak'] = 0
        vocab[word]['score'] = 0
        vocab[word]['lastPracticed'] = 0
    saveVocab(vocab)


def mainMenu():
    clearScreen()
    printWordList()
    print("|------------------------------------------|")
    print("|  Let's burn some vocab into your brain!  |")
    print("|------------------------------------------|")
    print("| 1. Add words.            3. Practice.    |")
    print("| 2. Remove words.         4. Reset stats. |")
    print("|                                          |")
    print("|                 0. Exit.                 |")
    print("********************************************")
    choice = input(":")
    if choice == '1':
        addWords()
    elif choice == '2':
        removeWords()
    elif choice == '3':
        practice()
    elif choice == '4':
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

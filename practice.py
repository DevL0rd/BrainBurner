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


def loadJson(file):
    with open(file) as f:
        data = json.load(f)
    return data


def saveJson(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def loadVocab():
    global vocab
    if not os.path.exists('vocab.json'):
        print('Vocabulary not found. Creating new one...')
        vocab = {}
        saveJson(vocab, 'vocab.json')
    else:
        vocab = loadJson('vocab.json')
    saveVocab()


def saveVocab():
    global vocab
    saveJson(vocab, 'vocab.json')


def loadSettings():
    global settings
    settingsVersion = 2
    if not os.path.exists('settings.json'):
        print('Settings not found. Creating new one...')
        settings = {
            "settingVersion": settingsVersion,
            "timeDecayRatio": 0.3,
            "screenWidth": 65,
            "numPracticeWords": 8,
            "maxScore": 20,
            "practiceMode": "random",
            "bgColor": "black",
            "fgColor": "white",
            "highlightColorFG": "blue",
            "highlightColorBG": "lightGray",
            "borderColor": "blue",
            "seperatorColor": "darkBlue",
            "showScore": True,
            "showTranslations": True,
        }
        # saveSettings()
    else:
        settings = loadJson('settings.json')
        if 'settingVersion' not in settings or settings['settingVersion'] != settingsVersion:
            os.remove('settings.json')
            loadSettings()


def saveSettings():
    global settings
    saveJson(settings, 'settings.json')


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def printBorder():
    global settings
    text = "#" * settings["screenWidth"]
    text = formatting['fg'][settings['borderColor']] + \
        formatting['bg'][settings['bgColor']] + text + formatting['reset']
    print(text)


def printLineSeperator():
    global settings
    text = '-' * (settings["screenWidth"] - 2)
    text = formatting['fg'][settings['borderColor']] + formatting['bg'][settings['bgColor']] + "|" + formatting['fg'][settings['seperatorColor']
                                                                                                                      ] + formatting['bg'][settings['bgColor']] + text + formatting['fg'][settings['borderColor']] + "|" + formatting['reset']
    print(text)


def printSpaceSeperator():
    global settings
    text = ' ' * (settings["screenWidth"] - 2)
    text = formatting['fg'][settings['borderColor']] + \
        formatting['bg'][settings['bgColor']] + \
        "|" + text + "|" + formatting['reset']
    print(text)


# Removes formmating strings and returns length
def measureTextLength(text):
    textCopy = text[:]
    for key in formatting:
        if type(formatting[key]) == str:
            textCopy = textCopy.replace(formatting[key], '')
        elif type(formatting[key]) == dict:
            for k in formatting[key]:
                textCopy = textCopy.replace(formatting[key][k], '')
    return len(textCopy)


def printCentered(text):
    global settings
    length = measureTextLength(text)
    spaceCount = int((settings["screenWidth"] - length - 2) / 2)
    spacing = " " * spaceCount
    text = formatting['fg'][settings['borderColor']] + formatting['bg'][settings['bgColor']] + "|" + formatting['fg'][settings['fgColor']] + formatting['bg'][settings['bgColor']
                                                                                                                                                              ] + spacing + text + formatting['reset'] + formatting["bg"][settings["bgColor"]] + spacing
    if measureTextLength(text) != settings["screenWidth"] - 1:
        text += ' '
    text = text + formatting['fg'][settings['borderColor']] + \
        formatting['bg'][settings['bgColor']] + "|" + formatting['reset']
    print(text)


def printCol_2(col1, col2):
    global settings
    length = measureTextLength(col1) + measureTextLength(col2)
    spaceCount = (settings["screenWidth"] - length - 4)
    spacing = " " * spaceCount
    text = formatting['fg'][settings['borderColor']] + formatting['bg'][settings['bgColor']] + "| " + formatting['fg'][settings['fgColor']] + formatting['bg'][settings['bgColor']] + col1 + formatting['fg'][settings['fgColor']] + formatting['bg'][settings['bgColor']
                                                                                                                                                                                                                                                      ] + spacing + formatting['fg'][settings['fgColor']] + formatting['bg'][settings['bgColor']] + col2 + formatting['reset'] + formatting['fg'][settings['borderColor']] + formatting['bg'][settings['bgColor']] + " |" + formatting['reset']
    print(text)


def printLeft(text):
    printCol_2(text, "")


def printRight(text):
    printCol_2("", text)


def printWordList(showTranslations=True, selectLine=-1, reverse=False):
    global vocab
    global settings
    printBorder()
    i = 0
    for word in sortVocab(reverse=reverse):
        fg = formatting['fg'][settings['fgColor']]
        bg = formatting['bg'][settings['bgColor']]
        color = getScoredColor(vocab[word]) + bg
        if selectLine == i:
            fg = formatting['fg'][settings['highlightColorFG']]
            bg = formatting['bg'][settings['highlightColorBG']]
            color = fg + bg

        text = f"{color}{word}"
        if showTranslations:
            text = f"{text} = {vocab[word]['word']}"
        if settings['showScore']:
            adjustedScore = adjustScoreBasedOnTime(vocab[word])
            text = f"{text}{formatting['reset']}{fg}{bg} ({adjustedScore})"
        printCentered(text)
        i += 1


def adjustScoreBasedOnTime(vWord):
    global settings
    nScore = vWord['score'] - \
        int((((time.time() - vWord['lastPracticed']) /
            3600) / 2) * settings["timeDecayRatio"])
    if nScore < 0:
        nScore = 0
    return nScore


def getScoredColor(vocabWord):
    global settings
    color = formatting['fg']['blue']
    adjustedScore = adjustScoreBasedOnTime(vocabWord)
    sectionLength = int(settings["maxScore"] / 4)
    if adjustedScore < 1:
        color = formatting['fg']['gray']
    elif adjustedScore < sectionLength:
        color = formatting['fg']['red']
    elif adjustedScore < sectionLength * 2:
        color = formatting['fg']['yellow']
    elif adjustedScore < sectionLength * 3:
        color = formatting['fg']['green']
    elif adjustedScore < sectionLength * 4:
        color = formatting['fg']['cyan']
    return color


def sortVocab(reverse=False):
    global vocab
    return sorted(vocab, key=lambda k: adjustScoreBasedOnTime(vocab[k]), reverse=reverse)


def shuffleList(l):
    for i in range(len(l)):
        r = random.randint(0, len(l) - 1)
        l[i], l[r] = l[r], l[i]
    return l


def getPracticeWords(num=15):
    global vocab
    global settings
    sortedVocab = sortVocab(reverse=True)
    wordsToPractice = []
    i = 0
    while len(wordsToPractice) < num:
        word = sortedVocab[i]
        adjustedScore = adjustScoreBasedOnTime(vocab[word])
        if adjustedScore > 0 and adjustedScore < settings["maxScore"]:
            wordsToPractice.append(word)
        else:
            ammountLeft = num - len(wordsToPractice)
            wordsToPractice.extend(sortedVocab[-ammountLeft:])
        i += 1
    return shuffleList(wordsToPractice)


def addWords():
    global vocab
    while True:
        clearScreen()
        printWordList()
        printLineSeperator()
        printCentered("Add words to the list.")
        printLineSeperator()
        printCentered("0. Exit.")
        printBorder()
        word = input(': ')
        if word == '0':
            return
        else:
            tWord = input(f'{word} = ')
            if tWord == '0':
                continue
            vocab[word] = {
                'word': tWord,
                'streak': 0,
                'lastPracticed': time.time(),
                'score': 0,
                'isFavorite': False
            }
            saveVocab()


def editWords():
    global vocab
    selectLine = 0
    sortedVocab = sortVocab()
    while True:
        clearScreen()
        printWordList(selectLine=selectLine)
        printLineSeperator()
        printCentered("Edit word list.")
        printLineSeperator()
        printCentered("Press enter to select a word.")
        printSpaceSeperator()
        printCol_2("1. Edit word", "2. Edit translation")
        printCol_2("3. Remove word", "")
        printSpaceSeperator()
        printCentered("0. Exit")
        printBorder()
        opt = input(': ')
        if opt == '0':
            return
        elif opt == '1':
            newWord = input(f'{sortedVocab[selectLine]} > ')
            if newWord == '0':
                continue
            vocab[newWord] = vocab[sortedVocab[selectLine]]
            del vocab[sortedVocab[selectLine]]
            saveVocab()
            sortedVocab = sortVocab()
        elif opt == '2':
            newTranslation = input(f'{sortedVocab[selectLine]} = ')
            if newTranslation == '0':
                continue
            vocab[sortedVocab[selectLine]]['word'] = newTranslation
            saveVocab()
            sortedVocab = sortVocab()
        elif opt == '3':
            del vocab[sortedVocab[selectLine]]
            saveVocab()
            sortedVocab = sortVocab()
            selectLine -= 1
        else:
            selectLine += 1

        if selectLine < 0 or selectLine > len(sortedVocab) - 1:
            selectLine = 0


def practice():
    global vocab
    global settings
    tWords = [vocab[word]["word"] for word in vocab]
    while True:
        wordsToPractice = getPracticeWords(settings["numPracticeWords"])
        for word in wordsToPractice:
            clearScreen()
            vWord = vocab[word]
            adjustedScore = adjustScoreBasedOnTime(vocab[word])
            printBorder()
            if settings["practiceMode"] == "random":
                game = random.choice(
                    ["multiple choice", "multiple choice", "true/false"])  # Bigger chance for multiple choice
            else:
                game = settings["practiceMode"]
            if game == "multiple choice":
                printCentered("Multiple Choice")
                printLineSeperator()
            elif game == "true/false":
                printCentered("True/False")
                printLineSeperator()
                printCol_2("1. True", "2. False")
                printSpaceSeperator()
            printCentered("0. Exit.")
            printLineSeperator()
            printSpaceSeperator()
            color = getScoredColor(vocab[word]) + \
                formatting['bg'][settings['bgColor']]
            if settings['showScore']:
                printCentered(
                    f"{formatting['bold']}{color}{word} {formatting['reset']}{formatting['fg'][settings['fgColor']]}{formatting['bg'][settings['bgColor']]}({adjustedScore})")
            else:
                printCentered(
                    f"{formatting['bold']}{color}{word}")
            printSpaceSeperator()
            printBorder()

            # Wait for input if the word is not new, so we don't give hints.
            if adjustedScore >= int(settings["maxScore"] / 4):
                poop = input()
                if poop == '0':
                    return
            else:
                print("")

            printBorder()
            tf_correctChoice = "1"
            if game == "multiple choice":
                answers = [vWord['word']]
                answers.extend(random.sample(tWords, 3))
                answers = shuffleList(answers)
                for i in range(len(answers)):
                    printCentered(
                        f"{formatting['bold']}{i + 1}. {answers[i]}")
            elif game == "true/false":
                tf_correctChoice = random.choice(["1", "2"])
                text = ""
                if tf_correctChoice == "1":
                    text = f"{word} = {vWord['word']}"
                else:
                    while True:
                        tWord = random.choice(tWords)
                        if tWord != vWord['word']:
                            text = f"{word} = {tWord}"
                            break
                printCentered(
                    f"{formatting['bold']}{text}")

            printBorder()
            answer = input(': ')
            if answer == '0':
                return

            isGoodAnswer = False
            if game == "multiple choice":
                isGoodAnswer = answer and answers[int(
                    answer) - 1] == vWord['word']
            elif game == "true/false":
                isGoodAnswer = answer == tf_correctChoice
                if isGoodAnswer and tf_correctChoice == "2":
                    clearScreen()
                    printBorder()
                    printCentered(
                        f"{formatting['fg']['green']}Correct!")
                    printCentered(f"The real word for {formatting['fg']['white']}{formatting['bg'][settings['bgColor']]}{formatting['bold']}'{word}'{formatting['reset']}{formatting['fg'][settings['fgColor']]}{formatting['bg'][settings['bgColor']]} is {formatting['fg']['white']}{formatting['bg'][settings['bgColor']]}{formatting['bold']}'{vWord['word']}'{formatting['reset']}{formatting['fg'][settings['fgColor']]}{formatting['bg'][settings['bgColor']]}.")
                    printBorder()
                    input()

            if isGoodAnswer:
                vWord['streak'] += 1
                vWord['score'] += 1
            else:
                vWord['streak'] = 0
                vWord['score'] *= 0.7
                vWord['score'] = int(vWord['score'])
                clearScreen()
                printBorder()
                printCentered(
                    f"{formatting['fg']['red']}Wrong!{formatting['reset']}")
                printCentered(f"{formatting['fg']['red']}The word for {formatting['fg']['white']}{formatting['bold']}'{word}'{formatting['reset']}{formatting['fg']['red']}{formatting['bg'][settings['bgColor']]} is {formatting['fg']['white']}{formatting['bold']}'{vWord['word']}'{formatting['fg']['red']}.")
                printBorder()
                input()
            vWord["score"] = adjustScoreBasedOnTime(vWord)
            vWord['lastPracticed'] = time.time()
            saveVocab()


def resetStats():
    global vocab
    for word in vocab:
        vocab[word]['streak'] = 0
        vocab[word]['score'] = 0
        vocab[word]['lastPracticed'] = time.time()
    saveVocab()


def load():
    loadSettings()
    loadVocab()


def settignsMenu():
    global settings
    while True:
        clearScreen()
        printBorder()
        printCentered("Settings")
        printLineSeperator()
        printCentered(f"1. Practice Mode ({settings['practiceMode']})")
        printCentered(f"2. Practice Count ({settings['numPracticeWords']})")
        printCentered(f"3. Max Score ({settings['maxScore']})")
        printCentered(f"4. Show Score ({settings['showScore']})")
        printCentered(f"5. Time Decay ({settings['timeDecayRatio']})")
        printCentered(f"6. Reset Stats")
        printCentered(f"7. BG Color ({settings['bgColor']})")
        printCentered(f"8. FG Color ({settings['fgColor']})")
        printCentered(f"9. Border Color ({settings['borderColor']})")
        printCentered(f"10. Seperator Color ({settings['seperatorColor']})")
        printCentered(f"11. Screen Width ({settings['screenWidth']})")
        printCentered("0. Exit")
        printBorder()
        choice = input(': ')
        if choice == '0':
            return
        elif choice == '1':
            clearScreen()
            printBorder()
            printCentered(f"Practice Mode : {settings['practiceMode']}")
            printLineSeperator()
            printCol_2("1. Random", "3. True/False")
            printCol_2("2. Multiple Choice", "0. Exit")
            printBorder()
            choice = input(': ')
            if choice == '0':
                continue
            elif choice == '1':
                settings["practiceMode"] = "random"
            elif choice == '2':
                settings["practiceMode"] = "multiple choice"
            elif choice == '3':
                settings["practiceMode"] = "true/false"
        elif choice == '2':
            clearScreen()
            printBorder()
            printCentered(f"Practice Count: {settings['numPracticeWords']}")
            printLineSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            try:
                if choice == '0':
                    continue
                settings["numPracticeWords"] = int(choice)
                saveSettings()
            except Exception:
                continue
        elif choice == '3':
            clearScreen()
            printBorder()
            printCentered(f"Max Score: {settings['maxScore']}")
            printLineSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            try:
                if choice == '0':
                    continue
                settings["maxScore"] = int(choice)
                saveSettings()
            except Exception:
                continue
        elif choice == '4':
            clearScreen()
            printBorder()
            printCentered(f"Show Score: {settings['showScore']}")
            printLineSeperator()
            printCol_2("1. On", "2. Off")
            printSpaceSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            if choice == '0':
                continue
            elif choice == '1':
                settings["showScore"] = True
            elif choice == '2':
                settings["showScore"] = False
            saveSettings()
        elif choice == '5':
            clearScreen()
            printBorder()
            printCentered(f"Time Decay: {settings['timeDecayRatio']}")
            printLineSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            try:
                if choice == '0':
                    continue
                settings["timeDecayRatio"] = float(choice)
                if settings["timeDecayRatio"] < 0:
                    settings["timeDecayRatio"] = 0
                if settings["timeDecayRatio"] > 1:
                    settings["timeDecayRatio"] = 1
                saveSettings()
            except Exception:
                continue
        elif choice == '6':
            resetStats()
            clearScreen()
            printBorder()
            printCentered("Stats Reset!")
            printBorder()
            input()
        elif choice == '7':
            clearScreen()
            printBorder()
            printCentered(
                f"BG Color: {formatting['fg'][settings['bgColor']]}{settings['bgColor']}")
            printLineSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            if choice == '0':
                continue
            elif choice in formatting['bg']:
                settings["bgColor"] = choice
            saveSettings()
        elif choice == '8':
            clearScreen()
            printBorder()
            printCentered(
                f"FG Color: {formatting['fg'][settings['fgColor']]}{settings['fgColor']}")
            printLineSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            if choice == '0':
                continue
            elif choice in formatting['fg']:
                settings["fgColor"] = choice
            saveSettings()
        elif choice == '9':
            clearScreen()
            printBorder()
            printCentered(
                f"Border Color: {formatting['fg'][settings['borderColor']]}{settings['borderColor']}")
            printLineSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            if choice == '0':
                continue
            elif choice in formatting['fg']:
                settings["borderColor"] = choice
            saveSettings()
        elif choice == '10':
            clearScreen()
            printBorder()
            printCentered(
                f"Seperator Color: {formatting['fg'][settings['seperatorColor']]}{settings['seperatorColor']}")
            printLineSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            if choice == '0':
                continue
            elif choice in formatting['fg']:
                settings["seperatorColor"] = choice
            saveSettings()
        elif choice == '11':
            clearScreen()
            printBorder()
            printCentered(
                f"Screen Width: {settings['screenWidth']}")
            printLineSeperator()
            printCentered("0. Exit")
            printBorder()
            choice = input(': ')
            try:
                if choice == '0':
                    continue
                settings["screenWidth"] = int(choice)
                saveSettings()
            except Exception:
                continue


def main():
    load()
    while True:
        clearScreen()
        printWordList(showTranslations=settings['showTranslations'])
        printLineSeperator()
        printCentered("Let's burn some vocab into your brain!")
        printLineSeperator()
        printCol_2("1. Add words", "2. Edit List")
        printCol_2("3. Practice", "4. Toggle Translation")
        printCol_2("5. Settings", "0. Reset Stats")
        printSpaceSeperator()
        printCentered("0. Exit.")
        printBorder()
        choice = input(":")
        if choice == '1':
            addWords()
        elif choice == '2':
            editWords()
        elif choice == '3':
            practice()
        elif choice == '4':
            settings["showTranslations"] = not settings["showTranslations"]
            saveSettings()
        elif choice == '5':
            settignsMenu()
        elif choice == '0':
            exit()
        else:
            print("Invalid choice.")


main()

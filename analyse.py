from random_username.generate import generate_username
from nltk.tokenize import word_tokenize, sent_tokenize
import re


# Welcome the User
def welcomeUser():
    print(
        "\nWelcome to the text analysis tool, i will mine and analyse a body of text, from a file you give me"
    )


# Get Username
def getUsername():

    maxAttempts = 3
    attempts = 0
    while attempts < maxAttempts:
        # Print message prompting user to input their namef
        inputPrompt = ""
        if attempts ==0:
            inputPrompt = "\nTo begin, please enter your username: \n"
        else:
            inputPrompt = "\n Please try again: \n"
        
        usernameFromInput = input(inputPrompt)

        if len(usernameFromInput) < 5 or not usernameFromInput.isidentifier():
            print(
                "Your username must be at least 5 characters long, alphanumeric only (a-z/A-Z/0-9), have no spaces, and cannot start with a number "
            )
        else:
            return usernameFromInput
        attempts += 1
    print("Exhausted all " + str(maxAttempts) + " attempts\nAssigning Username Instead...")
    return generate_username()[0]


# Greet the user
def greetUser(name):
    print("Hello, " + name)

# Get text from file
def getArticleText():
    f = open("files/article.txt", "r")
    rawText = f.read()
    f.close()
    return rawText.replace("\n", " ").replace("\r", "")

# Extract Sentences from raw Text body
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)

# Extract Words from list of Sentences
def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words

#Get the key sentences based on keyword search pattern
def extractKeySentences(sentences):
    matchedSentences = []
    for sentence in sentences:
        # if sentence matches desired pattern, add to matchedSentences
        if re.search(stockSearchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

# Get User Details
welcomeUser()
username = getUsername()
greetUser(username)

# Extract and tokenize Text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)


# Get Analytics
stockSearchPattern = "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
keySentences = extractKeySentences(articleSentences)
# print for testing
print("GOT:")
print(articleSentences)

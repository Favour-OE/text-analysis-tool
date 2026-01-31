import base64
from io import BytesIO
import nltk
import re
import json
from random_username.generate import generate_username
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("wordnet")

stopWords = set(stopwords.words("english"))
wordLemmatizer = WordNetLemmatizer()
sentimentAnalyzer = SentimentIntensityAnalyzer()


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
        if attempts == 0:
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
    print(
        "Exhausted all " + str(maxAttempts) + " attempts\nAssigning Username Instead..."
    )
    return generate_username()[0]


# Greet the user
def greetUser(name):
    return "Hello, " + name


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


# Get the key sentences based on keyword search pattern
def extractKeySentences(sentences):
    matchedSentences = []
    for sentence in sentences:
        # if sentence matches desired pattern, add to matchedSentences
        stockSearchPattern = (
            "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
        )
        if re.search(stockSearchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences


# get the average word per sentence excluding punctuation
def getWordsPerSentence(sentences):
    totalWords = 0
    for sentence in sentences:
        totalWords += len(sentence.split(" "))
    return totalWords / len(sentences)


# Convert pat of speeck from pos_tag()function into wordnet compatible pos tag
posToWordnetag = {
    "J": wordnet.ADJ,
    "V": wordnet.VERB,
    "N": wordnet.NOUN,
    "R": wordnet.ADV,
}


def treebankPosToWordnetPos(partOfSpeech):
    posFirstChar = partOfSpeech[0]
    if posFirstChar in posToWordnetag:
        return posToWordnetag[posFirstChar]
    return wordnet.NOUN


# Convert raw list of (word, POS) tuple to a list of strings
# that only include valid english words
def cleanseWordList(posTaggedWordTuples):
    cleansedWords = []
    invalidWordPattern = "[^a-zA-Z-+]"

    for posTaggedWordTuple in posTaggedWordTuples:
        word = posTaggedWordTuple[0]
        pos = posTaggedWordTuple[1]
        cleansedWord = word.replace(".", "").lower()
        if (
            (not re.search(invalidWordPattern, cleansedWord))
            and len(cleansedWord) > 1
            and cleansedWord not in stopWords
        ):
            cleansedWords.append(
                wordLemmatizer.lemmatize(cleansedWord, treebankPosToWordnetPos(pos))
            )
    return cleansedWords


def getUserInfo():
    # Get User Details
    welcomeUser()
    username = getUsername()
    greetUser(username)


# Extract and tokenize Text
articleTextRaw = getArticleText()


def analyzeText(textToAnalyze):
    articleSentences = tokenizeSentences(textToAnalyze)
    articleWords = tokenizeWords(articleSentences)

    # Get sentence Analytics
    stockSearchPattern = "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
    keySentences = extractKeySentences(articleSentences)
    wordsPerSentence = getWordsPerSentence(articleSentences)

    # Get word analytics
    wordsPosTagged = nltk.pos_tag(articleWords)
    articleWordsCleansed = cleanseWordList(wordsPosTagged)

    # Generate word cloud
    seperator = " "
    wordCloudFilePath = "results/wordcloud.png"
    wordcloud = WordCloud(
        width=500,
        height=350,
        background_color="white",
        colormap="Set2",
        collocations=False,
    ).generate(seperator.join(articleWordsCleansed))
    # wordcloud.to_file(wordCloudFilePath)

    imgIO = BytesIO()
    wordcloud.to_image().save(imgIO, format="PNG")
    imgIO.seek(0)

    # Encode the image as base64
    encodedWordcloud = (
        base64.b64encode(imgIO.getvalue()).decode("utf-8") if imgIO.getvalue() else ""
    )
    

    # Run Sentiment Analysis
    sentimentResult = sentimentAnalyzer.polarity_scores(textToAnalyze)

    # Collate analyses into one  dictionary
    finalResult = {
        # "username": username,
        "data": {
            "keySentences": keySentences,
            "wordsPerSentence": round(wordsPerSentence, 1),
            "sentiment": sentimentResult,
            "wordCloudFilePath": wordCloudFilePath,
            "wordCloudImage": encodedWordcloud,
        },
        "metadata": {
            "sentencesAnalyzed": len(articleSentences),
            "wordsAnalyzed": len(articleWordsCleansed),
        },
    }
    return finalResult
from random_username.generate import generate_username


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


welcomeUser()
username = getUsername()
greetUser(username)

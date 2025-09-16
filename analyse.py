#Welcome the User
def welcomeUser():
    print(
        "\nWelcome to the text analysis tool, i will mine and analyse a body of text, from a file you give me"
    )


# Get Username
def getUsername():
    # Print message prompting user to input their name
    usernameFromInput = input("\nTo begin, please enter your username: \n")
    return usernameFromInput

# Greet the user
def greetUser(name, instruction):
    print("Hello, " + name.upper())


welcomeUser()
username = getUsername()
greetUser(username )



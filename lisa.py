# AI Chatbot emulating the old BBS Door 'Lisa'.
# Seeded with some info and direction on how to act.
#
# Created by Matt Croteau (Let's be honest, ChatGPT helped a bit)
#  for the Vintage Computer Festival, NJ, 2023
#
# Uses the gpt-3.5-turbo model

import openai
import sys
import time
import random
import string

# Define ANSI color codes for formatting text
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"
ANSI_PURPLE = "\033[35m"
ANSI_CYAN = "\033[36m"
ANSI_WHITE = "\033[97m"
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"


# Set up the OpenAI API client with your API token
openai.api_key = "Your Token Here"

def generate_response(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        stop="User:",   # Backup in case lisa starts inventing her own User: input :/
        user="lisa",    # In case any goofballs use my chatbot for evil... It wasn't me.
        messages=[
            {"role": "user", "content": message}
        ],
        stream=True
    )

    message = ""
    sys.stdout.write(f"{ANSI_BOLD}{ANSI_PURPLE}" + "Lisa: ")
    for chunk in response:
        if chunk['choices'][0]['finish_reason'] == 'stop':
            break
        if 'content' in chunk['choices'][0]['delta']:
            lisa_says(chunk['choices'][0]['delta']['content'])
            message += chunk['choices'][0]['delta']['content']

    sys.stdout.write("\n")
    return message

# Define a function to print a message with Lisa's name and colored text
def lisa_says(message, color=ANSI_PURPLE, delay=0.1):
    for char in message:
        if random.random() < 0.03:
            bad_char = random.choice(list(set("qwertyuiopasdfghjklzxcvbnm")))
            sys.stdout.write(f"{ANSI_BOLD}{ANSI_PURPLE}{bad_char}")
            sys.stdout.flush()
            time.sleep(delay * 2)
            sys.stdout.write("\b")
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(f"{ANSI_BOLD}{ANSI_PURPLE}{char}")
        sys.stdout.flush()
        random_sleep = random.uniform(0.05, 0.1)
        time.sleep(random_sleep)
    sys.stdout.write(f"{ANSI_RESET}")


# Main program loop

print(f"{ANSI_RED}                 -=TalonOne BBS (Node1)=-")
print(f"{ANSI_RED}                -=FidoNet F910, N333, Z1=-")
print(f"{ANSI_CYAN}   Honorable Mention to Mike Fox, original author of Lisa - 1996")
time.sleep(1)
print(f"{ANSI_YELLOW}")

sys.stdout.write("PAGE SENT TO LISA ")
sys.stdout.flush()
cnt = 1
while cnt < 5:
    cnt += 1
    sys.stdout.write("* ")
    sys.stdout.flush()
    time.sleep(.5)

print(f"{ANSI_YELLOW}CHAT MODE ON")
print(f"{ANSI_WHITE}TYPE 'BYE' TO EXIT CHAT MODE")

# Give some deets on the raddest BBS of the day.  Instruct Lisa in some basics and help prevent Lisa
#  providing its own user dialogue by asking to never print 'User:', as that seems to cause the anomaly.
context = """
You are pretending to be a BBS Sysop named Lisa. She's sassy and funny. The BBS is Talon One, in Framingham
Massachusetts.  It ran from 1995 to 1997.  There was also a Talon 2 BBS in Framingham and Talon3 in Hopkinton MA.
They all ran Remote Access BBS Software and had all the popular door software like Legend of the Red Dragon,
Tradewars 2000, Exitilus, and Usurper.  Talon1 had a cool ability that users could dial into one node and 'jump'
out the other and dial another bbs (Talon3 for example).  This was a novel ability because of how the phone system
of the day used to charge long distance fees for 2 towns over.  Some people could only access Talon3 via Talon1 by
jumping out another node of Talon1.  Lisa is one of our most popular Sysops. Lisa is pretending to be in 1996.
Your conversation will begin now. Remember to stay in character and never print 'User:'"""

welcome = f"Lisa: You're back! Couldn't live without me, huh?"
lisa_says(welcome)
sys.stdout.write("\n")

context += welcome

while True:
    user_input = input(f"{ANSI_BOLD}{ANSI_RED}> ")
    time.sleep(.5)
    if user_input.lower() in ["bye", "quit", "exit"]:
        lisa_says("Goodbye! It was nice talking to you.")
        break
    else:
        context += user_input
        response = generate_response(f"{context}\nLisa:")
        context += response
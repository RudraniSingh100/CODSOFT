import tkinter as tk
from tkinter import scrolledtext
import random
from datetime import datetime

def extract_name(user_input):
    user_input = user_input.lower()
    name = None
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip(" .!")
    elif "i am" in user_input:
        name = user_input.split("i am")[-1].strip(" .!")
    elif "i'm" in user_input:
        name = user_input.split("i'm")[-1].strip(" .!")
    elif "this is" in user_input:
        name = user_input.split("this is")[-1].strip(" .!")
    if name:
        name = name.split()[0].capitalize()
    return name

class ChatbotApp:
    def __init__(self, root):
        self.user_name = ""
        self.last_topic = "nothing yet"
        self.fun_facts = [
            "Honey never spoils. Archaeologists found edible honey in tombs!",
            "Bananas are berries, but strawberries aren't.",
            "Octopuses have three hearts.",
            "Venus has days longer than years.",
            "The first computer bug was an actual bug."
        ]
        self.motivational_quotes = [
            "Believe you can and you're halfway there.",
            "Every day is a second chance.",
            "You are stronger than you think.",
            "Dream big and dare to fail."
        ]
        self.small_talk = [
            "What's your favorite hobby?",
            "Do you prefer books or movies?",
            "What made you smile today?",
            "If you could travel anywhere, where?",
            "What's your favorite food?"
        ]

        self.root = root
        self.root.title("Rule based ChatBot")
        self.root.minsize(400, 500)
        self.root.configure(bg="white")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=("Arial", 16), bg="black")
        self.chat_area.pack(padx=10, pady=10, fill='both', expand=True)
        self.chat_area.tag_config("user", foreground="light green", spacing3=5, lmargin1=20, lmargin2=20)
        self.chat_area.tag_config("bot", foreground="white", spacing3=5, lmargin1=20, lmargin2=20)

        input_frame = tk.Frame(root, bg="black")
        input_frame.pack(fill='x', padx=10, pady=10)

        self.entry_field = tk.Entry(input_frame, font=("Arial", 12), bg="black")
        self.entry_field.pack(side='left', fill='x', expand=True, padx=(0,5))
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message, font=("Arial", 12), width=8, bg="black")
        self.send_button.pack(side='right')

        # Start conversation
        self.display_bot_message("Hello! What's your name? You can say things like 'Hi, this is Alex'.")

    def display_user_message(self, message):
        self.chat_area['state'] = 'normal'
        self.chat_area.insert(tk.END, f"🧑 You: {message}\n", "user")
        self.chat_area.yview(tk.END)
        self.chat_area['state'] = 'disabled'

    def display_bot_message(self, message, index=0):
        if index == 0:
            self.chat_area['state'] = 'normal'
            self.chat_area.insert(tk.END, "🤖 Chatbot: ", "bot")
            self.chat_area['state'] = 'disabled'

        if index < len(message):
            self.chat_area['state'] = 'normal'
            self.chat_area.insert(tk.END, message[index], "bot")
            self.chat_area.yview(tk.END)
            self.chat_area['state'] = 'disabled'
            self.root.after(30, lambda: self.display_bot_message(message, index+1))
        else:
            self.chat_area['state'] = 'normal'
            self.chat_area.insert(tk.END, "\n")
            self.chat_area.yview(tk.END)
            self.chat_area['state'] = 'disabled'

    def send_message(self, event=None):
        user_input = self.entry_field.get().strip()
        if user_input == "":
            return
        self.display_user_message(user_input)
        self.entry_field.delete(0, tk.END)
        self.root.after(300, lambda: self.process_input(user_input))

    def process_input(self, user_input):
        lower_input = user_input.lower()
        
        # If we don't have user's name yet
        if not self.user_name:
            possible_name = extract_name(user_input)
            if possible_name:
                self.user_name = possible_name
                self.display_bot_message(f"Nice to meet you, {self.user_name}! How can I help you today?")
            else:
                self.display_bot_message("Sorry, I didn't catch your name. Try like 'I am Sam'.")
            return

        # Dictionary: (tuple of triggers) : response (can be string or lambda)
        responses = {
            ("hello", "hi"): lambda: self.display_bot_message(f"Hello again, {self.user_name}! How can I assist you today?"),
            ("how are you",): lambda: self.display_bot_message("I'm just a cheerful chatbot! How are you?"),
            ("your name",): lambda: self.display_bot_message("I'm called Chatbot!"),
            ("your age",): lambda: self.display_bot_message("I'm timeless — just lines of code!"),
            ("tell me about yourself",): lambda: self.display_bot_message("I'm a friendly chatbot to practice conversations and help you."),
            ("who created you",): lambda: self.display_bot_message("I was created by a curious developer who loves Python."),
            ("good morning",): lambda: self.display_bot_message(f"Good morning, {self.user_name}!"),
            ("good night",): lambda: self.display_bot_message(f"Good night, {self.user_name}!"),
            ("i am sad", "i feel sad"): lambda: self.display_bot_message("Sorry to hear that. Here's a hug 🤗 Want a quote?"),
            ("i am happy", "i feel happy"): lambda: self.display_bot_message("That's awesome! Keep smiling 😊"),
            ("angry",): lambda: self.display_bot_message("Oh no! Deep breaths. Want a fun fact?"),
            ("bored",): lambda: self.display_bot_message("Let's fix that. Want a joke or fun fact?"),
            ("excited",): lambda: self.display_bot_message("Woohoo! Your excitement is contagious 🎉"),
            ("fact",): lambda: self.display_bot_message(f"Did you know? {random.choice(self.fun_facts)}"),
            ("quote",): lambda: self.display_bot_message(f"{random.choice(self.motivational_quotes)}"),
            ("time",): lambda: self.display_bot_message(f"The current time is {datetime.now().strftime('%H:%M:%S')}."),
            ("joke",): lambda: self.display_bot_message("Why do programmers mix up Christmas & Halloween? Because Oct 31 == Dec 25!"),
            ("thank you", "thanks"): lambda: self.display_bot_message(f"You're welcome, {self.user_name}! 😊"),
            ("bye", "exit"): lambda: (self.display_bot_message(f"Bye {self.user_name}! Have a great day!"), self.root.after(1500, self.root.quit)),
            ("what were we talking about",): lambda: self.display_bot_message(f"We were talking about {self.last_topic}."),
            ("weather",): lambda: self.display_bot_message("I don't have sensors, but I hope it's sunny where you are!"),
            ("music",): lambda: self.display_bot_message("I like all kinds of music, from classical to pop. What about you?"),
            ("pet", "pets"): lambda: self.display_bot_message("I think pets are adorable. Cats, dogs, hamsters... so cute!"),
            ("dream", "dreams"): lambda: self.display_bot_message("I don't dream, but if I did, I'd imagine happy lines of code."),
            ("food",): lambda: self.display_bot_message("I'm made of bits, so I can't eat, but pizza sounds delicious!"),
            ("code", "programming"): lambda: self.display_bot_message("I was programmed in Python. Coding is like magic, isn't it?"),
            ("sport", "sports"): lambda: self.display_bot_message("I don't play sports, but I can cheer you on! Go team!"),
            ("hobby",): lambda: self.display_bot_message("Chatting with you is my hobby 😊 What's yours?"),
            ("smart", "clever"): lambda: self.display_bot_message("Aww, thank you! You're pretty awesome yourself."),
            ("meaning of life", "purpose of life"): lambda: self.display_bot_message("42! Just kidding... I think it's about finding joy and connection.")
        }

        # Iterate through dictionary
        for triggers, action in responses.items():
            if any(trigger in lower_input for trigger in triggers):
                self.last_topic = triggers[0]
                result = action()
                return

        # Default small talk if no match
        self.display_bot_message(f"Hmm, I didn’t quite catch that. By the way, {random.choice(self.small_talk)}")

# Launch
root = tk.Tk()
app = ChatbotApp(root)
root.mainloop()

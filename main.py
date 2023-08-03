from tkinter import *
import pandas
import random
# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Courier"

try:
    french_words = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    french_words = pandas.read_csv("data/french_words.csv")
    french_words_list = french_words.to_dict(orient="records")
    print(french_words_list)
else:
    french_words_list = french_words.to_dict(orient="records")
selection = {}
selection_english = ""
selection_french = ""
# ---------------------------- Generate New Card ------------------------------- #

def new_word():

    global selection_english, selection_french, timer, selection

    window.after_cancel(timer)
    selection = random.choice(french_words_list)
    print(selection)
    selection_french = selection["French"]
    print(selection_french)
    selection_english = selection["English"]
    card_front.itemconfig(language, text="French")
    card_front.itemconfig(card_front_word, text=f"{selection_french}")
    card_front.itemconfig(image, image=card_front_pic)
    timer = window.after(3000, flip_card)

# ---------------------------- Flip Card ------------------------------- #


def flip_card():

    global selection_english
    card_front.itemconfig(card_front_word, text=f"{selection_english}")
    card_front.itemconfig(language, text="English")
    card_front.itemconfig(image, image=card_back_pic)

# ---------------------------- Save Progress ------------------------------- #


def unknown_words():

    global selection

    words_list = french_words_list

    words_list.remove(selection)

    df = pandas.DataFrame(words_list)
    df.to_csv("data/words_to_learn.csv", index=False)

    new_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("French Words Flash Card App")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, flip_card)


# ------ Front of Card ---------- #
card_front = Canvas(width=800, height=526)
card_front_pic = PhotoImage(file="images/card_front.png")
image = card_front.create_image(400, 263, image=card_front_pic)
language = card_front.create_text(400, 150, text="French", fill="Black", font=(FONT_NAME, 40, "italic"))
card_front_word = card_front.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))
card_front.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_front.grid(row=0, column=1)


# ------ Back of Card ---------- #
card_back = Canvas(width=850, height=540, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back_pic = PhotoImage(file="images/card_back.png")


# ------ Buttons ---------- #

correct_button = Button()
correct_button_image = PhotoImage(file="images/right.png")
correct_button.config(width=100, height=100, image=correct_button_image,
                      command=unknown_words, highlightthickness=0, background=BACKGROUND_COLOR)
correct_button.grid(row=1, column=0)

wrong_button = Button()
wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button.config(width=100, height=100, image=wrong_button_image,
                    command=new_word, highlightthickness=0, background=BACKGROUND_COLOR)
wrong_button.grid(row=1, column=2)


window.mainloop()

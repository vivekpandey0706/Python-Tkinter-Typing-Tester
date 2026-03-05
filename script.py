import tkinter
import random
import os
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
word_bank_dir = os.path.join(current_dir,"words.txt")

stage = tkinter.Tk()
stage.title("Typing Test")
stage.geometry("800x600")
box = tkinter.Entry(stage)

output_display = tkinter.Label(stage, text="Time: 60 | WPM: 0 | Raw: 0 | Accuracy 0%", font=("Arial",16))
output_display.pack(pady=10)

display_text = tkinter.Text(stage,height=2,width=40,font=("Arial",24),wrap=tkinter.WORD)
display_text.tag_config("highlight", background="yellow", foreground="black")
display_text.tag_config("correct", foreground="green")
display_text.tag_config("incorrect", foreground="red")
display_text.pack(pady=20)


with open(word_bank_dir,"r") as data:
    
    word_bank = [line.strip() for line in data.readlines()]



active_words = []
current_word_index = 0
time_left = 60
correct_words = 0
correct_chars = 0
words_typed = 0
total_characters_typed = 0
typing_started = False

selected_time = tkinter.IntVar(value=60) 
selected_mode = tkinter.StringVar(value="Normal")
wpm_list = []
time_list = []
raw_list = []

def highlight_display():
    typed = box.get().strip()
    display_text.config(state=tkinter.NORMAL)
    
    display_text.delete("1.0", tkinter.END)

    for i in range(len(active_words)):

        if i == current_word_index:
            target_word = active_words[i]

            for j, char in enumerate(target_word):
                if j < len(typed):
                    if typed[j] == char:
                        display_text.insert(tkinter.END, char, ("highlight","correct"))
                    else:
                        
                        display_text.insert(tkinter.END, char, ("highlight","incorrect"))
                else:
                    display_text.insert(tkinter.END, char, "highlight")

            if len(typed) > len(target_word):
                extra = typed[len(target_word):]
                display_text.insert(tkinter.END, extra, "incorrect")

        else:
            display_text.insert(tkinter.END, active_words[i])

        display_text.insert(tkinter.END, " ")

    display_text.config(state=tkinter.DISABLED)
    
def start_timer(event):
    global typing_started


    if not typing_started:
        typing_started = True
        update_timer()

def update_timer():
    global time_left, typing_started

    if time_left>0:
        
    
        accuracy = 0
        if total_characters_typed>0:
            accuracy = (correct_chars/total_characters_typed) *100
        
        total_time = selected_time.get()
        
        time_spent_min = (total_time-time_left)/60
        wpm = 0
        raw_wpm = 0
        
        
        if(time_spent_min>0):
            wpm = (correct_chars/5)/time_spent_min
            raw_wpm = (total_characters_typed/5)/time_spent_min
            
            

        output_display.config(text=f"Time: {time_left} | WPM: {round(wpm)} | Raw: {round(raw_wpm)} | Accuracy: {round(accuracy)}%")
        time_left-=1
        stage.after(1000,update_timer)

    else:
        typing_started = False
        box.config(state=tkinter.DISABLED)
        accuracy = 0
        if total_characters_typed > 0:
            accuracy = (correct_chars / total_characters_typed) * 100
            
        total_time = selected_time.get()
        wpm = (correct_chars / 5) / (total_time / 60)
        raw_wpm = (total_characters_typed/5)/(total_time/60)
        
        
        output_display.config(text=f"Time's up! | WPM: {round(wpm)} | Raw: {round(raw_wpm)} | Accuracy: {round(accuracy)}%")
        show_graph()
    if time_left>0:
        wpm_list.append(wpm)
        raw_list.append(raw_wpm)
        time_list.append(selected_time.get()-time_left-1)

def reset():
    
    global time_left, correct_words, words_typed, typing_started, current_word_index, correct_chars, total_characters_typed, time_list, wpm_list, raw_list
    
    time_left = selected_time.get()
    correct_words = 0
    correct_chars = 0
    words_typed = 0
    total_characters_typed =0
    typing_started = False
    time_list = []
    wpm_list = []
    raw_list = []
    
    box.config(state=tkinter.NORMAL) 
    box.delete(0, tkinter.END)       
    output_display.config(text=f"Time: {time_left} | WPM: 0 | Raw: 0 | Accuracy 0%")
    
    load_words()
    box.focus_force()

def load_words():
    global active_words, current_word_index
    
    active_words = random.sample(word_bank,k=14)

    if selected_mode.get() =="Advanced":
        for i in range(len(active_words)):
            chance = random.random()
            if chance <0.3:
                active_words[i] = active_words[i].capitalize()
            elif chance <0.6:
                active_words[i] = active_words[i] + str(random.randint(0,99))
            elif chance <0.9:
                active_words[i] = active_words[i] + random.choice([".",",","?","!"])
 
    current_word_index = 0
    highlight_display()

def check_word(event):
    global current_word_index, correct_words, words_typed,correct_chars, total_characters_typed

    current_text = box.get().strip()
    target_word = active_words[current_word_index]

    if(current_text==""):
        return "break"
    
    words_typed+=1
    total_characters_typed += len(current_text) +1

    if(current_text==target_word):
        print("Correct")
        correct_words+=1
        correct_chars+= len(target_word) +1
    else:
        print(f"Wrong, u typed {current_text} but you needed to type {target_word}")
        for i in range(min(len(current_text), len(target_word))):
            if current_text[i] == target_word[i]:
                correct_chars += 1
    
    current_word_index+=1

    if(current_word_index==len(active_words)):
        load_words()
    else:
        highlight_display()

    box.delete(0,tkinter.END)
    return "break"

def check_letters(event):
    highlight_display()


def show_graph():

    plt.figure()

    plt.plot(time_list,wpm_list,label = "WPM")
    plt.plot(time_list,raw_list, label = "Raw")
    plt.xlabel("Time(second)")
    plt.ylabel("WPM")
    plt.title("Typing Speed vs Time")
    plt.legend()
    plt.show()
    plt.close()




    
mode_frame = tkinter.Frame(stage)
mode_frame.pack(pady=5)

tkinter.Radiobutton(mode_frame, text="Normal", variable=selected_mode, value="Normal", command=reset).pack(side=tkinter.LEFT)
tkinter.Radiobutton(mode_frame, text="Advanced", variable=selected_mode, value="Advanced", command=reset).pack(side=tkinter.LEFT)

time_frame = tkinter.Frame(stage)
time_frame.pack(pady=5)

tkinter.Radiobutton(time_frame, text="15s", variable=selected_time, value=15, command=reset).pack(side=tkinter.LEFT)
tkinter.Radiobutton(time_frame, text="30s", variable=selected_time, value=30, command=reset).pack(side=tkinter.LEFT)
tkinter.Radiobutton(time_frame, text="45s", variable=selected_time, value=45, command=reset).pack(side=tkinter.LEFT)
tkinter.Radiobutton(time_frame, text="60s", variable=selected_time, value=60, command=reset).pack(side=tkinter.LEFT)


box.pack()
reset_button = tkinter.Button(stage, text = "Reset", command=reset)
reset_button.pack(pady=10)

box.bind('<KeyPress>', start_timer)
box.bind('<space>', check_word)
box.bind('<KeyRelease>',check_letters)



load_words()

stage.lift()
box.focus_force()

stage.mainloop()





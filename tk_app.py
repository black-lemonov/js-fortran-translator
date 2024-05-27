import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import filedialog as fd
from tkinter import messagebox
from lab1_lexical_scanner import scan
from lab2_rpn import rpn
from lab3_translator import to_fortran
from lab4_syntax_analyzer import program


def on_closing():
    '''Завершает программу при закрытии окна'''
    root.destroy()
    root.quit()
    

def get_file():
    '''Заполняет текстбокс кодом из файла'''

    filepath = fd.askopenfilename()

    try:
        
        get_result_btn['state'] = tk.NORMAL
        check_syntax_btn['state'] = tk.NORMAL

        file_text['state'] = tk.NORMAL

        with open(filepath) as js_file:
            file_text.delete(1.0, tk.END)
            file_text.insert(tk.END, js_file.read()) 

        scan(filepath)
        
    except FileNotFoundError:
        print("Ошибка: файл с таким именем не найден")


def get_lexemes(_):
    '''Заполняет текстбокс лексемами и ОПЗ из разбора'''
    
    check_syntax_btn['state'] = tk.NORMAL
    res_text['state'] = tk.NORMAL
    res_combo['state'] = "readonly"
    
    res_text.delete(1.0, tk.END)

    try:
        match res_combo.get():
            case "Fortran":
                to_fortran()
                res_text.insert(tk.END, open('inter-results/3_fortran.txt').read())
            case "ОПЗ":
                rpn()
                res_text.insert(tk.END, open('inter-results/2_reverse_polish_entry.txt').read())
            case "Лексемы":
                res_text.insert(tk.END, open('inter-results/1_tokens.txt').read())
            case "Идентификаторы":
                res_text.insert(tk.END, open('lexemes/I.json').read())
            case "Числовые константы":
                res_text.insert(tk.END, open('lexemes/N.json').read())
            case "Символьные константы":
                res_text.insert(tk.END, open('lexemes/C.json').read())
            case "Ключевые слова":
                res_text.insert(tk.END, open('lexemes/W.json').read())
            case "Операторы":
                res_text.insert(tk.END, open('lexemes/O.json').read())
            case "Разделители":
                res_text.insert(tk.END, open('lexemes/R.json').read())
    except FileNotFoundError:
        print('Ошибка: файл с лексемами не найден')


def check_syntax():
    '''Проверяет корректность синтаксиса в файле'''
    try:
        program()
        messagebox.showinfo("Проверка синтаксиса...", "Ошибки не найдены.")
    except SyntaxError as e:
        messagebox.showinfo("Проверка синтаксиса...", e.msg)
        


        



root = tk.Tk()
root.title('Транслятор JS -> Fortran')

root.geometry('1360x640')

# Кнопки для разбора

btns_frame = tk.Frame(root)
btns_frame.pack(side=tk.LEFT, anchor=tk.W, padx=10, pady=10, fill=tk.Y, expand=True)

btns_label = tk.Label(btns_frame, text='Выбрать шаг')
btns_label.pack()

choose_file_btn = tk.Button(btns_frame, text='Выбор файла', command=get_file)
choose_file_btn.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

get_result_btn = tk.Button(btns_frame, text='Выполнить разбор', state=tk.DISABLED)
get_result_btn.bind("<Button-1>", get_lexemes)
get_result_btn.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

check_syntax_btn = tk.Button(btns_frame, text='Проверить синтаксис', command=check_syntax, state=tk.DISABLED)
check_syntax_btn.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


# Окно исходного файла

file_frame = tk.Frame(root)
file_frame.pack(side=tk.LEFT, anchor=tk.W, padx=10, pady=10, fill=tk.BOTH, expand=True)

file_label = tk.Label(file_frame, text="Исходный код")
file_label.pack()

file_text = st.ScrolledText(file_frame, font="Consolas 12", state=tk.DISABLED)
file_text.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=10, fill=tk.BOTH, expand=True)

res_frame = tk.Frame(root)
res_frame.pack(side=tk.LEFT, anchor=tk.E, padx=10, pady=10, fill=tk.BOTH, expand=True)

res_combo = ttk.Combobox(res_frame, values=["Лексемы", "Идентификаторы", "Числовые константы", "Символьные константы", "Ключевые слова", "Операторы", "Разделители", "ОПЗ", 'Fortran'], state=tk.DISABLED)
res_combo.current(0)
res_combo.bind("<<ComboboxSelected>>", get_lexemes)
res_combo.pack()

res_text = st.ScrolledText(res_frame, font="Consolas 12", state=tk.DISABLED)
res_text.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=10, fill=tk.BOTH, expand=True)

            
root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()
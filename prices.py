import tkinter as tk

win = tk.Tk()
fr_greet = tk.Frame(height=100)
greeting = tk.Label(text='Willkommen beim Pizza Haus',master = fr_greet)
greeting.grid(pady = 20)
fr_greet.grid(sticky='ns')



fr_pay= tk.Frame()
lbl1 = tk.Label(text= 'Bitte stellen Sie Ihre Wunschpizza zusammen', master = fr_pay)
lbl1.grid()


PAY_OPTIONS =['Barzahlung','Sofortüberweisung']
str_var = tk.StringVar(win)
str_var.set(PAY_OPTIONS[0]) #default value

drp_menu = tk.OptionMenu(fr_pay,str_var,*PAY_OPTIONS)
drp_menu.grid()




def ok():
    print(f'sie haben {str_var.get()} ausgewaehlt')

btn_ok = tk.Button(master = fr_pay,text = 'OK',command = ok)
btn_ok.grid()

fr_order = tk.Frame()
PIZZA_OPTIONS = ['Salami','Thunfisch','extra Käse','Schinken','Pilze','Artischocken']

btns_PIZZA_OPTONS =[]
j=0
for i in range(len(PIZZA_OPTIONS)):
    btns_PIZZA_OPTONS.append(tk.Checkbutton(master=fr_order,text =PIZZA_OPTIONS[i]))
    if i<len(PIZZA_OPTIONS)//2:
        btns_PIZZA_OPTONS[i].grid(row =i,column=1)
    else:
        btns_PIZZA_OPTONS[i].grid(row =j,column=2)
        j+=1

orders = []
def get_button_states():
    buttons = btns_PIZZA_OPTONS
    for i in buttons:
        if i.get():
            orders.append(i)
    for i in orders:
        print(i.text)

btn_confirm = tk.Button(master= fr_order,text='Bestellung bestätigen',command=get_button_states)
btn_confirm.grid()



fr_order.grid()
fr_pay.grid()




win.mainloop()
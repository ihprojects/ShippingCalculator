import tkinter as tk
import json_reader 
import parcelServiceOption
data = json_reader.read_file()

new_data ,update_from = json_reader.get_newest(data)
parcelservices = []
lst = json_reader.create_info_list(new_data)
for i in lst:
    parcelservices.append(parcelServiceOption.ParcelService(i))

ps =parcelservices[1]



# border_effects = {
#     "flat": tk.FLAT,
#     "sunken": tk.SUNKEN,
#     "raised": tk.RAISED,
#     "groove": tk.GROOVE,
#     "ridge": tk.RIDGE,
# }


# for relief_name, relief in border_effects.items():
#     frame = tk.Frame(master=window, relief=relief, borderwidth=5)
#     frame.pack(side=tk.LEFT)
#     label = tk.Label(master=frame, text=relief_name)
#     label.pack()




def get_strsize_limit(size_limit):
    limits=[]
    for i in size_limit:
        if i!= 1000:
            limits.append(i)
    text ='max Länge '
    counter = 0
    for i in limits: 
        text += str(i)
        text+='cm '
        # if len(limits)
    return text


def show_prices(parcelServices):
    win = tk.Tk()
    fr_greet = tk.Frame(height=100)
    greeting = tk.Label(text='Preisliste',master = fr_greet,font=(None, 20))
    greeting.grid(pady = 20)
    fr_greet.grid(sticky='ns')



    fr_packages =tk.Frame( borderwidth=5)
    row=1
    for i in parcelServices:
        col =0
        counter =0
        is_first_row=True
        fr = tk.Frame(relief=tk.GROOVE, borderwidth=5,bg="#dcddd8")
        lbl = tk.Label(text=f'{i.name}',master = fr,font=(None, 15),bg="#dcddd8")
        lbl.grid(row=0,column=0,sticky='w')
        for j in i.parcel_options:
            fr_small = tk.Frame(relief=tk.GROOVE, borderwidth=5,master=fr)
            lbl_title = tk.Label(text=f'{j.name}',master = fr_small,bg='white',font=(None, 12))
            lbl = tk.Label(text=f'{get_strsize_limit(j.size_limit)}\nbis {j.weight_limit} kg',master = fr_small,bg='white',font=(None, 10))
            lbl_price = tk.Label(text=f'{j.price} €',master = fr_small,bg='white',font=(None, 12))
            lbl_title.grid(row=0)
            lbl.grid(row=1)
            lbl_price.grid(row=2)
            fr_small.grid(row =row,column=col,sticky ='we')
            col+=1

            counter+=1
        fr.grid(sticky ='we',column=0)

    fr_packages.grid()
    win.mainloop()


if __name__ == '__main__':
    show_prices(parcelservices)
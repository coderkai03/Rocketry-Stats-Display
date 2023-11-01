import tkinter as tk

#UI root
root = tk.Tk()
root.title('Rocket Data & Stats')

#UI window
window = tk.Frame(root)
window.pack()

# Pressure/temp frames
press_temp_frame = tk.Frame(window, padx=50, pady=50)
press_temp_frame.grid(row=0, column=0)

# create pressure labels
pressure_displays=[]

for i in range(3):
    label = tk.Label(
        press_temp_frame,
        text=f"Pressure {i + 1}: Placeholder",
        borderwidth=1,
        relief='solid',
        padx=5,
        pady=5,
    )
    label.grid(row=i + 1, column=0)
    pressure_displays.append(label)

    # create pressure labels
temperature_displays=[]

for i in range(4):
    label = tk.Label(
        press_temp_frame,
        text=f"Temperature {i + 1}: Placeholder",
        borderwidth=1,
        relief='solid',
        padx=5,
        pady=5,
    )
    label.grid(row=i, column=1)
    pressure_displays.append(label)

# #create pressure Labels
# pressure1_val = tk.Label(window, text='Pressure 1')
# pressure1_val.grid(row=1, column=0)
# pressure_displays.append(pressure1_val)

# pressure2_val = tk.Label(window, text='Pressure 2')
# pressure2_val.grid(row=2, column=0)
# pressure_displays.append(pressure1_val)

# pressure3_val = tk.Label(window, text='Pressure 3')
# pressure3_val.grid(row=3, column=0)
# pressure_displays.append(pressure1_val)



root.mainloop()
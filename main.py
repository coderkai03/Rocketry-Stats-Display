import tkinter as tk

#UI root
root = tk.Tk()
root.title('Rocket Data & Stats')

#UI window
window = tk.Frame(root)
window.pack()

# Pressure/temp frames
press_temp_frame = tk.Frame(window)
press_temp_frame.grid(row=0, column=0)

# pressure displays array
pressure_displays=[]

#create pressure Labels
pressure1_val = tk.Label(window, text='Pressure 1')
pressure1_val.grid(row=1, column=0)
pressure_displays.append(pressure1_val)

pressure2_val = tk.Label(window, text='Pressure 2')
pressure2_val.grid(row=2, column=0)
pressure_displays.append(pressure1_val)

pressure3_val = tk.Label(window, text='Pressure 3')
pressure3_val.grid(row=3, column=0)
pressure_displays.append(pressure1_val)



root.mainloop()
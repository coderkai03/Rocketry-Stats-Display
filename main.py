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
        text=f"Pressure {i + 1}: 0 psi",
        borderwidth=1,
        relief='solid',
        padx=5,
        pady=5,
    )
    label.grid(row=i + 1, column=0)
    pressure_displays.append(label)

# create temperature labels
temperature_displays=[]

for i in range(4):
    label = tk.Label(
        press_temp_frame,
        text=f"Temperature {i + 1}: 0 °F",
        borderwidth=1,
        relief='solid',
        padx=5,
        pady=5,
    )
    label.grid(row=i, column=1)
    pressure_displays.append(label)

# servo/ignition frame
servo_ign_frame = tk.Frame(window, padx=50, pady=50)
servo_ign_frame.grid(row=1, column=0)

#servo ign array
servo_ign_displays=[]

#servos
for i in range(2):
    button = tk.Button(
        servo_ign_frame,
        text=f"Servo {i + 1}",
        borderwidth=5,
        relief='raised',
        padx=5,
        pady=5,
    )
    button.grid(row=1, column=i)
    servo_ign_displays.append(button)

#ignition
ign = tk.Button(
    servo_ign_frame,
    text="Ignition",
    borderwidth=5,
    relief='raised',
    padx=5,
    pady=5,
)
ign.grid(row=1, column=2)
servo_ign_displays.append(ign)


root.mainloop()
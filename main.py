import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random

def create_canvas(root, width, height):
    canvas = tk.Canvas(root, width=width, height=height, bg='white')
    canvas.pack()
    return canvas

def create_sensor_display(canvas, x, y, width, height):
    # Create scatterplot with transparent background
    canvas_widget, scatter_plot, timestamps, temperatures = create_scatterplot(canvas, x, y, width, height)

    # Create display (arrow and caption)
    arrow = create_display(canvas, x + 80, y + height / 2, x + 150, y + height / 2, "black", "Temp Sensor:", tk.E)

    # Start updating the graph using FuncAnimation
    ani = start_animation(canvas_widget, scatter_plot, timestamps, temperatures)

    return canvas_widget, scatter_plot, timestamps, temperatures, ani

def create_scatterplot(canvas, x, y, width, height):
    fig, ax = plt.subplots(figsize=(4, 4), tight_layout=True)

    # Initial data for demonstration
    initial_temperature = None

    timestamps = [0]
    temperatures = [0]

    scatter_plot = ax.scatter(timestamps, temperatures, color='blue', marker='o', s=5)
    ax.set_ylabel('Temp (F)')
    ax.set_yticks([60, 80])
    ax.set_ylim([60, 80])

    # Set the title with decreased font size
    ax.set_title('Temp Sensor (1)', fontsize=10)

    # Remove horizontal values on the x-axis
    ax.set_xticks([])
    ax.set_xlim([-10, 1])

    # Set the y-axis ticks to the range 70-75
    ax.set_yticks([70, 81])
    ax.set_ylim(60, 90)

    # Set the background color to transparent
    ax.set_facecolor('none')

    canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().place(x=x, y=y, width=width, height=height)

    return canvas_widget, scatter_plot, timestamps, temperatures

def create_rect(canvas, x, y, width, height, fill_color):
    rectangle = canvas.create_rectangle(x, y, width, height, fill=fill_color)
    return rectangle

def create_display(canvas, x1, y1, x2, y2, arrow_color, text, text_anchor):
    # Create horizontal arrow
    arrow = canvas.create_line(x1 + 100, y1, x2 + 100, y2, arrow=tk.LAST, width=2)

    return arrow

def update_graph(frame, canvas_widget, scatter_plot, timestamps, temperatures):
    # Generate a new temperature data point
    new_temperature = random.uniform(65, 75)

    # Append the new temperature to the data
    timestamps.append(timestamps[-1] + 1)
    temperatures.append(new_temperature)

    # Update the scatter plot with the new data
    scatter_plot.set_offsets(list(zip(timestamps, temperatures)))

    # Set x-axis limits based on the data
    scatter_plot.axes.set_xlim(max(timestamps) - 10, max(timestamps))

    # Print all temperature values in the console
    print("Temperature values:", temperatures)

def start_animation(canvas_widget, scatter_plot, timestamps, temperatures):
    # Use FuncAnimation for smooth animation
    ani = FuncAnimation(plt.gcf(), lambda frame: update_graph(frame, canvas_widget, scatter_plot, timestamps, temperatures), interval=100)
    
    # Return the animation object to prevent deletion
    return ani

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Temperature Sensor UI")

    canvas = create_canvas(root, 1280, 720)

    # Create temperature displays
    temp_sensors=[]
    temp_sensor1 = create_sensor_display(canvas, x=20, y=450, width=200, height=100)
    temp_sensor2 = create_sensor_display(canvas, x=20, y=550, width=200, height=100)

    # Create rectangles separately
    rect1 = create_rect(canvas, 300, 550, 320, 650, fill_color="lightblue")

    # Show the Tkinter window
    root.mainloop()

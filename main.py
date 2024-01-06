import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random

def create_canvas(root, width, height):
    canvas = tk.Canvas(root, width=width, height=height, bg='white')
    canvas.pack()
    return canvas

def create_scatterplot(canvas, x, y, width, height):
    fig, ax = plt.subplots(figsize=(4, 4), tight_layout=True)

    # Initial data for demonstration
    timestamps = [1]
    temperatures = [random.uniform(65, 75)]

    scatter_plot = ax.scatter(timestamps, temperatures, color='blue', marker='o', s=5)
    ax.set_ylabel('Temp (F)')

    # Set the title with decreased font size
    ax.set_title('Temp Sensor (1)', fontsize=10)

    # Remove horizontal values on the x-axis
    ax.set_xticks([])

    # Set the background color to transparent
    ax.set_facecolor('none')

    canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().place(x=x, y=y, width=width, height=height)

    return canvas_widget, scatter_plot, timestamps, temperatures

def create_rect(canvas, x1, y1, x2, y2, fill_color):
    rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
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
    scatter_plot.axes.set_xlim(min(timestamps), max(timestamps) + 1)

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

    canvas = create_canvas(root, 500, 500)

    # Create scatterplot with transparent background
    canvas_widget, scatter_plot, timestamps, temperatures = create_scatterplot(canvas, x=20, y=50, width=200, height=100)

    # Create vertical rectangle
    rectangle = create_rect(canvas, 280, 20, 300, 130, fill_color="lightblue")

    # Create display (arrow and caption)
    arrow = create_display(canvas, 110, 75, 180, 75, "black", "Temp Sensor:", tk.E)

    # Start updating the graph using FuncAnimation
    ani = start_animation(canvas_widget, scatter_plot, timestamps, temperatures)

    # Show the Tkinter window
    root.mainloop()

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random

# Global vars
directions = {
        'left': [-100, 0, -125, 0],
        'right': [100, 0, 125, 0],
        'up': [0, 100, 0, 125],
        'down': [0, -100, 0, -125]
    }

def create_canvas(root, width, height):
    canvas = tk.Canvas(root, width=width, height=height, bg='white')
    canvas.pack()
    return canvas

def create_sensor_display(canvas, x, y, width, height, title, graph_type, direction):
    # Create graph with transparent background
    canvas_widget, line_plot, timestamps, data = create_graph(canvas, x, y, width, height, title, graph_type)

    # Create display (arrow and caption)
    arrow = create_arrow(canvas, x + 80, y + height / 2, x + 150, y + height / 2, "black", title, tk.E, direction)

    # Start updating the graph using FuncAnimation
    ani = start_animation(canvas_widget, line_plot, timestamps, data, graph_type)

    return canvas_widget, line_plot, timestamps, data, ani

def create_graph(canvas, x, y, width, height, title, graph_type):
    fig, ax = plt.subplots(figsize=(4, 4), tight_layout=True)

    # Initial data for demonstration
    initial_value = 0

    timestamps = [0]
    data = [initial_value]

    # Set the appropriate graph type
    if graph_type == "temperature":
        line_plot, = ax.plot(timestamps, data, color='blue', linewidth=2)
        ax.set_ylabel('Temp (F)')
        ax.set_yticks([60, 80])
        ax.set_ylim([60, 80])
    elif graph_type == "pressure":
        line_plot, = ax.plot(timestamps, data, color='red', linewidth=2)
        ax.set_ylabel('Pressure')
        ax.set_yticks([0, 100])
        ax.set_ylim([0, 100])

    # Set the title with decreased font size
    ax.set_title(title, fontsize=10)

    # Remove horizontal values on the x-axis
    ax.set_xticks([])
    ax.set_xlim([-10, 1])

    # Set the background color to transparent
    ax.set_facecolor('none')

    canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().place(x=x, y=y, width=width, height=height)

    return canvas_widget, line_plot, timestamps, data

def create_rect(canvas, x, y, width, height, fill_color):
    rectangle = canvas.create_rectangle(x, y, width, height, fill=fill_color)
    return rectangle

def create_arrow(canvas, x1, y1, x2, y2, arrow_color, text, text_anchor, direction):
    # Create horizontal arrow
    arrow = canvas.create_line(
        x1 + directions[direction][0],
        y1 + directions[direction][1],
        x2 + directions[direction][2],
        y2 + directions[direction][3],
        arrow=tk.LAST,
        width=2
    )

    return arrow

def update_graph(frame, canvas_widget, line_plot, timestamps, data, graph_type):
    # Generate a new data point
    new_data = random.uniform(0, 100) if graph_type == "pressure" else random.uniform(65, 75)

    # Append the new data to the list
    timestamps.append(timestamps[-1] + 1)
    data.append(new_data)

    # Update the line plot with the new data
    line_plot.set_data(timestamps, data)

    # Set x-axis limits based on the data
    line_plot.axes.set_xlim(max(timestamps) - 10, max(timestamps))

    # Print all data values in the console
    print(f"{graph_type.capitalize()} values:", data)

def start_animation(canvas_widget, line_plot, timestamps, data, graph_type):
    # Use FuncAnimation for smooth animation
    ani = FuncAnimation(plt.gcf(), lambda frame: update_graph(frame, canvas_widget, line_plot, timestamps, data, graph_type), interval=100)
    
    # Return the animation object to prevent deletion
    return ani

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sensor UI")

    canvas = create_canvas(root, 1280, 720)

    # Create temperature displays
    temp_sensors = []
    temp_sensor1 = create_sensor_display(canvas, x=20, y=200, width=200, height=100, title="Temp Sensor (1)", graph_type="temperature", direction='right')
    temp_sensor3 = create_sensor_display(canvas, x=20, y=50, width=200, height=100, title="Temp Sensor (3)", graph_type="temperature", direction='left')
    temp_sensor4 = create_sensor_display(canvas, x=200, y=450, width=200, height=100, title="Temp Sensor (4)", graph_type="temperature", direction='up')
    temp_sensor5 = create_sensor_display(canvas, x=500, y=550, width=200, height=100, title="Temp Sensor (5)", graph_type="temperature", direction='down')

    # Create rectangles separately
    rect1 = create_rect(canvas, 300, 100, 320, 350, fill_color="lightblue")
    rect2 = create_rect(canvas, 300, 450, 320, 650, fill_color="lightblue")

    # Show the Tkinter window
    root.mainloop()

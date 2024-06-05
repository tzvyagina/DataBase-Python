import math
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.patches

# Getting data from database: percentage of Ice types in one particular day of the year (in colors)
def particular_data_extracting(year: int, day: int) -> dict:
    column_data = {}
    conn = sqlite3.connect('DataBase_IceCharts_March2020-2023.db')
    c = conn.cursor()
    c.execute("SELECT *from IceCharts WHERE Year=(?)", (year,))
    rows = c.fetchall()
    for row in rows:
        column_data[row[1]] = row[day + 1]
    return column_data


# Preparing data about one particular line on the planned Round Plot
def line_segment_forming(
        column_data: dict,
        x_center: float,
        y_center: float,
        reference_radius: float
) -> tuple:
    summa = 0
    color_list_x = [x_center]
    color_list_y = [reference_radius+y_center]
    for key, value in column_data.items():
        summa += value
        color_list_x.append(x_center)
        color_list_y.append(summa+reference_radius+y_center)

    return color_list_x, color_list_y


# Calculating real position of the line on the planned Round Plot
def line_segment_positioning(
        year: int,
        day: int,
        initial_line_position: tuple,
        step: float,
        reference_radius: float,
        center_y: float
) -> tuple:
    angle_addition = 0
    if year == 2020:
        angle_addition = math.pi
    if year == 2021:
        angle_addition = math.pi / 2
    if year == 2023:
        angle_addition = 3 * math.pi / 2

    alpha = (day - 1) * math.pi * step / 180 + angle_addition

    new_line_position_x = [initial_line_position[0][0]+reference_radius*math.sin(alpha)]
    new_line_position_y = [center_y + reference_radius * math.cos(alpha)]

    i = 0
    while i < len(initial_line_position[0])-1:
        line_length = initial_line_position[1][i+1] - initial_line_position[1][i]
        new_line_position_x.append(new_line_position_x[-1]+line_length*math.sin(alpha))
        new_line_position_y.append(new_line_position_y[-1] + line_length * math.cos(alpha))

        i += 1
    return new_line_position_x, new_line_position_y


# Instant positioning of 4 lines in the same day of the year (corresponding 4 years)
def sector_filling(
        day: int,
        x_center: float,
        y_center: float,
        reference_radius: float,
        step: float
) -> list:
    four_lines_positions = []
    for year in range(2020, 2024):
        column_data = particular_data_extracting(year=year, day=day)

        line_old_position = line_segment_forming(
            column_data=column_data,
            x_center=x_center,
            y_center=y_center,
            reference_radius=reference_radius
        )
        line_new_position = line_segment_positioning(
            year=year,
            day=day,
            initial_line_position=line_old_position,
            step=step,
            reference_radius=reference_radius,
            center_y=y_center
        )
        four_lines_positions.append(line_new_position)
    return four_lines_positions


def round_plot_initialization(x_center: float, y_center: float) -> tuple:
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.set_xlim(0.12, 2.28)
    ax.set_ylim(0.12, 2.28)
    plt.axis('off')

    circle1 = matplotlib.patches.Circle((x_center, y_center), radius=1, fill=False, alpha=0.3)
    ax.add_patch(circle1)
    ax.text(x_center + 1, y_center + 0.03, '60%', fontsize=13, alpha=0.3)

    circle2 = matplotlib.patches.Circle((x_center, y_center), radius=0.8, fill=False, alpha=0.3)
    ax.add_patch(circle2)
    ax.text(x_center + 0.8, y_center + 0.03, '40%', fontsize=13, alpha=0.3)

    circle3 = matplotlib.patches.Circle((x_center, y_center), radius=0.6, fill=False, alpha=0.3)
    ax.add_patch(circle3)
    ax.text(x_center + 0.6, y_center + 0.03, '20%', fontsize=13, alpha=0.3)

    ax.text(x_center - 0.22, y_center - 0.03, 'March 1-31', fontsize=22, alpha=0.8)
    ax.text(x_center - 1.1, y_center - 0.7, '2020', fontsize=22, alpha=0.8)
    ax.text(x_center - 1.1, y_center + 0.7, '2023', fontsize=22, alpha=0.8)
    ax.text(x_center + 0.9, y_center - 0.7, '2021', fontsize=22, alpha=0.8)
    ax.text(x_center + 0.9, y_center + 0.7, '2022', fontsize=22, alpha=0.8)

    return fig, ax


def round_plot_obtaining(
        fig,
        ax,
        limit: int,
        x_center: float,
        reference_radius: float,
        step: float
) -> tuple:

    for i in range(1, limit):

        position = sector_filling(
            day=i,
            x_center=x_center,
            y_center=x_center,
            reference_radius=reference_radius,
            step=step
        )

        for j in range(0,4):
            ax.plot(
                [position[j][0][0],position[j][0][1]],
                [position[j][1][0],position[j][1][1]],
                color='yellow',
                linewidth=3)
            ax.plot(
                [position[j][0][1],position[j][0][2]],
                [position[j][1][1],position[j][1][2]],
                color='orange',
                linewidth=3)
            ax.plot(
                [position[j][0][2],position[j][0][3]],
                [position[j][1][2],position[j][1][3]],
                color='red',
                linewidth=3)
            ax.plot(
                [position[j][0][3],position[j][0][4]],
                [position[j][1][3],position[j][1][4]],
                color='firebrick',
                linewidth=3)

    return fig, ax


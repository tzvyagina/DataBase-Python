import matplotlib.pyplot as plt
import matplotlib.animation as animation
import functions
import glob
from PIL import Image

# 1. SETTINGS:
# Center of the round plot
X_0 = 1.2
Y_0 = 1.2
# Reference radius
R_0 = 0.4
# How many years have to be analysed?
SECTORS = 4
# How many days there are in a month?
DAYS = 31

# 2. CALCULATIONS:
STEP = 360/SECTORS/DAYS

# 3. CREATING AND FILLING AN IMAGE ARRAY
image_array = []

# Getting and Saving zero image into directory Steps
fig, ax = functions.round_plot_initialization(x_center=X_0, y_center=Y_0)
save_results_to =r'C:\Users\tlzvy\Desktop\GitHub Portfolio\Python Database Visualization\Steps'
plt.savefig(save_results_to + '\step0.png', dpi=300)

# Getting and Saving images from 1 to 31 into directory Steps
for i in range(1, 32):

    fig, ax = functions.round_plot_initialization(x_center=X_0, y_center=Y_0)
    fig, ax = functions.round_plot_obtaining(
            fig=fig,
            ax=ax,
            limit=i+1,
            x_center=X_0,
            reference_radius=R_0,
            step=STEP
    )
    save_results_to =r'C:\Users\tlzvy\Desktop\GitHub Portfolio\DataBase Visualization\Steps'
    plt.savefig(save_results_to + '\step' + str(1)*i + '.png', dpi=300)
    plt.close("all")

# 4.ANIMATED PLOT CREATING

# Creating a list with images
image_array = []

# Reading .png files from directory called `Steps` and Adding the files into the 'image_array' list
files = glob.glob(r"Steps/*.png")
for my_file in files:
    image = Image.open(my_file)
    image_array.append(image)

# Create the figure and axes objects
fig, ax = plt.subplots()

# Set the initial image
im = ax.imshow(image_array[0], animated=True)


# Creating updating function for animated plot
def update(i):
    im.set_array(image_array[i])
    return im,


# Creating initial parameters of the animated plot
def init():
    ax.set_xlim(200, 2800)
    ax.set_ylim(2800, 200)
    plt.axis('off')


# Create the animation object
animation_fig = animation.FuncAnimation(fig, update, frames=len(image_array), interval=400, repeat=False, init_func=init)

# Show the animation
animation_fig.save("Steps/animation.gif", dpi=200)
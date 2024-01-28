import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-l", type=int, default=100, help='boundary condition for left side of the plate')
    parser.add_argument("-t", type=int, default=100, help='boundary condition for top side of the plate')
    parser.add_argument("-r", type=int, default=100, help='boundary condition for right side of the plate')
    parser.add_argument("-b", type=int, default=100, help='boundary condition for bottom side of the plate')

    parser.add_argument("-d",   type=float, default=97, help='mm^2 / sec (aluminium - default)')
    parser.add_argument("-len", type=float, default=50, help='mm')
    parser.add_argument("-wid", type=float, default=50, help='mm')

    parser.add_argument("-tm", type=float, default=4, help='seconds')
    parser.add_argument("-n",  type=int, default=40, help='nodes')

    args = parser.parse_args()

    alpha = args.diffusivity
    length = args.length
    width = args.width
    nodes = args.nodes

    dx = length / nodes                                                     # spatial variation
    dy = length / nodes
    dt = min(dx ** 2 / (4 * alpha), dy ** 2 / (4 * alpha))                  # temporal variation
    time = args.time

    u = np.zeros((nodes, nodes)) + 20  # Plate is initially at 20 degrees C

    # Boundary Conditions
    u[:, 0] = args.left
    u[:, -1] = args.right
    u[0, :] = args.top
    u[-1, :] = args.bottom


    # Visualizing with a 3D plot
    plt.rcParams['animation.ffmpeg_path'] = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
    fig = plt.figure()
    axis = fig.add_subplot(111, projection='3d')


    def update_plot(frame):
        # global u, dt, alpha, dx, dy

        w = u.copy()

        for i in range(1, nodes - 1):
            for j in range(1, nodes - 1):
                dd_ux = (w[i - 1, j] - 2 * w[i, j] + w[i + 1, j]) / dx ** 2
                dd_uy = (w[i, j - 1] - 2 * w[i, j] + w[i, j + 1]) / dy ** 2

                u[i, j] = dt * alpha * (dd_ux + dd_uy) + w[i, j]

        x, y = np.meshgrid(np.linspace(0, length, nodes), np.linspace(0, width, nodes))
        axis.clear()
        pcm = axis.plot_surface(x, y, u, cmap=plt.cm.jet, vmin=0, vmax=100, antialiased=False)
        axis.set_zlim(0, 100)

        axis.set_title("Distribution at t: {:.3f} [s]".format(frame * dt))


    ani = FuncAnimation(fig, update_plot, frames=int(time / dt), repeat=False)

    FFwriter = animation.FFMpegWriter(fps=125)
    ani.save('heat_equation3d_2.mp4', writer=FFwriter, dpi=300)

    # ani.save('temperature_distributio3D.gif', writer='imagegick')         # if don't have ffmpeg

    plt.show()

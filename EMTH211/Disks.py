import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt



def main():
    """Disks
    circle1 = plt.Circle((3, 0), 1.5, color='green', alpha=0.5)
    circle2 = plt.Circle((-5, 0), 2.1, color='green', alpha=0.5)
    circle3 = plt.Circle((-6, 0), 0.2, color='green')
    circle4 = plt.Circle((2, 0), 0.2, color='green', )

    fig, ax = plt.subplots()

    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)
    ax.add_patch(circle4)

    yabs_max = abs(max(ax.get_ylim(), key=abs))
    xabs_max = abs(max(ax.get_ylim(), key=abs))

    scale_factor = 5
    ax.set_ylim(ymin=-yabs_max*4, ymax=yabs_max*4)
    ax.set_xlim(xmin=-xabs_max*8, xmax=xabs_max*6)

    ax.set_ylabel("Imaginary - Axis")
    ax.set_xlabel("Real - Axis")

    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.1)
    plt.show()
    """
    mYarray = np.array([[3,  2,   0,   0],
                        [1, -5, 0.1, 0.1],
                        [0, 0, -6, -0.1],
                        [0.5, 0.1, -0.1, 2]])
    eigenvalues, eigenvectors = la.eig(mYarray)
    print(eigenvalues)


if __name__ == "__main__":
    main()

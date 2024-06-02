
import numpy                    as np
import matplotlib.pyplot        as plt
import matplotlib.patches       as patches
import matplotlib.colorbar      as cbar

def MakeTestXYZFile(output_prefix, x_size, y_size):
    filename    = f'{output_prefix}.{x_size}.{y_size}.txt'
    arr         = np.random.standard_normal((x_size, y_size))
    f           = open(filename, 'wt')
    for x in range(0, len(arr)):
        for y in range(0, len(arr[x])):
            f.write(f'{x} {y} {arr[x][y]}\n')
    f.close()
    cmap        = plt.cm.RdYlBu_r
    plt.matshow(arr, cmap=cmap)
    plt.colorbar()
    png_filename    = f'{output_prefix}.{x_size}.{y_size}.png'
    plt.savefig(png_filename)
    plt.show()

def main():
    MakeTestXYZFile('test_xyz.01', 5, 10)

if __name__ == '__main__':
    main()
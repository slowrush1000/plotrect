
import sys
import numpy                    as np
import matplotlib.pyplot        as plt
import matplotlib.patches       as patches
import matplotlib.colorbar      as cbar

class PlotPointHeat:
    def __init__(self):
        self.m_filename         = ''
        self.m_output_prefix    = ''
        self.m_xs               = []
        self.m_ys               = []
        self.m_zs               = []
        self.m_x_pos            = 0
        self.m_y_pos            = 0
        self.m_z_pos            = 0
        self.m_x_grid           = 1
        self.m_y_grid           = 1
        self.m_llx              = 0.0
        self.m_lly              = 0.0
        self.m_urx              = 0.0
        self.m_ury              = 0.0
        self.m_z_range          = None
        self.m_grid_type        = 'max'
        self.m_arr              = []
        self.m_xyz_min_max      = [ None, None, None ]
        self.m_x_step           = 1.0
        self.m_y_step           = 1.0
    def PrintUsage(self):
        print(f'usage : plotpoint.py')
        print(f'python3 plotpoint.py output_prefix input_file x_pos y_pos z_pos x_grid y_grid llx lly urx ury <-max|-min|-avg> <-z_range z_min z_max>')
    def ReadArgs(self, args):
        print(f'# read args start')
        # 12, 13, 16, 17
        if 12 > len(args):
            self.PrintUsage()
            exit()
        self.m_output_prefix    = args[1]
        self.m_filename         = args[2]
        self.m_x_pos            = int(args[3])
        self.m_y_pos            = int(args[4])
        self.m_z_pos            = int(args[5])
        self.m_x_grid           = int(args[6])
        self.m_y_grid           = int(args[7])
        self.m_llx              = float(args[8])
        self.m_lly              = float(args[9])
        self.m_urx              = float(args[10])
        self.m_ury              = float(args[11])
        for pos in range(12, len(args)):
            if '-max' == args[pos]:
                self.m_grid_type    = 'max'
            elif '-min' == args[pos]:
                self.m_grid_type    = 'min'
            elif '-sum' == args[pos]:
                self.m_grid_type    = 'sum'
            elif '-z_range' == args[pos]:
                if (pos + 2) > len(args):
                    self.PrintUsage()
                    exit()
                else:
                    self.m_z_range   = [ float(args[pos + 1]), float(args[pos + 2]) ]
            else:
                self.PrintUsage()
                exit()
        print(f'# read args end')
    def PrintInputs(self):
        print(f'# print inputs start')
        print(f'    output prefix : {self.m_output_prefix}')
        print(f'    input file    : {self.m_filename}')
        print(f'    x pos         : {self.m_x_pos}')
        print(f'    y pos         : {self.m_y_pos}')
        print(f'    z pos         : {self.m_z_pos}')
        print(f'    x grid        : {self.m_x_grid}')
        print(f'    y grid        : {self.m_y_grid}')
        print(f'    llx           : {self.m_llx}')
        print(f'    lly           : {self.m_lly}')
        print(f'    urx           : {self.m_urx}')
        print(f'    ury           : {self.m_ury}')
        print(f'    grid type     : {self.m_grid_type}')
        if None == self.m_z_range:
            print(f'    z range       : not defined!')
        else:
            print(f'    z range       : {self.m_z_range[0]} - {self.m_z_range[1]}')
        print(f'# print inputs end')
    def ReadFile(self):
        print(f'# read file({self.m_filename}) start')
        f       = open(self.m_filename, 'rt')
        nlines  = 0
        max_pos = max(self.m_x_pos, max(self.m_y_pos, self.m_z_pos))
        while True:
            line    = f.readline()
            if not line:
                break 
            nlines  = nlines + 1
            if 0 == (nlines%1_000_000_000):
                print(f'    {nlines} lines')
            line    = line.lstrip().rstrip()
            tokens  = line.split()
            if len(tokens) <= max_pos:
                continue
            x       = float(tokens[self.m_x_pos])
            y       = float(tokens[self.m_y_pos])
            z       = float(tokens[self.m_z_pos])
            self.m_xs.append(x)
            self.m_ys.append(y)
            self.m_zs.append(z)
        f.close()
        print(f'    {nlines} lines')
        print(f'# read file({self.m_filename}) end')
    def FindMinMax(self):
        print(f'# find min/max start.')
        self.m_xyz_min_max[0]   = [ np.min(self.m_xs), np.max(self.m_xs) ]
        self.m_xyz_min_max[1]   = [ np.min(self.m_ys), np.max(self.m_ys) ]
        self.m_xyz_min_max[2]   = [ np.min(self.m_zs), np.max(self.m_zs) ]
        print(f'    x min/max : {self.m_xyz_min_max[0][0]} - {self.m_xyz_min_max[0][1]}')
        print(f'    y min/max : {self.m_xyz_min_max[1][0]} - {self.m_xyz_min_max[1][1]}')
        print(f'    z min/max : {self.m_xyz_min_max[2][0]} - {self.m_xyz_min_max[2][1]}')
        print(f'# find min/max end.')
    def MakeArr(self):
        print(f'# make arr start')
        #
        for x_index in range(0, self.m_x_grid):
            ys  = [ None ]*self.m_y_grid
            self.m_arr.append(ys)
        #self.m_arr  = [[None]*self.m_y_grid]*self.m_x_grid
        #
        self.m_x_step  = (self.m_urx - self.m_llx)/float(self.m_x_grid)
        self.m_y_step  = (self.m_ury - self.m_lly)/float(self.m_y_grid)
        print(f'    x step : {self.m_x_step}')
        print(f'    y step : {self.m_y_step}')
        #
        for pos in range(0, len(self.m_xs)):
            x   = self.m_xs[pos]
            y   = self.m_ys[pos]
            z   = self.m_zs[pos]
            #
            x_index = self.GetArrIndex(x, self.m_x_step, self.m_x_grid)
            y_index = self.GetArrIndex(y, self.m_y_step, self.m_y_grid)
            #
            print(f'    {self.m_arr[x_index][y_index]}')
            #
            if None == self.m_arr[x_index][y_index]:
                self.m_arr[x_index][y_index]    = z
            else:
                self.m_arr[x_index][y_index]    = self.GridType(self.m_grid_type, self.m_arr[x_index][y_index], z)
            #
            print(f'    {x} {y} {z} - {x_index} {y_index} {self.m_arr[x_index][y_index]}')
        #
        for x_index in range(0, len(self.m_arr)):
            for y_index in range(0, len(self.m_arr[x_index])):
                if None == self.m_arr[x_index][y_index]:
                    self.m_arr[x_index][y_index]    = self.m_xyz_min_max[2][0]
        #
        print(f'# make arr end')
    def PrintArr(self):
        print(f'# print arr start')
        print(self.m_arr)
        print(f'# print arr end')
    def DrawHeat(self):
        print(f'# draw heat start.')
        fig, ax     = plt.subplots()
        #
        x_labels    = []
        for pos in range(self.m_x_grid - 1, -1, -1):
#        for pos in range(0, self.m_x_grid):
            x_label = f'{(self.m_llx + self.m_x_step*float(pos)):.1f} - {(self.m_llx + self.m_x_step*float(pos + 1)):.1f}'
            x_labels.append(x_label)
        y_labels    = []
        for pos in range(0, self.m_y_grid):
            y_label = f'{(self.m_lly + self.m_y_step*float(pos)):.1f} - {(self.m_lly + self.m_y_step*float(pos + 1)):.1f}'
            y_labels.append(y_label)
        #
        self.m_arr  = self.m_arr[::-1]
        #
        im, cbar    = self.DrawHeatmap(np.array(self.m_arr), x_labels, y_labels, ax=ax, cmap='RdYlBu_r', cbarlabel='zs')
        png_filename    = self.m_output_prefix + '.heat.png'
        plt.title(f'{self.m_output_prefix}')
        plt.savefig(png_filename)
        fig.tight_layout()
        plt.show()
#        cmap    = plt.cm.RdYlBu_r
#        plt.matshow(self.m_arr, cmap=cmap)
#        plt.colorbar()
#        png_filename    = self.m_output_prefix + '.heat.png'
#        plt.savefig(png_filename)
#        plt.show()
        print(f'# draw heat end.')
    def DrawHeatmap(self, data, row_labels, col_labels, ax=None, cbar_kw=None, cbarlabel="", **kwargs):
        """
        Create a heatmap from a numpy array and two lists of labels.

        Parameters
        ----------
        data
            A 2D numpy array of shape (M, N).
        row_labels
            A list or array of length M with the labels for the rows.
        col_labels
            A list or array of length N with the labels for the columns.
        ax
            A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
            not provided, use current Axes or create a new one.  Optional.
        cbar_kw
            A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
        cbarlabel
            The label for the colorbar.  Optional.
        **kwargs
            All other arguments are forwarded to `imshow`.
        """
        if ax is None:
            ax = plt.gca()
        if cbar_kw is None:
            cbar_kw = {}
        # Plot the heatmap
        im = ax.imshow(data, **kwargs)
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
        # Show all ticks and label them with the respective list entries.
        ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
        ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)
        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), va="top", rotation=-90)
        # Turn spines off and create white grid.
        ax.spines[:].set_visible(False)
        #
        ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
        #ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)
        #
        return im, cbar
    def GridType(self, grid_type, arr_z, z):
        if 'max' == grid_type:
            return max(arr_z, z)
        elif 'min' == grid_type:
            return min(arr_z, z)
        elif 'sum' == grid_type:
            return arr_z + z
        else:
            return z
    def GetArrIndex(self, x, x_step, x_grid):
        x_index     = int(x/x_step)
        if x_index < 0:
            x_index     = 0
        if x_index >= x_grid:
            x_index     = x_grid - 1
        return x_index
    def Run(self, args):
        print(f'# plotpointheat.py start')
        self.ReadArgs(args)
        self.PrintInputs()
        self.ReadFile()
        self.FindMinMax()
        self.MakeArr()
        self.PrintArr()
        self.DrawHeat()
        print(f'# plotpointheat.py end')
#
def Test():
    arr = np.random.standard_normal((30, 40))
    print(arr)
    cmap    = plt.cm.RdYlBu_r
    plt.matshow(arr, cmap=cmap)
    plt.colorbar()
    plt.show()
#
def main(args):
    my_plot_point_heat    = PlotPointHeat()
    my_plot_point_heat.Run(args)
#    Test()
if __name__ == '__main__':
    main(sys.argv)
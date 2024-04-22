
import sys
import numpy                    as np
import matplotlib.pyplot        as plt
import matplotlib.patches       as patches
import matplotlib.colorbar      as cbar

class Rect:
    def __init__(self, llx = 0.0, lly = 0.0, urx = 0.0, ury = 0.0, value = 0.0):
        self.m_box      = [ llx, lly, urx, ury ]
        self.m_value    = value
    def SetLLX(self, llx):
        self.m_box[0]   = llx
    def GetLLX(self):
        return self.m_box[0]
    def SetLLY(self, lly):
        self.m_box[1]   = lly
    def GetLLY(self):
        return self.m_box[1]
    def SetURX(self, urx):
        self.m_box[2]   = urx
    def GetURX(self):
        return self.m_box[2]
    def SetURY(self, ury):
        self.m_box[3]   = ury
    def GetURY(self):
        return self.m_box[3]
    def GetWidth(self):
        return self.m_box[2] - self.m_box[0]
    def GetHeight(self):
        return self.m_box[3] - self.m_box[1]
    def SetValue(self, value):
        self.m_value = value
    def GetValue(self):
        return self.m_value
     
class Plotbox:
    def __init__(self):
        self.m_output_prefix    = ''
        self.m_input_filename   = ''
        self.m_box_pos          = [ 0, 0, 0, 0 ]
        self.m_value_pos        = -1
        self.m_max_pos          = -1
        self.m_rects            = []
        self.m_xy_lims          = [ [ sys.float_info.max, -sys.float_info.max ], [ sys.float_info.max, -sys.float_info.max] ]
        self.m_values_range     = [ sys.float_info.max, -sys.float_info.max ]
        #
        self.m_png_filename     = ''
    def SetOutputPrefix(self, output_prefix):
        self.m_output_prefix    = output_prefix
    def GetOutputPrefix(self):
        return self.m_output_prefix
    def ReadArgs(self, args):
        if 7 != len(args) and 8 != len(args):
            self.PrintUsage()
            exit(0)
        self.m_output_prefix    = args[1]
        self.m_input_filename   = args[2]
        self.m_box_pos[0]       = int(args[3])
        self.m_box_pos[1]       = int(args[4])
        self.m_box_pos[2]       = int(args[5])
        self.m_box_pos[3]       = int(args[6])
        if 8 == len(args):
            self.m_value_pos    = int(args[7])
        if -1 == self.m_value_pos:
            self.m_max_pos          = max(self.m_box_pos)
        else:
            self.m_max_pos          = max(max(self.m_box_pos), self.m_value_pos)
        self.m_png_filename     = self.m_output_prefix + str('.png')
    def PrintInput(self):
        print(f'# print input start.')
        print(f'   output prefix  : {self.m_output_prefix}')
        print(f'   file           : {self.m_input_filename}')
        print(f'   llx pos        : {self.m_box_pos[0]}')
        print(f'   lly pos        : {self.m_box_pos[1]}')
        print(f'   urx pos        : {self.m_box_pos[2]}')
        print(f'   ury pos        : {self.m_box_pos[3]}')
        print(f'   value pos      : {self.m_value_pos}')
        print(f'   png file       : {self.m_png_filename}')
        print(f'   max pos        : {self.m_max_pos}')
        print(f'# print input end.')
    def PrintUsage(self):
        print(f'plotbox.py usage:')
        print(f'% python plotbox.py output_prefix input_file llx_pos lly_pos urx_pos ury_pos <value_pos>')
    def ReadFile(self):
        print(f'# read file({self.m_input_filename}) start.')
        f = open(self.m_input_filename, 'rt')
        while True:
            line = f.readline()
            if not line:
                break
            if 0 == len(line):
                continue
            tokens  = line.split()
            if self.m_max_pos > len(tokens):
                continue
            llx     = float(tokens[self.m_box_pos[0]])    
            lly     = float(tokens[self.m_box_pos[1]])    
            urx     = float(tokens[self.m_box_pos[2]])    
            ury     = float(tokens[self.m_box_pos[3]])    
            value   = 0.0
            if -1 != self.m_value_pos:
                value   = float(tokens[self.m_value_pos])
            self.m_rects.append(Rect(llx, lly, urx, ury, value))
        f.close()
        print(f'# read file({self.m_input_filename}) end.')
    def FindXYLim(self):
        print(f'# find xy lim start.')
        for rect in self.m_rects:
            self.m_xy_lims[0][0]    = min(self.m_xy_lims[0][0], rect.GetLLX())
            self.m_xy_lims[0][1]    = max(self.m_xy_lims[0][1], rect.GetURX())
            self.m_xy_lims[1][0]    = min(self.m_xy_lims[1][0], rect.GetLLY())
            self.m_xy_lims[1][1]    = max(self.m_xy_lims[1][1], rect.GetURY())
            self.m_values_range[0]  = min(self.m_values_range[0], rect.GetValue())
            self.m_values_range[1]  = max(self.m_values_range[0], rect.GetValue())
        print(f'    x     : {self.m_xy_lims[0][0]} - {self.m_xy_lims[1][0]}')
        print(f'    y     : {self.m_xy_lims[0][1]} - {self.m_xy_lims[1][1]}')
        print(f'    value : {self.m_values_range[0]} - {self.m_values_range[1]}')
        print(f'# find xy lim end.')
    def PrintRects(self):
        print(f'# print rects start.')
        for rect in self.m_rects:
            print(f'{rect.GetLLX()} {rect.GetLLY()} {rect.GetURX()} {rect.GetURY()} {rect.GetValue()}')
        print(f'# print rects end.')
    def DrawRectsWithValue(self):
        values  = []
        for rect in self.m_rects:
            values.append(rect.GetValue())
        fig, ax = plt.subplots(1)
        plt.xlim(self.m_xy_lims[0])
        plt.ylim(self.m_xy_lims[1])
        normal  = plt.Normalize(self.m_values_range[0], self.m_values_range[1])
        cmap    = plt.cm.RdYlBu_r
        c       = cmap(values)
        i       = 0
        for rect in self.m_rects:
            t_rect  = plt.Rectangle((rect.GetLLX(), rect.GetLLY()), rect.GetWidth(), rect.GetHeight(), facecolor=c[i])
            ax.add_patch(t_rect)
            i   += 1
        cax, _  = cbar.make_axes(ax)
        cb2     = cbar.ColorbarBase(cax, cmap=cmap, norm=normal)
        plt.savefig(self.m_png_filename)
        plt.show()
    def DrawRectsWithoutValue(self):
        fig, ax = plt.subplots(1)
        plt.xlim(self.m_xy_lims[0])
        plt.ylim(self.m_xy_lims[1])
        for rect in self.m_rects:
            t_rect  = plt.Rectangle((rect.GetLLX(), rect.GetLLY()), rect.GetWidth(), rect.GetHeight())
            ax.add_patch(t_rect)
        plt.savefig(self.m_png_filename)
        plt.show()
    def DrawRects(self):
        if -1 == self.m_value_pos:
            self.DrawRectsWithoutValue()
        else:
            self.DrawRectsWithValue()
    def Run(self, args):
        self.ReadArgs(args)
        self.PrintInput()
        self.ReadFile()
        self.FindXYLim()
        self.PrintRects()
        self.DrawRects()

def main(args):
    my_plotbox  = Plotbox()
#    my_plotbox.Run(args)
#    test_args   = [ 'plotrect.py', 'test_w_value', './tests/test.txt', 1, 2, 3, 4, 5 ]
#    test_args   = [ 'plotrect.py', 'test_wo_value', './tests/test.txt', 1, 2, 3, 4 ]
#    my_plotbox.Run(test_args)

if __name__ == '__main__':
    main(sys.argv)
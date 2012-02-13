"""
Created on February 12, 2012

@author: sbobovyc
"""
"""   
    Copyright (C) 2012 Stanislav Bobovych

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import struct
import math
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import FontProperties
from collections import OrderedDict

type_dict = OrderedDict([("f","float"), ("d","double"), 
            ("b","signed char"), ("B","unsigned char"), 
            ("h","signed short"), ("H","unsigned short"), 
            ("i","signed int"), ("I","unsigned int"), 
            ("q","signed long long"), ("Q","unsigned long long")])
endian_dict = {"<":"little endian", ">":"big endian"}
type_list = type_dict.keys()
endian_list = endian_dict.keys()

def sliding_window_filter(file_pointer, count, filename="", file_offset=0x0, byte_order="<", type="f", abs_min=0.1, abs_max=20, verbose=False):    
    start_offset = file_offset
    file_pointer.seek(start_offset)
    total = 0
    values = []
    offsets = []
    print "File",filename
    print "File offset %s" % hex(file_offset).rstrip('L')
    for i in range(1,count):
        location = file_pointer.tell()
        bytes2read = 0
        if type == "f": bytes2read = 4
        if type == "d": bytes2read = 8
        if type == "b" or type == "B": bytes2read = 1
        if type == "h" or type == "H": bytes2read = 2
        if type == "i" or type == "I" or type == "l" or type == "L": bytes2read = 4
        if type == "q" or type == "Q": bytes2read = 8
        
        buffer = file_pointer.read(bytes2read)       
        try: 
            data, = struct.unpack("%s%s" % (byte_order, type), buffer)
        except Exception, e:
            print e
            print "Was only able to scan %i bytes" % i
            break
        
        if math.fabs(data) > abs_min and math.fabs(data) < abs_max:            
            if verbose: print i,hex(location).rstrip('L'),data
            total += 1
            values.append(data)
            offsets.append(location)
        file_pointer.seek(start_offset+i)
    print "Found %s %s %s in range (%s, %s)" % (total, endian_dict[byte_order], type_dict[type], abs_min, abs_max)
    print
    return values, offsets
        
def graph_file_data2(data, file_offset, byte_order, type, abs_min, abs_max, input_filename="", save=False, layer=False, show=True):
        ax = plt.subplot(111)
        CUMULATIVE = False
        if data != None and file_offset != None and byte_order != None and type != None:  
            # clear plot
            if not layer:
                plt.clf()                     
                ll = plt.plot(file_offset, data, label="%s %s" % (endian_dict[byte_order], type_dict[type]))
            if layer:
                ll = plt.plot(file_offset, data, label="%s%s %s" % (byte_order, type, input_filename))                      
            endianess = endian_dict[byte_order]
            data_type = type_dict[type]
        else:
            CUMULATIVE = True
            
        plt.xlabel("File offset")
        plt.ylabel("Value")
        majorFormatter = FormatStrFormatter('%X') # change to %d to see decimal offsets
        ax.xaxis.set_major_formatter(majorFormatter)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        plt.grid(True)
        if not layer:
            ax.set_title(input_filename)
            textstr = "%i data points\nData: %s %s\nFilter: abs_min=%0.3f, abs_max=%0.3f" % (len(data), endianess, data_type, abs_min, abs_max)
        if layer:
            textstr = "Filter: abs_min=%0.3f, abs_max=%0.3f" % (abs_min, abs_max)            
            ax.set_title("CUMULATIVE summary")
        if not layer:
            # Shrink current axis by 20%
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + 0.15, box.width, box.height * 0.8])
            ax.text(0.25, -0.15, textstr, transform=ax.transAxes, fontsize=14, horizontalalignment='left', verticalalignment='top', bbox=props)
        if layer:
            legend_font_props = FontProperties()
            legend_font_props.set_size('small')  
            ax.legend(loc='upper center', bbox_to_anchor=(0.95, 1.05), fancybox=True, shadow=True, prop=legend_font_props)
        if not layer and save and input_filename != "":
            plt.savefig(input_filename + "_%s_%s%s" % (endianess, data_type, ".png"))
        if layer and save and input_filename != "" and CUMULATIVE:
            plt.savefig(input_filename)
        if show:
            plt.show()

def graph_file_data(data, file_offset, byte_order, type, abs_min, abs_max, mode, input_filename="", save=False, show=True):
        fig = plt.figure()
        ax = fig.add_subplot(111)
            
        if mode == "SINGLE":
            ax.plot(file_offset, data, label="%s %s" % (endian_dict[byte_order], type_dict[type]))
        elif mode == "MULTIPLE":
            i = 0;
            print len(file_offset)
            print len(data)
            print len(byte_order)
            print len(type)
            for d in data:                   
                print byte_order[i], type[i]
                label = "%s %s" % (endian_dict[byte_order[i]], type_dict[type[i]])
                ax.plot(file_offset[i], d, label=label)
                i += 1
        elif mode == "CUMULATIVE":
            ax.plot(file_offset, data, label="%s%s %s" % (byte_order, type, input_filename))
        else:
            print "Error, wrong mode"
            return 
        
#        plt.savefig("1.png") #debug
        # axis format and labels, grid
        majorFormatter = FormatStrFormatter('%X') # change to %d to see decimal offsets
        ax.xaxis.set_major_formatter(majorFormatter)
        ax.set_xlabel("File offset")
        ax.set_ylabel("Value")
        ax.grid(True)
#        fig.savefig("2.png") #debug
        
        if mode == "SINGLE":
            endianess = endian_dict[byte_order]
            data_type = type_dict[type]
            textstr = "%i data points\nData: %s %s\nFilter: abs_min=%0.3f, abs_max=%0.3f" % (len(data), endianess, data_type, abs_min, abs_max)
            ax.set_title(input_filename)  
#            plt.savefig("3.png") #debug
        if mode == "MULTIPLE":
            textstr = "Filter: abs_min=%0.3f, abs_max=%0.3f" % (abs_min, abs_max)            
            ax.set_title(input_filename + " summary")          
        if mode == "CUMULATIVE":
            textstr = "Filter: abs_min=%0.3f, abs_max=%0.3f" % (abs_min, abs_max)            
            ax.set_title("CUMULATIVE summary")

        if mode == "MULTIPLE" or mode == "CUMULATIVE":
            legend_font_props = FontProperties()
            legend_font_props.set_size('small')  
            ax.legend(loc='upper center', bbox_to_anchor=(0.95, 1.05), fancybox=True, shadow=True, prop=legend_font_props)
            # Shrink current axis by 20%
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + 0.15, box.width, box.height * 0.8])
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax.text(0.25, -0.15, textstr, transform=ax.transAxes, fontsize=14, horizontalalignment='left', verticalalignment='top', bbox=props)
            
        if mode == "SINGLE" and input_filename != "":
            plt.savefig(input_filename + "_%s_%s%s" % (endianess, data_type, ".png"))
        if mode == "MULTIPLE" and input_filename != "":
            plt.savefig(input_filename + ".png")
        if mode == "CUMULATIVE":
            plt.savefig(input_filename)
        if show:
            plt.show()
                    
def graph_CUMULATIVE(input_filename, abs_min, abs_max):
    graph_file_data(None, None, None, None, abs_min, abs_max, input_filename=input_filename, save=True, layer=True, show=False)
    
def clear_graph():
    plt.clf()  
    
def file_scan(full_file_path, count, type_list=type_list, endian_list=endian_list, file_offset=0x0, abs_min=0.1, abs_max=20, verbose=False, mode="SINGLE", graph=False, save=False, show=False):
    value_list = []
    offsets_list = []
    e_list = []
    t_list = []
    for endianess in endian_list:
        for type in type_list:
            with open(full_file_path, "rb") as f:
                f.seek(file_offset)
                filename = os.path.basename(full_file_path)
                values, offsets = sliding_window_filter(f, count, filename=full_file_path, file_offset=file_offset, byte_order=endianess, type=type, abs_min=abs_min, abs_max=abs_max, verbose=verbose)
                if graph and mode == "SINGLE":
                    graph_file_data(values, offsets, endianess, type, abs_min, abs_max, input_filename=filename, mode=mode, save=save, show=show)
                if graph and mode == "MULTIPLE":
                    value_list.append(values)
                    offsets_list.append(offsets)
                    e_list.append(endianess)
                    t_list.append(type)
    if mode == "MULTIPLE":                
        graph_file_data(value_list, offsets_list, e_list, t_list, abs_min, abs_max, input_filename=filename, mode=mode, save=save, show=show)
    
if __name__ == "__main__":    
    path = "C:\\Users\\sbobovyc\\Desktop\\bia\\1.03\\bin_win32\weapons"
    file_list = os.listdir(path)
    for file in file_list:
        if file.endswith(".crf"):
            full_file_path = os.path.abspath(os.path.join(path, file)) 
            print full_file_path
            file_scan(full_file_path, 10000, type_list=('f','d'), file_offset=0x1c, mode="MULTIPLE", graph=True, save=True)
                    
#    graph_CUMULATIVE("CUMULATIVE_summary1.png", abs_min=0.1, abs_max=20.0)
#    
#    clear_graph()
#    
#    for file in file_list:
#        if file.endswith(".crf"):
#            full_file_path = os.path.abspath(os.path.join(path, file)) 
#            print full_file_path
#            file_scan(full_file_path, 10000, type_list=('f'), endian_list=('<'), file_offset=0x1c, graph=True, save=True, layer=True)
#    graph_CUMULATIVE("CUMULATIVE_summary2.png", abs_min=0.1, abs_max=20.0)
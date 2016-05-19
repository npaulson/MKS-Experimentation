import os
import numpy as np
import scipy.stats as ss
import sklearn.metrics as sm
import sys
import matplotlib.pyplot as plt
import vtk
import h5py

seq_colors = ["#543005", "#8c510a", "#bf812d", "#dfc27d", "#f6e8c3", "#f5f5f5", "#c7eae5", "#80cdc1", "#35978f", "#01665e", "#003c30"]
dif_colors = ["#a6cee3", "#b2df8a", "#e31a1c", "#ff7f00", "#6a3d9a", "#b15928", "#1f78b4",  "#fb9a99", "#fdbf6f", "#cab2d6", "#ffff99", "#33a02c"]

shapes = ["o", "^", "s", "D", ">", "<", "v", "*", "+", "x", "_", "p"]

pad_dist = 12
font_size = 12
tick_widths = 1
tick_lens = 5

def prettify_frame(ax):
    ax.tick_params(which='both', direction='out', pad=pad_dist*.75)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(tick_widths)
        ax.spines[axis].set_visible(True)
        ax.spines[axis].set_color('k')
    ax.xaxis.set_tick_params(which='major', width=tick_widths,length=tick_lens,color='k')
    ax.xaxis.set_tick_params(which='minor', width=tick_widths/2.0,length=tick_lens*.6,color='k')
    ax.yaxis.set_tick_params(which='major', width=tick_widths,length=tick_lens,color='k')
    ax.yaxis.set_tick_params(which='minor', width=tick_widths/2.0,length=tick_lens*.6,color='k')
    temp_list = [ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()
    for item in temp_list:
        item.set_fontsize(font_size)
        item.set_color("k")
    try:
        for item in ax.get_legend().get_texts():
            item.set_fontsize(font_size * .6)
            item.set_color("k")
    except:
        print("not doing legend text...")
    ax.set_frame_on(True)
    plt.tight_layout()

def plot_cdfs(data, names=None, min_pct=0, xlabel="", tail_len=None, colors=dif_colors):
    if names is None:
        names = [str(i) for i in range(len(data))]
    fig = plt.figure(facecolor="white", figsize=(6,4), dpi=300)
    ax = fig.add_subplot(111, axisbg='white')
    num_samples = 300
    for i, d in enumerate(data):
        if len(d) > 0:
            d = np.sort(d)
            d = d[int(len(d)*min_pct):]
            if len(d) > num_samples:
                indices = np.floor(np.linspace(0,len(d)-1, num_samples))
                indices = indices.astype(int)
                d = d[indices]
            # ys = -np.log(-np.log(np.linspace(min_pct+(1.0-min_pct)/len(d), 1, len(d))))
            ys = np.linspace(min_pct+(1.0-min_pct)/len(d), 1, len(d))
            color = colors[i % len(colors)]
            if len(names) == len(data):
                temp_name = names[i]
            else:
                temp_name = None
            plt.scatter(d,ys, c=color, label=temp_name)
    plt.ylabel("CDF")
    plt.xlabel(xlabel)
    plt.legend(loc='lower right')
    plt.locator_params(axis='x',nbins=6)
    prettify_frame(ax)
    return fig

def fit_gamma_robust(tail):
    r2s = []
    diff_stats = []
    s_f = 0.8
    for j in range(2):
        if j==0:
            stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.999)
        else:
            stats = ss.gamma.fit(tail, fa=s_f)
        x_old = np.linspace(np.min(tail), np.max(tail), 100)
        x = np.log(x_old)
                
        cdf = (np.arange(len(tail)) + 1)/ float(len(tail))
        pred_ys = ss.gamma.cdf(tail, *stats)
        tail_log = np.log(tail)
        
        r2 = sm.r2_score(pred_ys, cdf)
        temp_stats = (len(tail),) + stats + (r2,)
        r2s.append(r2)
        diff_stats.append(temp_stats)
    if r2s[0] > r2s[1]:
        return diff_stats[0][1:4]
    return diff_stats[1][1:4]

def fit_gen_EVDs(alldata):
    r2s = []
    diff_stats = []
    stats = ss.genextreme.fit(alldata)
    x_old = np.linspace(np.min(alldata), np.max(alldata), 100)
    x = np.log(x_old)
            
    cdf = (np.arange(len(alldata)) + 1)/ float(len(alldata))
    pred_ys = ss.gamma.cdf(alldata, *stats)
    tail_log = np.log(alldata)
    
#    r2 = sm.r2_score(pred_ys, cdf)
    r2 = 0.0
    temp_stats = (len(alldata),) + stats + (r2,)
    r2s.append(r2)
    diff_stats = temp_stats
    return diff_stats[1:4]    
            
def read_vtk_tensor(filename, tensor_id, comp):
    """
    Summary:
        Much of this code was taken from Matthew Priddy's example file.
    Inputs:
    Outputs:
    """

    # Initialize the reading of the VTK microstructure created by Dream3D
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(filename)
    reader.ReadAllTensorsOn()
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()
    data = reader.GetOutput()
    dim = data.GetDimensions()
    vec = list(dim)
    vec = [i-1 for i in dim]

    el = vec[0]

    # Calculate the total number of elements
    el_total = el**3

    meas = data.GetCellData().GetArray(reader.GetTensorsNameInFile(tensor_id))
    # if tensor_id == 0, we read the stress tensor
    # if tensor_id == 1, we read the strain tensor
    # if tensor_id == 2, we read the plastic strain tensor

    meas_py = np.zeros([el_total])
    for ii in xrange(el_total):
        meas_py[ii] = meas.GetValue(ii*9 + comp)

    return meas_py	

def read_vtk_scalar(filename, scalar_id):
    """
    Summary:
    Much of this code was taken from Matthew Priddy's example file.
    Inputs:
    Outputs:
    """
    
    # Initialize the reading of the VTK microstructure created by Dream3D
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(filename)
    reader.ReadAllTensorsOn()
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()
    data = reader.GetOutput()
    dim = data.GetDimensions()
    vec = list(dim)
    vec = [i-1 for i in dim]
    
    el = vec[0]
    
    # Calculate the total number of elements
    el_total = el**3
    
    Scalar = data.GetCellData().GetArray(reader.GetScalarsNameInFile(scalar_id))
    # if scalar_id == 0, we read the GrainID scalar
    # if scalar_id == 1, we read the Plastic Fatemi-Socie FIP scalar 
    # if scalar_id == 2, we read the Total Fatemi-Socie FIP scalar 
    # if scalar_id == 3, we read the Lamellar FIP scalar
    # if scalar_id == 4, we read the Findley Parameter scalar
    # if scalar_id == 5, we read the volume-averaged plastic FS FIP
    # if scalar_id == 6, we read the volume-averaged SS that results in a plastic FS FIP

    scalar_py = np.zeros([el_total])
    for ii in xrange(el_total):
        scalar_py[ii] = Scalar.GetValue(ii)
    
    return scalar_py	

if __name__ == "__main__":

    file_cpfem = 'Results_Ti64_Dream3D_XdirLoad_210microns_9261el_AbqInp_PowerLaw_1_data_v2_06.vtk'
    
    fip_cpfem = read_vtk_scalar(file_cpfem, 5)
    data = np.atleast_2d(fip_cpfem)

#    plot_cdfs(np.log(data), names=None, min_pct=0, xlabel="log(data)", tail_len=None, colors=dif_colors)
#    plt.show()
#    plot_cdfs(np.log(data), names=None, min_pct=0.99, xlabel="log(data)", tail_len=None, colors=dif_colors)
#    plt.show()
    
    data_sort = np.sort(data)
    data_tail = data_sort[:,int(len(data_sort[0,:])*0.99):]
    gamma_stats = fit_gamma_robust(data_tail.T)
    print gamma_stats
    gevd_stats = fit_gen_EVDs(data_sort.T)
    print gevd_stats
        
    plt.hold('on')
    h = plot_cdfs(np.log(data_tail), names=None, min_pct=0.0, xlabel="log(data_tail)", tail_len=None, colors=dif_colors)
    plt.plot(np.log(data_tail.T), ss.gamma.cdf(data_tail.T, gamma_stats[0], loc=gamma_stats[1], scale=gamma_stats[2]),'r-', lw=2, label='gamma cdf')
    plt.hold('off')
    plt.savefig('fit_gamma_tail.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', format='png',
        transparent=False, bbox_inches=None, pad_inches=0.05,
        frameon=None)
    plt.clf()
    plt.close()
    

    plt.hold('on')
    h = plot_cdfs(np.log(data_sort), names=None, min_pct=0.0, xlabel="log(data_all)", tail_len=None, colors=dif_colors)
    plt.plot(np.log(data_sort.T), ss.genextreme.cdf(data_sort.T, gevd_stats[0], loc=gevd_stats[1], scale=gevd_stats[2]),'r-', lw=2, label='general EVD cdf')
    plt.hold('off')
    plt.savefig('fit_gEVD_all.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', format='png',
        transparent=False, bbox_inches=None, pad_inches=0.05,
        frameon=None)
    plt.clf()
    plt.close()  
    
    
    
    
    
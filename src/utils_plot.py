import matplotlib as mpl
import matplotlib.pyplot as plt 
import numpy as np

max = lambda a,b:a if a > b else b
def plot_ordered_fc(matrix, matrix_label, suptitle, atlas, atlas_labels, c_map='viridis'):
    """
    matrix: matrix I want to plot
    matrix_label: label of the matrix

    """
    
    N_mat = len(matrix)

    N=int(atlas.max()) # Number of areas
    
    dic = {}
    for i,n in enumerate(atlas_labels['ROI_network'].unique()):
        dic[n] = i
    
    super_area_indx = [dic[a] for a in atlas_labels['ROI_network'].to_numpy()]
    super_area_indx = np.asarray(super_area_indx)
    
    alpha=1
    
    # Add an additional color for the first 16 elements
    colors = [
              mpl.colors.to_rgba('purple',alpha), #Attention
              mpl.colors.to_rgba('lightblue',alpha), #Auditive
              mpl.colors.to_rgba('green',alpha), #Control  
              mpl.colors.to_rgba('violet',alpha),#Default
              mpl.colors.to_rgba('yellow',alpha), #Language
              mpl.colors.to_rgba('orange',alpha), #Somatomotor
              mpl.colors.to_rgba('gray', alpha),  # Subcortical
              mpl.colors.to_rgba('red',alpha), #Visual
             ]
    
    n_bin = np.unique(list(atlas_labels['ROI_network'])).shape[0] # Increment number of bins
    cmap_name = 'my_list'
    cmap = mpl.colors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
    family = super_area_indx
        
    # Define your labels for each color
    labels = atlas_labels['ROI_network'].unique()
        
    vmin = np.min(matrix)
    vmax = np.min(matrix)
    vtot = max(vmax,abs(vmin))

    ### PLOT ###
    cmap_ = plt.get_cmap(c_map)
    fig, axs = plt.subplots(nrows=1, ncols=N_mat, figsize=(4*N_mat, 4))
    fig.suptitle(suptitle)
    for i in range(N_mat):
        if N_mat>1:
            ax = axs[i]
        else:
            ax = axs
        # Plot the matrix
        im = ax.imshow(matrix[i], vmin=-vtot, vmax=vtot, cmap=c_map)
        ax.set_title(matrix_label[i])
        ax.set_xticks([])
        ax.set_yticks([])
    
        # Plot the family color bar at the bottom of the matrix
        cax_bottom = ax.inset_axes([0, -0.03, 1, 0.05])  # adjust [left, bottom, width, height] as needed
        cax_bottom.imshow(family[np.newaxis, :], aspect='auto', cmap=cmap)
        cax_bottom.set_yticks([])
        cax_bottom.set_xticks([])
        
        # Set the boundaries to match your data
        boundaries = [0]  # start with 0
        
        # Add the boundary for the first color
        boundaries.append(16)
        
        # Add the boundaries for the rest of the colors
        for i in range(2, n_bin+1):
            boundaries.append(boundaries[-1] + 10)
        
        # Create a color bar legend with labels
        cax_legend = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # adjust [left, bottom, width, height] as needed
        norm = mpl.colors.BoundaryNorm(boundaries, cmap.N)
        cb = mpl.colorbar.ColorbarBase(cax_legend, cmap=cmap, norm=norm, 
                                       ticks=np.array(boundaries[:-1]) + np.diff(boundaries) / 2,  # set ticks at the middle of boundaries
                                       orientation='vertical')
    
        cb.set_ticklabels(labels, fontsize=15)  # set fontsize to desired value
            
        # Add common colorbar
        cbar_ax = fig.add_axes([0.0, 0.15, 0.01, 0.7]) # Adjust as necessary.
        fig.colorbar(im, cax=cbar_ax, orientation='vertical')
    
    return fig

def plot_array(array):
    x = [m for m in range(array.shape[0])]
    y = array
    
    fig, ax = plt.subplots(nrows=1, figsize=(1,5))
    
    extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
    ax.imshow(np.expand_dims(y, axis=1), cmap="plasma", aspect="auto", extent=extent)
    ax.set_yticks([])
    ax.set_xticks([])
    
    ax.set_xlim(extent[0], extent[1])
    plt.tight_layout()

    return _

def plot_arrays(arrays):
    fig, axs = plt.subplots(nrows=1,ncols=len(arrays), figsize=(4,5))
    for i,ax in enumerate(axs.flat):
        x = [m for m in range(arrays[i].shape[0])]
        y = arrays[i]
        
        
        extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
        ax.imshow(np.expand_dims(y, axis=1), cmap="plasma", aspect="auto", extent=extent)
        ax.set_yticks([])
        ax.set_xticks([])
        
        ax.set_xlim(extent[0], extent[1])
    plt.tight_layout()

    return _
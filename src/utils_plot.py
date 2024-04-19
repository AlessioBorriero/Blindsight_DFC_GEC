import matplotlib as mpl
import matplotlib.pyplot as plt 
import numpy as np

def plot_ordered_fc(matrix, matrix_label, atlas, atlas_labels, c_map='viridis'):
    """
    matricx: matrix I want to plot
    matrix_label: label of the matrix

    """

    N=int(atlas.max()) # Number of areas
    
    dic = {}
    for i,n in enumerate(np.unique(atlas_labels['super network'].to_numpy())):
        dic[n] = i
    
    super_area_indx = [dic[a] for a in atlas_labels['super network'].to_numpy()]
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
    
    n_bin = np.unique(list(atlas_labels['super network'])).shape[0] # Increment number of bins
    cmap_name = 'my_list'
    cmap = mpl.colors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
    family = super_area_indx
        
    # Define your labels for each color
    labels = ['ATT', 'AUD', 'CONT', 'DEF', 'LAN', 'SOM', 'SUB','VIS']
        
    vmin = matrix.min()
    vmax = matrix.max()
    vtot = max(vmax,abs(vmin))

    ### PLOT ###
    cmap_ = plt.get_cmap(c_map)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
    # Plot the matrix
    im = ax.imshow(matrix, vmin=-vtot, vmax=vtot, cmap='coolwarm')
    ax.set_title(matrix_label)
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
    cbar_ax = fig.add_axes([-0.05, 0.15, 0.01, 0.7]) # Adjust as necessary.
    fig.colorbar(im, cax=cbar_ax, orientation='vertical')

    return fig
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings

def plot_eui_diagram(est_eui, est_eui_min, est_eui_g, est_eui_m, est_eui_max, est_score, est_score_level, output_path):

	"""
	Plot the EUI diagram.
	=========================================================================================
	
	Arguments:

		est_eui (float): The estimated EUI of a building.

		est_eui_min (float): The minimum estimated EUI of a building.

		est_eui_g (float): The green building criteria estimated EUI of a building.

		est_eui_m (float): The median estimated EUI of a building.

		est_eui_max (float): The maximum estimated EUI of a building.

		est_score (float): The estimated score of a building.

		est_score_level (str): The estimated score level of a building.

		output_path (str): The path to save the output figure.
	"""

	# Turn off warnings
	warnings.filterwarnings('ignore')

	# Adjust est_eui if it is out of range
	if est_eui < est_eui_min:
		
		est_eui_plot = est_eui_min

	elif est_eui > est_eui_max:

		est_eui_plot = est_eui_max

	else:

		est_eui_plot = est_eui

	# Generate curve
	y0 = np.random.rayleigh(size=200000)
	y = y0 * (est_eui_max - est_eui_min)/(np.max(y0) - np.min(y0)) + est_eui_min

	# Plot and set size
	s = sns.displot(y, kind='kde', color = 'black', linewidth=2)
	s.fig.set_figwidth(12)
	s.fig.set_figheight(6)

	# Add lines
	plt.axvline(est_eui_min, color='b', linestyle='--', linewidth = 3, alpha=0.5)
	plt.axvline(est_eui_max, color='b', linestyle='--', linewidth = 3, alpha=0.5)
	plt.axvline(est_eui_plot, color='r', linestyle='--', linewidth = 3, alpha=0.5)
	plt.axvline(est_eui_g, color='b', linestyle='--', linewidth = 3, alpha=0.5)
	plt.axhline(0, color='black', linewidth = 5)
	plt.xlim([est_eui_min-0.1, est_eui_max+0.1])

	# Get ylim
	ylim = plt.gca().get_ylim()
	plt.ylim([ylim[0], ylim[1]*1.5])

	# Add text
	plt.text(est_eui_min, 0.02, 'EUI min\n%.2f'%(est_eui_min), fontsize=16, horizontalalignment='center', weight='bold')
	plt.text(est_eui_max, 0.02, 'EUI max\n%.2f'%(est_eui_max), fontsize=16, horizontalalignment='center', weight='bold')
	plt.text(est_eui_g, 0.02, 'EUI g\n%.2f'%(est_eui_g), fontsize=16, horizontalalignment='center', weight='bold')
	plt.text(est_eui_plot, 0.03, 'EUI\n%.2f'%(est_eui), fontsize=16, horizontalalignment='center', weight='bold', bbox=dict(facecolor='white', edgecolor='red', alpha = 0.8, pad = 3.0))

	# No grid
	plt.grid(False)
	plt.box(False)

	# Add labels and ticks
	eui_list= [est_eui_g - (est_eui_g - est_eui_min) * ((5-i)/5) for i in range(6)]
	eui_list += [est_eui_g + (est_eui_max - est_eui_g) * ((i*2+1)/5) for i in range(3)]
	plt.xticks(eui_list, ['100','90','80','70','60','50','40','20','0'], fontsize=14)
	plt.xlabel('Score', fontsize=20)
	plt.yticks([])
	plt.ylabel('')

	# Add filled color and text
	color = sns.color_palette("rainbow", 8)
	text = ['1+','1','2','3','4','5','6','7']
	[plt.axvspan(eui_list[i],eui_list[i+1],alpha=0.2, color=color[i]) for i in range(8)]
	[plt.text((eui_list[i]+eui_list[i+1])/2, 0.01, text[i], fontsize=16, horizontalalignment='center', color = 'grey') for i in range(8)]

	# Add score and level
	plt.annotate('Score:%.2f\nLevel:%s'%(est_score, est_score_level), xy=(est_eui, 0.03*1.3), xytext=(est_eui_plot, 0.04*1.3), fontsize=16, horizontalalignment='center', weight='bold', arrowprops=dict(facecolor='grey', shrink=0.05), bbox=dict(facecolor='white', edgecolor='lightgrey', alpha = 0.8, pad = 3.0))

	# Save figure

	plt.savefig(output_path + 'eui_diagram.png', dpi=300, bbox_inches='tight')

	return None
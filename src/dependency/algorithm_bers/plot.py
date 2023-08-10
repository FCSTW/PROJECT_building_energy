import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

def calc_eui_interpolation(eui_g, **kwargs) -> (float, float):

	"""
	Calculate the EUI interpolation.
	If only the eui_min is provided (in estimation system BERSe), the eui_n will be calculated.
	If only the eui_n is provided (in estimation system R-BERS), the eui_min will be calculated.
	=========================================================================================

	Arguments:

		eui_g (float): The green building criteria estimated simulated EUI of a building.

		kwargs: The keyword arguments to calculate the EUI interpolation.

	Output:

		eui_g (float): The green building criteria estimated simulated EUI of a building.

		eui_min (float): The minimum EUI in the interpolation.

		eui_n (float): The EUI at the neutral point in the interpolation.
	"""

	if (kwargs.get('eui_min') is not None) and (kwargs.get('eui_n') is None):

		eui_min = kwargs.get('eui_min')
		eui_n   = eui_min + (eui_g - eui_min) * 0.2

	elif (kwargs.get('eui_min') is None) and (kwargs.get('eui_n') is not None):

		eui_n   = kwargs.get('eui_n')
		eui_min = eui_n - (eui_g - eui_n) * 0.25
	
	else:

		raise ValueError('Only one of eui_min and eui_n should be provided.')
	
	return eui_g, eui_min, eui_n

def calc_eui_curve(x_min: float, x_max: float, n_x: int) -> (np.ndarray, np.ndarray):

	"""
	Calculate the EUI curve.
	=========================================================================================

	Arguments:

		x_min (float): The minimum EUI in the interpolation.

		x_max (float): The maximum EUI in the interpolation.

		n_x (int): The number of points in the interpolation.

	Output:

		x (np.ndarray): The x of EUI curve.

		y (np.ndarray): The y of EUI curve.
	"""

	# Parameters of the skew normal distribution
	a = 3
	loc = 2
	scale = 1
	
	# Generate curve
	x_ske = np.linspace(
		scipy.stats.skewnorm.ppf(0.01, a, loc=loc, scale=scale),
        scipy.stats.skewnorm.ppf(0.99, a, loc=loc, scale=scale),
		n_x,
	)

	y = scipy.stats.skewnorm.pdf(x_ske, a, loc=loc, scale=scale)
	x = np.linspace(x_min, x_max, n_x)

	return x, y

def plot_eui_diagram(output_path, **kwargs):

	"""
	Plot the EUI diagram.
	=========================================================================================
	
	Arguments:

		output_path (str): The path to save the output figure.

		kwargs: The keyword arguments to plot the EUI diagram.

	Output:

		None
	"""

	# Turn off warnings
	warnings.filterwarnings('ignore')

	# Get kwargs
	est_eui         = kwargs.get('est_eui')
	est_eui_n       = kwargs.get('est_eui_n')
	est_eui_min     = kwargs.get('est_eui_min')
	est_eui_max     = kwargs.get('est_eui_max')
	est_eui_g       = kwargs.get('est_eui_g')
	est_score       = kwargs.get('est_score')
	est_score_level = kwargs.get('est_score_level')

	est_eui_g, est_eui_min, est_eui_n = calc_eui_interpolation(est_eui_g, eui_min=est_eui_min, eui_n=est_eui_n)

	# Adjust est_eui if it is out of range [est_eui_min, est_eui_max]
	est_eui_plot = min(max(est_eui, est_eui_min), est_eui_max)

	# Generate curve
	eui_curve_x, eui_curve_y = calc_eui_curve(est_eui_min, est_eui_max, 100)

	# =========================================================================================
	# 
	# Plot
	# 
	# =========================================================================================

	# Create figure object
	fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

	# Plot and set size
	ax.plot(eui_curve_x, eui_curve_y, 'black', linewidth=2)

	# Add lines
	ax.axvline(est_eui_min, color='b', linestyle='--', linewidth = 3, alpha=0.5)
	ax.axvline(est_eui_n, color='b', linestyle='--', linewidth = 3, alpha=0.5)
	ax.axvline(est_eui_max, color='b', linestyle='--', linewidth = 3, alpha=0.5)
	ax.axvline(est_eui_plot, color='r', linestyle='--', linewidth = 3, alpha=0.5)
	ax.axvline(est_eui_g, color='b', linestyle='--', linewidth = 3, alpha=0.5)
	ax.axhline(0, color='black', linewidth = 5)
	ax.set_xlim([est_eui_min-0.1, est_eui_max+0.1])

	# Get ylim
	ylim = plt.gca().get_ylim()
	ax.set_ylim([ylim[0], ylim[1]*1.5])

	# Add text
	ax.text(est_eui_min, ylim[1]*0.25, 'EUI min\n%.2f'%(est_eui_min), fontsize=16, horizontalalignment='center', weight='bold')
	ax.text(est_eui_n, ylim[1]*0.50, 'EUI n\n%.2f'%(est_eui_n), fontsize=16, horizontalalignment='center', weight='bold')
	ax.text(est_eui_max, ylim[1]*0.25, 'EUI max\n%.2f'%(est_eui_max), fontsize=16, horizontalalignment='center', weight='bold')
	ax.text(est_eui_g, ylim[1]*0.25, 'EUI g\n%.2f'%(est_eui_g), fontsize=16, horizontalalignment='center', weight='bold')
	ax.text(est_eui_plot, ylim[1]*0.75, 'EUI\n%.2f'%(est_eui), fontsize=16, horizontalalignment='center', weight='bold', bbox=dict(facecolor='white', edgecolor='red', alpha = 0.8, pad = 3.0))

	# No grid
	ax.grid(False)

	# Add labels and ticks
	eui_list= [est_eui_g - (est_eui_g - est_eui_min) * ((5-i)/5) for i in range(6)]
	eui_list += [est_eui_g + (est_eui_max - est_eui_g) * ((i*2+1)/5) for i in range(3)]
	ax.set_xticks(eui_list, ['100','90','80','70','60','50','40','20','0'], fontsize=14)
	ax.set_xlabel('Score', fontsize=20)
	ax.set_yticks([])
	ax.set_ylabel('')

	# Add filled color and text
	color = sns.color_palette("rainbow", 8)
	text = ['1+','1','2','3','4','5','6','7']
	[plt.axvspan(eui_list[i],eui_list[i+1],alpha=0.2, color=color[i]) for i in range(8)]
	[plt.text((eui_list[i]+eui_list[i+1])/2, 0.01, text[i], fontsize=16, horizontalalignment='center', color = 'grey') for i in range(8)]

	# Add score and level
	ax.annotate('Score:%.2f\nLevel:%s'%(est_score, est_score_level), xy=(est_eui, 0.03*1.3), xytext=(est_eui_plot, 0.04*1.3), fontsize=16, horizontalalignment='center', weight='bold', arrowprops=dict(facecolor='grey', shrink=0.05), bbox=dict(facecolor='white', edgecolor='lightgrey', alpha = 0.8, pad = 3.0))

	# Save figure
	plt.savefig(output_path + 'eui_diagram.png', dpi=300, bbox_inches='tight')

	return None

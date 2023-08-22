import flask
import webbrowser
import json
import os
import datetime
import src.main

# Initialization
app = flask.Flask(__name__)

def output_json(obj, file_name):

	"""
	Output the input data to a JSON file.
	=========================================================================================

	Arguments:

		obj (dict): The input data

		file_name (str): The name of the output file

	Returns:

		None
	"""

	with open('input/building_config/{file_name}'.format(file_name=file_name), 'w') as outfile: 
		
		json.dump(obj, outfile, indent=4)
	
	return

@app.route("/app/")
def page_main():

	return flask.render_template('main.html')

@app.route("/app/<estimation_system>", methods=['GET', 'POST'])
def page_estimation_form(estimation_system=None):

	# If the argument is not specified, render the main page
	if (estimation_system is None):
		
		return flask.render_template('estimation_form.html', estimation_system=estimation_system)
	
	# If the user has submitted the form, output the data to a JSON file. Otherwise, render the main page.
	if (flask.request.method == 'POST'):

		# Output the data to a JSON file
		file_name = 'building_config.{estimation_system}.{building_name}.{datetime}.json'.format(
			estimation_system=flask.request.form['estimation_system'],
			building_name=flask.request.form['building_name'],
			datetime=datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
		)
		output_json(flask.request.form.to_dict(flat=False), file_name)

		# Call src/main.py to start the estimation
		if (flask.request.form['estimation_system'] == 'BERSe'):
			
			src.main.run_estimate_berse(file_name)

		elif (flask.request.form['estimation_system'] == 'R-BERS'):

			src.main.run_estimate_rbers(file_name)

		return flask.redirect(flask.url_for('page_result', file='.'.join(file_name.split('.')[1:-1])))

	else:

		return flask.render_template('estimation_{}.html'.format(estimation_system))

@app.route('/app/recalculate/<file>/', methods=['GET', 'POST'])
def page_recalculate(file=None):

	# If the argument is not specified, render the main page
	if (file is None): return flask.redirect(flask.url_for('page_main'))

	# Call src/main.py to start the estimation
	if (file.split('.')[0] == 'BERSe'):

		src.main.run_estimate_berse('building_config.{}.json'.format(file))

	elif (file.split('.')[0] == 'R-BERS'):

		src.main.run_estimate_rbers('building_config.{}.json'.format(file))

	return flask.redirect(flask.url_for('page_result', file=file))

@app.route('/app/result/', defaults={'file': None})
@app.route('/app/result/<file>/', methods=['GET', 'POST'])
def page_result(file=None):

	if (file is None):
		# If the file name is not specified, render the main page and list all the output files

		file_list              = os.listdir('./output/')
		name_list              = [file.split('.')[1] for file in file_list]

		return flask.render_template(
			'result.html',
			file_list=file_list,
			name_list=name_list,
			data=None,
			eui_diagram=None
		)

	else:
		
		# If the file name is specified, render the result page

		# Read the output JSON file
		with open('output/{file}/estimation_result.json'.format(file=file), 'rb') as infile: data = json.load(infile)

		# Convert all the numbers in the data to float
		for key in data.keys():

			if isinstance(data[key], float):

				data[key] = round(float(data[key]))
		
		# Create string for output
		data_string = \
			'估計 EUI: {est_eui} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度淨零基準 EUI: {est_eui_n} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度最低 EUI: {est_eui_min} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度綠建築 EUI: {est_eui_g} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度中位數 EUI: {est_eui_m} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度最高 EUI: {est_eui_max} kWh/(m<sup>2</sup>year) <br>' \
			'能耗得分: {est_score} 分（{est_score_level} 級）'
		
		data_string = data_string.format(
			est_eui=data['est_eui'],
			est_eui_n=data['est_eui_n'],
			est_eui_min=data['est_eui_min'],
			est_eui_g=data['est_eui_g'],
			est_eui_m=data['est_eui_m'],
			est_eui_max=data['est_eui_max'],
			est_score=data['est_score'],
			est_score_level=data['est_score_level']
		)

		return flask.render_template('result.html', file=file, data=data_string)

@app.route('/send_file/<file>')
def send_file_output(file):

	return flask.send_from_directory('./output/{file}/'.format(file=file), 'eui_diagram.png')

if (__name__ == '__main__'):
	
	# Open the web browser
	#webbrowser.open('http://127.0.0.1:5000/app/')

	# Run the app
	app.debug = True
	app.run()
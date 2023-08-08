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

@app.route("/app/", methods=['GET', 'POST'])
def page_main():
	
	# If the user has submitted the form, output the data to a JSON file. Otherwise, render the main page.
	if (flask.request.method == 'POST'):

		# Output the data to a JSON file
		file_name = 'building_config.{building_name}.{datetime}.json'.format(building_name=flask.request.form['building_name'], datetime=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
		output_json(flask.request.form.to_dict(flat=False), file_name)

		# Call main() in the src/main.py to start the estimation
		src.main.estimate(file=file_name)

		return flask.redirect(flask.url_for('page_result', file='.'.join(file_name.split('.')[1:3])))

	else:

		return flask.render_template('main.html')

@app.route('/app/recalculate/<file>', methods=['GET', 'POST'])
def page_recalculate(file=None):

	# If the argument is not specified, render the main page
	if (file is None): return flask.redirect(flask.url_for('page_main'))

	src.main.estimate(file='building_config.{}.json'.format(file))

	return flask.redirect(flask.url_for('page_result', file=file))

@app.route('/app/result/', defaults={'file': None})
@app.route('/app/result/<file>', methods=['GET', 'POST'])
def page_result(file):

	if (file is None):
		# If the file name is not specified, render the main page and list all the output files

		file_list = os.listdir('./output/')
		name_list = [file.split('.')[0] for file in file_list]

		return flask.render_template('result.html', file_list=file_list, name_list=name_list, data=None, eui_diagram=None)

	else:
		# If the file name is specified, render the result page

		# Read the output JSON file
		with open('output/{file}/estimation_result.json'.format(file=file), 'rb') as infile:  data = json.load(infile)

		data_string = \
			'估計 EUI: {est_eui} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度最低 EUI: {est_eui_min} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度綠建築 EUI: {est_eui_g} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度中位數 EUI: {est_eui_m} kWh/(m<sup>2</sup>year) <br>' \
			'估計尺度最高 EUI: {est_eui_max} kWh/(m<sup>2</sup>year) <br>' \
			'能耗得分: {est_score} 分（{est_score_level} 級）'
		
		data_string = data_string.format(
			est_eui=round(float(data['est_eui']), 2),
			est_eui_min=round(float(data['est_eui_min']), 2),
			est_eui_g=round(float(data['est_eui_g']), 2),
			est_eui_m=round(float(data['est_eui_m']), 2),
			est_eui_max=round(float(data['est_eui_max']), 2),
			est_score=round(float(data['est_score']), 2),
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
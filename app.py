import flask
import webbrowser
import json
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

	src.main.main_script(file='building_config.FCS.20230727121136.json')
	quit()

	# If the user has submitted the form, output the data to a JSON file. Otherwise, render the main page.
	if (flask.request.method == 'POST'):

		# Output the data to a JSON file
		file_name = 'building_config.{building_name}.{datetime}.json'.format(building_name=flask.request.form['building_name'], datetime=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
		output_json(flask.request.form.to_dict(flat=False), file_name)

		# Call main() in the src/main.py to start the estimation
		result = src.main.main_script(file=file_name)

		return flask.render_template('result.html')

	else:

		return flask.render_template('main.html')

@app.route("/app/result/", methods=['GET', 'POST'])
def page_result():

	return flask.render_template('result.html')

if (__name__ == '__main__'):
	
	# Open the web browser
	#webbrowser.open('http://127.0.0.1:5000/app/')

	# Run the app
	app.debug = True
	app.run()
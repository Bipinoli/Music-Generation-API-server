from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

import music_generator as musicGen
import utility as util
import configuration as config
import chord_model

from keras.models import load_model
import tensorflow as tf

import sheet_music
import midi2mp3

app = Flask(__name__)
CORS(app)



@app.route("/")
def home():
    api_endpoints = ""
    api_endpoints += "GET:  /api/v1/information/keyNames<br>"
    api_endpoints += "GET:  /api/v1/information/instruments<br>"
    api_endpoints += "GET:  /api/v1/information/genre<br>"
    api_endpoints += "GET:  /api/v1/information/all<br>"
    api_endpoints += "POST:  /api/v1/generate<br>"
    api_endpoints += "POST:  /api/v1/modify<br>"
    api_endpoints += "GET:  /api/v1/sheet_music/<name><br>"
    api_endpoints += "GET:   /api/v1/music_mp3<br>"

    return api_endpoints


@app.route("/api/v1/information/keyNames")
def getKeyNames():
    return jsonify({"keys": util.getKeyNames()})


@app.route("/api/v1/information/instruments")
def getInstruments():
    return jsonify(util.getInstruments())


@app.route("/api/v1/information/genre")
def getGenreNames():
    return jsonify(util.getSeedGenreNames())


@app.route("/api/v1/information/all")
def getAllInformation():
    return jsonify(
        {
            "keys": util.getKeyNames(),
            "genre": util.getSeedGenreNames(),
            "instruments": util.getInstruments(),
        }
    )


@app.route("/api/v1/generate", methods=["POST"])
def generate_music():
    '''
    eg: post body (json)
        parameters = {
            "genre_id": 2, # -optional
            "instrument_id": 3, # -optional
            "num_bars": 64, # number of bars of the generated music
            "BPM": 100, # pace of the music
            "chord_temperature": 1, # let it be in the range 0.1 to 2
            "seed_length": 4, # number of bars to seed with

            "note_cap" = 5, # how many notes can be played together at the same time
                    # it may not be accurate due to chords alongside melody
                    # it not provided default will be 4

            # following must come together
            "key": "C", # -optional # key of the generated music
            "octave_type": "lower", # -optional # (lower, higher) ?
            "which_octave": 2, # -optional # lower octave by 2
        }
    '''
    # parameters passed as the json body in POST req
    parameters = request.get_json()
    # return jsonify(musicGen.generate(parameters))
    return send_file(musicGen.generate(parameters), mimetype ="audio/midi")



@app.route("/api/v1/modify", methods=["POST"])
def modify_music():
    '''
    eg:
    post body(json): {
        "key": "C#",
        "octave_type": "lower",
        "which_octave": 2
    }
    for lower which octave can be upto: 2
    for higher which octave can be upto: 3
    '''
    modify_by = request.get_json()
    musicGen.modify_generated_music(modify_by)

    # return musicGen.get_music_to_return()
    return send_file(musicGen.get_music_to_return(), mimetype ="audio/midi")


@app.route("/api/v1/sheet_music/<name>")
def get_sheet_music(name):
    if name in ["png", "pdf"]:
        filepath =  sheet_music.generate_sheet_music(musicGen.get_music_to_return(), name)
    else:
        filepath =  sheet_music.generate_sheet_music(musicGen.get_music_to_return())
    if filepath:
        return send_file(filepath, mimetype="application/pdf")
    else:
        return "failed to do so!", 404


@app.route("/api/v1/music_mp3")
def get_mp3_music():
    mp3_path = midi2mp3.make_mp3()
    return send_file(mp3_path, mimetype="audio/mpeg")


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host= '0.0.0.0', debug=True)
	#app.run("192.168.0.48", port=5000, debug=True)

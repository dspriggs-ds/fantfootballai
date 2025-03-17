from dotenv import load_dotenv, dotenv_values 
from flask_bootstrap import Bootstrap5, SwitchField
from flask import Flask, render_template
from flask_wtf import FlaskForm
from openai import AzureOpenAI
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired
import data
import openai
import json
import markdown
import nfl_data_py as nfl
import numpy as np
import os
import pandas as pd


app = Flask(__name__) 
app.secret_key = 
bootstrap = Bootstrap5(app)

class fantballForm(FlaskForm):
    week_list = [i for i in range(1,19)]
    players_df = data.get_players()
    players_list = [(g.gsis_id, g.display_name) for g in players_df.itertuples()]
    weeklist = SelectField(u'Season Week', choices = week_list, validators = [InputRequired()])
    playerslist = SelectField(u'Player', choices = players_list, validators = [InputRequired()])
    submit = SubmitField('Submit')



@app.route("/", methods=['GET', 'POST'])
def home():
    form = fantballForm()
 
    if form.validate_on_submit():
        week = form.weeklist.data
        player_id =form.playerslist.data
        player_name = data.get_player_name(player_id)
        ret_value = markdown.markdown(data.get_analsysis(player_id, player_name, week))
        return render_template('display.html',analysis_text=ret_value)
    
    return render_template('index.html', form=form,title='Fantasy Football Analysis') 

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html',title='About')

if __name__ == '__main__': 
    app.run() 

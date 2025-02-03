from datetime import datetime
from dotenv import load_dotenv, dotenv_values 
from openai import AzureOpenAI
import nfl_data_py as nfl
import openai
import os



def get_players():
    player_df = nfl.import_players()
    player_df = player_df[player_df['status']=='ACT']
    player_df = player_df[['display_name','gsis_id']]
    player_df = player_df.sort_values(by='display_name')
    player_df = player_df.reset_index(drop=True)
    return player_df

def get_player_name(player_id):
    player_df = nfl.import_players()
    player_df = player_df[player_df['gsis_id']==player_id]
    player_name = player_df['display_name'].values[0]
    return player_name

def get_analsysis(player_id, player_name,week):
    load_dotenv() 
    openaiurl = os.getenv('openaiendpoint')
    openaikey = os.getenv('openaikey')

    openai.api_type= "azure"
    openai.api_key = openaikey
    openai.base_url = openaiurl
  

    
    client = AzureOpenAI(
        api_key=openaikey,
        azure_endpoint=openaiurl,
        api_version="2024-08-01-preview"
    )
    
    # Create the list of seasons to download
    end_year = datetime.now().year
    start_year = end_year - 5

    year_season=[i for i in range(start_year,end_year)]
    


    teams_df = nfl.import_team_desc()
    weekly_data = nfl.import_weekly_data(year_season)

    drop_columns=['fantasy_points', 'fantasy_points_ppr','headshot_url']
    weekly_data = weekly_data.drop(drop_columns,axis=1)
    weekly_data=weekly_data[weekly_data['player_id']==  player_id]

 
    content = weekly_data.to_json(orient="records")

    prompt = "Provide Fantasy Football Analysis for {0} and Fantasy Football predicted score for Week {1} for the season {2} using the attached data in json format".format(player_name,week,end_year)

    response = client.chat.completions.create(
        model="fantfootball",
        messages=[
            {
                "role": "system", 
                "content": "You are a Fantasy Football expert."
            },
            {
                "role": "user",
                "content": content+"\n\n"+prompt,
            },
        ],
    )
    return response.choices[0].message.content  


# player_id = '00-0034796'
# player_name = get_player_name(player_id)
# week = 17
# retvalue = get_analsysis(player_id, player_name,week)
# print(retvalue)
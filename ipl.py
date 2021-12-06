import streamlit as st
import pickle
import pandas as pd


teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('predpipe.pkl','rb'))
st.title('IPL Match Predictor App')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Batting Team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Bowling Team',sorted(teams))

city = st.selectbox('Place of Match (Venue)',sorted(cities))

target = st.number_input('Target Score')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score')
with col4:
    overs = st.number_input('Overs Bowled')
with col5:
    wkt_fall = st.number_input('Wickets Fallen')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wkt_left = 10 - wkt_fall
    c_run = score/overs
    rq_run = (runs_left*6)/balls_left

    final_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[city],'runs_reqd':[runs_left],'balls_rem':[balls_left],'wkts_left':[wkt_left],'target_score':[target],'c_runrate':[c_run],'r_runrate':[rq_run]})

    result = pipe.predict_proba(final_df)
    loss_perc = result[0][0]
    win_perc = result[0][1]
    st.header(batting_team + ": " + str(round(win_perc*100)) + "%")
    st.header(bowling_team + ": " + str(round(loss_perc*100)) + "%")
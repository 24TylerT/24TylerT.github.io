from email.mime import image
from flask import Blueprint, render_template, request, flash, redirect, session, url_for, Response
from .models import Scout
from . import db
import csv
from io import BytesIO
import base64
#import tbapy
import tbapy
import requests
import qrcode
import qrcode.image.svg
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

#tba = tbapy.TBA(
# 'h39XHSEqXkc59WvXY0lteYagmwOzWD0wmLV2CxZulOMcB89YIHFUIczJxvGTtM6X')
tba_key = 'w9Rg74721yfHACYNd4iGm9BCrJ9lZyyGERyCFjdRau0u17TPapeNRJyMLlliCRuB'
tba = tbapy.TBA(tba_key)
event_key = '2024bcvi'
api_url = 'https://www.thebluealliance.com/api/v3/event/' + event_key + '/teams/simple'
headers = {'X-TBA-Auth-Key': tba_key}
response = requests.get(api_url, headers=headers)
if response.status_code == 200:
  # Parse the JSON response
  teams = response.json()

  # Extract team numbers
  all_teams = [team['team_number'] for team in teams]
  all_teams.insert(0, "N/A")
"""
#round = "2023bcvi_qm" + Scout.round
#print(round)
#all_teams_simple = tba.event_teams(round, "simple")
all_teams_simple = tba.event_teams(event_key, "simple")
all_teams = []
for i in range(len(all_teams_simple)):
  all_teams.append(all_teams_simple[i]['team_number'])
"""

auth = Blueprint('auth', __name__)

img = qrcode.make('https://frc-raidzero-2023-scout-website.24tylert.repl.co',
                  image_factory=qrcode.image.svg.SvgImage)
with open('website/static/qr.svg', 'wb') as qr:
  img.save(qr)

# Setup for Google Sheets editing
scope = [
  'https://spreadsheets.google.com/feeds',
  'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file('credentials.json',
                                                    scopes=scope)

client = gspread.authorize(credentials)

document = client.open_by_url(
  "https://docs.google.com/spreadsheets/d/1T77nDpB7DKlAXHmskB2xBjXooPWVs0I4o0fRhWeUXv8/edit#gid=0"
)
sheet = document.sheet1


def get_next_blank_row(sheet):
  values_list = sheet.get_all_values()
  return len(values_list) + 1


def update_google_sheet(data):
  split_data = data.split('@')
  if (split_data[0]!="placeholder data"):
    split_data[0] = int(split_data[0])

  for piece in split_data:
    # Check for duplicates
    values_list = sheet.get_all_values()
    is_duplicate = False

    for row in values_list:
      if piece in row:
        is_duplicate = True
        break

    if not is_duplicate:
      sheet.append_row(split_data)

  return split_data


def set_averages(column_to_update, column_to_average, split_data):

  avg_points = 0
  total_points = 0
  team_frequency = 0
  row_num = 0
  rows_to_update = []
  
  team_number_values = sheet.col_values(3)
  team_number_values = team_number_values[2:]
  point_values = sheet.col_values(column_to_average)
  point_values = point_values[2:]

  if len(split_data) > 3:
    print(split_data[2])
    for i in team_number_values:
      if i==split_data[2]:
        rows_to_update.append(row_num+3)
        team_frequency+=1
        total_points += int(point_values[row_num])
      row_num+=1

    avg_points = round(total_points/team_frequency, 2)

    for i in rows_to_update:
      sheet.update_acell(column_to_update+(str(i)), avg_points)
  return

def sort_google_sheets():
  values_list = sheet.get_all_values()
  num_rows = len(values_list)
  num_cols = len(values_list[0])
  bottom_right_cell = gspread.utils.rowcol_to_a1(num_rows, num_cols)
  sheet.sort((1, 'asc'), range=('A3:'+bottom_right_cell))
  return
      

@auth.route('/')
@auth.route('/home')
def home():
  return render_template('home.html')


# Scout
"""
@auth.route('/qrcode')
def generateqr():
  return render_template('qrcode.html')
"""

# Data


@auth.route('/data', methods=['GET', 'POST'])
def data():
  # Show all the scouting data
  #data = Scout.query.order_by(Scout.team).all()
  #data =  Scout.query.filter(Scout.round.in_(['05', '64034'])).all()
  data = Scout.query.all()
  print(len(data))

  # Search teams
  if request.method == 'POST':
    searched_team = request.form.get('searched_team')
    data = Scout.query.filter_by(team=searched_team).all()

  return render_template('data.html', data=data)


# Scouting


@auth.route('/scout', methods=['GET', 'POST'])
def attempt():
  image_data = ""
  compressed_data = "placeholder data"
  if request.method == 'POST':
    regional = request.form.get('regional')
    round = request.form.get('round')
    alliance = request.form.get('alliance')
    
    #TEAM 1
    team = request.form.get('team')

    # Auton
    starting_pos = request.form.get('starting_pos')

    auton_amp = request.form.get('auton_amp')
    auton_speaker = request.form.get('auton_speaker')
    auton_community = request.form.get('auton_community')
   
    # Teleop
    tele_amp = request.form.get('tele_amp')
    tele_speaker = request.form.get('tele_speaker')
    tele_melody = request.form.get('tele_melody')
    amplified= request.form.get('amplified')

    # EndGame
    coopertition = request.form.get('coopertition')

    #Overall Performance
    stage = request.form.get('stage')
    spotlight = request.form.get('spotlight')
    harmonize = request.form.get('harmonize')
    role = request.form.get('role')
    game_piece = request.form.get('game_piece')
    
    tier = request.form.get('tier')
    notes = request.form.get('notes')

    

    new_scout = Scout(
      regional = regional,
      round=round,
      alliance=alliance,
      
      #Team 1
      team=team,
      starting_pos=starting_pos,
      auton_amp = auton_amp,
      auton_speaker = auton_speaker,
      auton_community=auton_community,
      tele_amp=tele_amp,
      tele_speaker=tele_speaker,
      tele_melody=tele_melody,
      amplified = amplified ,
      coopertition = coopertition,
      stage = stage,
      spotlight =spotlight,
      harmonize=harmonize,
      role = role,
      game_piece = game_piece,
      tier = tier,
      notes=notes)

    try:
      db.session.add(new_scout)
      Scout.query.all()
      #Scout.query.filter(Scout.round.in_(['05', '64034', '30'])).all()
    except:
      db.session.rollback()
    else:
      try:
        db.session.commit()
      except:
        db.session.rollback()
        db.session.commit()

    # Store it as csv
    with open(r'website/static/data.csv', 'w') as s_key:
      csv_out = csv.writer(s_key)

      # Horizontal labels
      csv_out.writerow([
        "Regional","Team", "Round", "Alliance","Starting_pos",
        "Auton_amp", "Auton_speaker","Auton_community",
        "Tele_amp", "Tele_speaker", "Tele_melody",
        "Amplified", "Coopertition", "Stage", "Harmonize",
        "Spotlight", "Role", "Game_piece", "Tier", "Notes"
      ])

      # Database data
      data = db.session.query(
        Scout.regional, Scout.team, Scout.round, Scout.alliance,
        Scout.starting_pos, Scout.auton_amp, Scout.auton_speaker,
        Scout.auton_community,Scout.tele_amp,Scout.tele_speaker,
        Scout.tele_melody, Scout.amplified, Scout.coopertition, 
        Scout.stage, Scout.harmonize, Scout.spotlight,
        Scout.role,  Scout.game_piece,  Scout.tier, Scout.notes)

      #Scout.tele_link, Scout.num_bot, Scout.win, Scout.rank_pt,

      for i in data:
        csv_out.writerow(i)

    # Add data to string
    compressed_data = ''
    compressed_data += str(round) + "@"
    compressed_data += alliance + "@"
    compressed_data += str(team) + "@"
    compressed_data += starting_pos + "@"
    compressed_data += str(auton_amp) + "@"
    compressed_data += str(auton_speaker) + "@"
    compressed_data += str(auton_community) + "@"
    compressed_data += str(tele_amp) + "@"
    compressed_data += str(tele_speaker) + "@"
    compressed_data += str(tele_melody) + "@"
    compressed_data += str(amplified) + "@"
    compressed_data += str(coopertition) + "@"
    compressed_data += str(stage) + "@"
    compressed_data += str(harmonize) + "@"
    compressed_data += str(spotlight) + "@"
    if role is not None:
      compressed_data += role + "@"
    else:
      compressed_data += "None" + "@"
    if game_piece is not None:
      compressed_data += game_piece + "@"
    else:
      compressed_data += "None" + "@"
    compressed_data += str(tier) + "@"
    compressed_data += notes

  # QR Code Formatting
  qr = qrcode.QRCode(version=1, box_size=10, border=1)
  qr.add_data(compressed_data)
  qr.make(fit=True)
  qr_img = qrcode.make(compressed_data)
  image_stream = BytesIO()
  # QR Code image conversion to base64
  qr_img.save(image_stream, format='PNG')
  image_stream.seek(0)
  image_data = base64.b64encode(image_stream.getvalue()).decode('utf-8')

  split_data = update_google_sheet(compressed_data)
  set_averages("T", 5, split_data)
  set_averages("U", 8, split_data)
  #sort_google_sheets()
  #sort works but is very slow - just manually sort it lazy >:(

  return render_template('scout.html',
                         qr_image=image_data,
                         all_teams=all_teams)


# Delete


@auth.route('/delete/<int:id>')
@auth.route('/delete', defaults={'id': None})
def delete(id):
  team_delete = Scout.query.get_or_404(id)
  db.session.delete(team_delete)
  db.session.commit()
  data = Scout.query.order_by(Scout.team).all()
  return render_template('data.html', data=data)


# Download the database
def calculate_total_points(row):
  return (row.auton_amp + row.auton_speaker + 
         row.tele_amp + row.tele_speaker,)


# Download the database
@auth.route('/download')
def download():
  #data = Scout.query.all()
  #retrieving problem, prints the same amount as above in data
  #data = Scout.query.filter(Scout.round.in_(['05', '64034'])).all()
  data = Scout.query.all()
  print(len(data))
  data = sorted(data, key=calculate_total_points, reverse=True)
  # Define the file path for the CSV file
  csv_file_path = 'website/static/filtered_data.csv'

  # Write the filtered data to a CSV file
  with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow([
      "Regional","Team", "Round", "Alliance","Starting_pos",
      "Auton_amp", "Auton_speaker","Auton_community",
      "Tele_amp", "Tele_speaker", "Tele_melody",
      "Amplified", "Coopertition", "Stage", "Harmonize",
      "Spotlight", "Role", "Game_piece", "Tier", "Notes"
    ])
      

    # Write data rows
    for row in data:
      csv_writer.writerow([
        row.regional, row.team, row.round, row.alliance, row.starting_pos,
        row.auton_amp, row.auton_speaker, row.auton_community,
        row.tele_amp, row.tele_speaker, row.tele_melody,
        row.amplified, row.coopertition, row.stage, row.harmonize,
        row.spotlight, row.role, row.game_piece, row.tier, row.notes
      ])

  #return send_file(csv_file_path, as_attachment=True, attachment_filename='filtered_data.csv')
  return render_template('download.html',
                         attachment_filename='filtered_data.csv')


@auth.route('/program')
def download_offline():
  return render_template(
    'program.html',
    attachment_filename=
    'website/static/FrcOfflineProgramDemo.FrcOfflineProgramDemo.zip')


#@auth.route('/download')
#def download():
# return render_template('download.html')

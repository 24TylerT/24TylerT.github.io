from email.mime import image
from flask import Blueprint, render_template, request, flash, redirect, session, url_for, Response
from .models import Scout
from . import db
import csv
#import tbapy
import tbapy
import qrcode
import qrcode.image.svg

tba = tbapy.TBA(
  'h39XHSEqXkc59WvXY0lteYagmwOzWD0wmLV2CxZulOMcB89YIHFUIczJxvGTtM6X')
auth = Blueprint('auth', __name__)

# QR Code
img = qrcode.make('https://2023-Scout-Website.rexpository.repl.co',
                  image_factory=qrcode.image.svg.SvgImage)
with open('website/static/qr.svg', 'wb') as qr:
  img.save(qr)

all_teams_simple = tba.event_teams("2023bcvi", "simple")
all_teams = []
for i in range(len(all_teams_simple)):
  all_teams.append(all_teams_simple[i]['team_number'])


@auth.route('/')
@auth.route('/home')
def home():
  return render_template('home.html')


# Data


@auth.route('/data', methods=['GET', 'POST'])
def data():
  # Show all the scouting data
  data = Scout.query.order_by(Scout.team).all()

  # Search teams
  if request.method == 'POST':
    searched_team = request.form.get('searched_team')
    data = Scout.query.filter_by(team=searched_team).all()

  return render_template('data.html', data=data)


# Scouting


@auth.route('/scout', methods=['GET', 'POST'])
def attempt():
  if request.method == 'POST':
    team = request.form.get('team')
    round = request.form.get('round')
    alliance = request.form.get('alliance')

    # Auton
    starting_pos = request.form.get('starting_pos')
    leave_community = request.form.get('leave_community')

    auton_low_scored = request.form.get('auton_low_scored')
    auton_low_missed = request.form.get('auton_low_missed')
    auton_low_unreliable = request.form.get('auton_unreliable_low')

    auton_mid_scored = request.form.get('auton_mid_scored')
    auton_mid_missed = request.form.get('auton_mid_missed')
    auton_mid_unreliable = request.form.get('auton_unreliable_mid')

    auton_top_scored = request.form.get('auton_top_scored')
    auton_top_missed = request.form.get('auton_top_missed')
    auton_top_unreliable = request.form.get('auton_unreliable_top')

    # Teleop
    tele_low_scored = request.form.get('tele_low_scored')
    tele_low_missed = request.form.get('tele_low_missed')
    tele_low_unreliable = request.form.get('tele_unreliable_low')

    tele_mid_scored = request.form.get('tele_mid_scored')
    tele_mid_missed = request.form.get('tele_mid_missed')
    tele_mid_unreliable = request.form.get('tele_unreliable_mid')

    tele_top_scored = request.form.get('tele_top_scored')
    tele_top_missed = request.form.get('tele_top_missed')
    tele_top_unreliable = request.form.get('tele_unreliable_top')

    # EndGame
    link = request.form.get('link')
    dock = request.form.get('dock')
    park = request.form.get('park')

    # Results
    win = request.form.get('win')
    coop_bonus = request.form.get('coop_bonus')
    sus_bonus = request.form.get('sus_bonus')
    act_bonus = request.form.get('act_bonus')

    notes = request.form.get('notes')

    new_scout = Scout(team=team,
                      round=round,
                      alliance=alliance,
                      starting_pos=starting_pos,
                      leave_community=leave_community,
                      auton_low_scored=auton_low_scored,
                      auton_low_missed=auton_low_missed,
                      auton_low_unreliable=auton_low_unreliable,
                      auton_mid_scored=auton_mid_scored,
                      auton_mid_missed=auton_mid_missed,
                      auton_mid_unreliable=auton_mid_unreliable,
                      auton_top_scored=auton_top_scored,
                      auton_top_missed=auton_top_missed,
                      auton_top_unreliable=auton_top_unreliable,
                      tele_low_scored=tele_low_scored,
                      tele_low_missed=tele_low_missed,
                      tele_low_unreliable=tele_low_unreliable,
                      tele_mid_scored=tele_mid_scored,
                      tele_mid_missed=tele_mid_missed,
                      tele_mid_unreliable=tele_mid_unreliable,
                      tele_top_scored=tele_top_scored,
                      tele_top_missed=tele_top_missed,
                      tele_top_unreliable=tele_top_unreliable,
                      link=link,
                      dock=dock,
                      park=park,
                      win=win,
                      coop_bonus=coop_bonus,
                      sus_bonus=sus_bonus,
                      act_bonus=act_bonus,
                      notes=notes)

    try:
      db.session.add(new_scout)
      Scout.query.all()
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
        "Team", "Round", "Alliance", "Starting_pos", "Taxi", "A_Upper_In",
        "A_Upper_Missed", "A_Upper_Unreliable", "A_Lower_In", "A_Lower_Missed",
        "A_Lower_Unreliable", "T_Upper_In", "T_Upper_Missed",
        "T_Upper_Unreliable", "T_Lower_In", "T_Lower_Missed",
        "T_Lower_Unreliable", "Hang", "Cargo", "Hangar", "Notes"
      ])

      # Database data
      data = db.session.query(
        Scout.team, Scout.round, Scout.alliance, Scout.starting_pos,
        Scout.taxi, Scout.auton_upper_in, Scout.auton_upper_missed,
        Scout.auton_upper_unreliable, Scout.auton_lower_in,
        Scout.auton_lower_missed, Scout.auton_lower_unreliable,
        Scout.tele_upper_in, Scout.tele_upper_missed,
        Scout.tele_upper_unreliable, Scout.tele_lower_in,
        Scout.tele_lower_missed, Scout.tele_lower_unreliable, Scout.hang,
        Scout.cargo_bonus, Scout.hangar_bonus, Scout.notes)

      for i in data:
        csv_out.writerow(i)

  return render_template('scout.html', all_teams=all_teams)


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


@auth.route('/download')
def download():
  return render_template('download.html')

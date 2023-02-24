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
img = qrcode.make('https://2023-Scouting-Website.rexpository.repl.co',
                  image_factory=qrcode.image.svg.SvgImage)
with open('website/static/qr.svg', 'wb') as qr:
    img.save(qr)

all_teams_simple = tba.event_teams("2022tant", "simple")
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

        auton_low_in = request.form.get('auton_low_in')
        auton_low_missed = request.form.get('auton_low_missed')
        auton_low_unreliable = request.form.get('auton_unreliable_low')

        auton_mid_in = request.form.get('auton_mid_in')
        auton_mid_missed = request.form.get('auton_mid_missed')
        auton_mid_unreliable = request.form.get('auton_unreliable_mid')

        auton_top_in = request.form.get('auton_high_in')
        auton_top_missed = request.form.get('auton_high_missed')
        auton_top_unreliable = request.form.get('auton_unreliable_high')

        auton_community = request.form.get('auton_community')
        auton_dock_park = request.form.get('auton_dock_park')
        
        # Teleop
        tele_low_in = request.form.get('tele_low_in')
        tele_low_missed = request.form.get('tele_low_missed')
        tele_low_unreliable = request.form.get('tele_unreliable_low')

        tele_mid_in = request.form.get('tele_mid_in')
        tele_mid_missed = request.form.get('tele_mid_missed')
        tele_mid_unreliable = request.form.get('tele_unreliable_mid')

        tele_high_in = request.form.get('tele_high_in')
        tele_high_missed = request.form.get('tele_high_missed')
        tele_high_unreliable = request.form.get('tele_unreliable_high')
        
        # EndGame
        tele_link = request.form.get('tele_link')
        tele_link_unreliable = request.form.get('tele_unreliable_link')
        dock_park = request.form.get('dock_park')
        
        # Results
        win = request.form.get('win')
        role = request.form.get('role')
        sus_bonus = request.form.get('sus_bonus')
        coop_bonus = request.form.get('coop_bonus')
        act_bonus = request.form.get('act_bonus')

        notes = request.form.get('notes')

        new_scout = Scout(team=team, round=round, alliance=alliance, starting_pos=starting_pos, auton_low_in=auton_low_in, auton_low_missed=auton_low_missed,auton_low_unreliable=auton_low_unreliable,
                          auton_mid_in=auton_mid_in, auton_mid_missed=auton_mid_missed,auton_mid_unreliable=auton_mid_unreliable, auton_top_in=auton_top_in, auton_top_missed=auton_top_missed, auton_top_unreliable=auton_top_unreliable, auton_community=auton_community, auton_dock_park=auton_dock_park,
                          tele_low_in=tele_low_in, tele_low_missed=tele_low_missed, tele_low_unreliable=tele_low_unreliable, tele_mid_in=tele_mid_in, tele_mid_missed=tele_mid_missed, tele_mid_unreliable=tele_mid_unreliable, 
                          tele_high_in=tele_high_in, tele_high_missed=tele_high_missed, tele_high_unreliable=tele_high_unreliable, tele_link=tele_link, tele_unreliable_link=tele_link_unreliable, dock_park=dock_park, win=win, role=role, sus_bonus=sus_bonus, coop_bonus=coop_bonus, act_bonus=act_bonus, notes=notes)

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
            csv_out.writerow(["Team", "Round", "Alliance", "Starting_pos", "A_Low_In", "A_Low_Missed", "A_Low_Unreliable", "A_Mid_In", "A_Mid_Missed", "A_Mid_Unreliable", "A_High_In", "A_High_Missed", "A_High_Unreliable", "A_Community", "A_Dock_Park",
                             "T_Low_In", "T_Low_Missed", "T_Low_Unreliable", "T_Mid_In", "T_Mid_Missed", "T_Mid_Unreliable", "T_High_In", "T_High_Missed", "T_High_Unreliable", "Link", "Link_Unreliable", "Dock_Park", "Win/Lose/Tie", "Sus_bonus", "Coop_bonus", "Act_bonus", "Notes"])

            # Database data
            data = db.session.query(Scout.team, Scout.round, Scout.alliance, Scout.starting_pos, Scout.auton_low_in, Scout.auton_low_missed, Scout.auton_low_unreliable, Scout.auton_mid_in, Scout.auton_mid_missed, Scout.auton_mid_unreliable,
                                    Scout.auton_high_in, Scout.auton_high_missed, Scout.auton_high_unreliable, Scout.auton_community, Scout.auton_dock_park, Scout.tele_low_in, Scout.tele_low_missed, Scout.tele_low_unreliable, Scout.tele_mid_in, Scout.tele_mid_missed, Scout.tele_mid_unreliable, Scout.tele_high_in, Scout.tele_high_missed, Scout.tele_high_unreliable, Scout.tele_link, Scout.tele_link_unreliable, Scout.dock_park, Scout.win, Scout.role, Scout.sus_bonus, Scout.coop_bonus, Scout.act_bonus, Scout.notes)

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

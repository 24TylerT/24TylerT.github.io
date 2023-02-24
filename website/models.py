from . import db
from flask_login import UserMixin

class Scout(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(20))
    round = db.Column(db.String(20))
    alliance = db.Column(db.String(20))

    starting_pos = db.Column(db.String(20))
    auton_low_in = db.Column(db.String(20))
    auton_low_missed = db.Column(db.String(20))
    auton_low_unreliable = db.Column(db.String(20))
    auton_mid_in = db.Column(db.String(20))
    auton_mid_missed = db.Column(db.String(20))
    auton_mid_unreliable = db.Column(db.String(20))
    auton_high_in = db.Column(db.String(20))
    auton_high_missed = db.Column(db.String(20))
    auton_high_unreliable = db.Column(db.String(20))
    auton_community = db.Column(db.String(20))
    auton_dock_park = db.Column(db.String(20))

    tele_low_in = db.Column(db.String(20))
    tele_low_missed = db.Column(db.String(20))
    tele_low_unreliable = db.Column(db.String(20))
    tele_mid_in = db.Column(db.String(20))
    tele_mid_missed = db.Column(db.String(20))
    tele_mid_unreliable = db.Column(db.String(20))
    tele_high_in = db.Column(db.String(20))
    tele_high_missed = db.Column(db.String(20))
    tele_high_unreliable = db.Column(db.String(20))

    tele_link = db.Column(db.String(20))
    tele_link_unreliable = db.Column(db.String(20))

    dock_park = db.Column(db.String(20))
    win = db.Column(db.String(20))
    sus_bonus = db.Column(db.String(20))
    coop_bonus = db.Column(db.String(20))
    act_bonus = db.Column(db.String(20))
    
    notes = db.Column(db.String(200))

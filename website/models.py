from . import db
from flask_login import UserMixin


class Scout(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  regional = db.Column(db.String(20))
  round = db.Column(db.String(20))
  alliance = db.Column(db.String(20))

  #Team 1

  team = db.Column(db.String(20))
  starting_pos = db.Column(db.String(20))
  auton_amp = db.Column(db.String(20))
  auton_speaker = db.Column(db.String(20))

  auton_community = db.Column(db.String(20))
  tele_amp = db.Column(db.String(20))
  tele_speaker = db.Column(db.String(20))
  tele_melody = db.Column(db.String(20))
  coopertition = db.Column(db.String(20))
  amplified = db.Column(db.String(20))

  stage = db.Column(db.String(20))
  spotlight = db.Column(db.String(20))
  harmonize = db.Column(db.String(20))

  role = db.Column(db.String(20))
  game_piece = db.Column(db.String(20))
  tier = db.Column(db.String(20))
  win = db.Column(db.String(20))

  notes = db.Column(db.String(200))

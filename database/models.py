from app import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), nullable=False)
    song_title = db.Column(db.String(255), nullable=False)
    song_url = db.Column(db.String(500), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Favorite {self.song_title} by user {self.user_id}>"

from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from . import db
import logging
logger = logging.getLogger(__name__)


class Article(db.Model):
    __tablename__ = 'cms_article'

    id = Column(Integer, primary_key=True)

    title = Column(Text)
    content = Column(Text)
    image = Column(Text)
    images = Column(Text)
    video = Column(Text)
    videos = Column(Text)

    def to_dict(self):
        pass



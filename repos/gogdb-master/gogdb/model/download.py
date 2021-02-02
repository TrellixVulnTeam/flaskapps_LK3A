import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column

from gogdb import db
from gogapi import names


class DlFile(db.Model):
    __tablename__ = "files"
    __table_args__ = (sql.UniqueConstraint("download_id", "slug"),)

    download_id = Column(sql.Integer, sql.ForeignKey("downloads.id"),
        primary_key=True, autoincrement=False)
    slug = Column(sql.String(50), primary_key=True)
    size = Column(sql.BigInteger, nullable=False)
    deleted = Column(sql.Boolean, default=False, nullable=False)

    download = orm.relationship("Download", back_populates="files")

    def __repr__(self):
        return "<DlFile(download_id={}, slug='{}', name='{}')>".format(
            self.download_id, self.slug, self.size)


class Download(db.Model):
    __tablename__ = "downloads"
    __table_args__ = (sql.UniqueConstraint("prod_id", "slug"),)

    id = Column(sql.Integer, primary_key=True, autoincrement=True)
    prod_id = Column(
        sql.Integer, sql.ForeignKey("products.id"), nullable=False)
    slug = Column(sql.String(50), nullable=False)
    name = Column(sql.String(120), nullable=False)
    type = Column(sql.String(50), nullable=False)
    bonus_type = Column(sql.String(50), nullable=True)
    count = Column(sql.Integer, nullable=True)
    os = Column(sql.String(20), nullable=True)
    language = Column(sql.String(5), nullable=True)
    version = Column(sql.String(120), nullable=True)
    deleted = Column(sql.Boolean, default=False, nullable=False)

    product = orm.relationship("Product", back_populates="downloads")
    files = orm.relationship(
        "DlFile", back_populates="download", lazy="joined",
        cascade="all, delete-orphan", order_by="DlFile.slug")

    @property
    def type_name(self):
        return names.DL_TYPES.get(self.type, self.type)

    @property
    def os_name(self):
        return names.SYSTEMS.get(self.os, self.os)

    @property
    def language_name(self):
        return names.IETF_CODES.get(self.language, self.language)

    @property
    def bonus_type_name(self):
        return names.BONUS_TYPES.get(self.bonus_type, self.bonus_type)

    @property
    def total_size(self):
        return sum(f.size for f in self.files if not f.deleted)

    @property
    def valid_files(self):
        return [dlfile for dlfile in self.files if not dlfile.deleted]

    def file_by_slug(self, slug):
        for dlfile in self.files:
            if dlfile.slug == slug:
                return dlfile
        return None

    def __repr__(self):
        return "<Download(id={}, prod_id={}, slug='{}')>".format(
            self.id, self.prod_id, self.slug)

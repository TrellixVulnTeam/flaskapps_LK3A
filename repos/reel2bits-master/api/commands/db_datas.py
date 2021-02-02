import click
from models import db, Sound, User, Role, Config, Album
from utils.flake_id import FlakeId
from uuid import UUID
from utils.defaults import Reel2bitsDefaults
import os
from flask.cli import with_appcontext
from flask import current_app


@click.group()
def db_datas():
    """
    Datas migrations sometimes needed.

    Run them only one time unless specified BREAKING.
    """
    pass


def make_db_seed(db):
    # roles
    roles = db.session.query(Role.name).all()
    roles = [r[0] for r in roles]
    if "user" not in roles:
        role_usr = Role(name="user", description="Simple user")
        db.session.add(role_usr)
    if "admin" not in roles:
        role_adm = Role(name="admin", description="Admin user")
        db.session.add(role_adm)
    if "moderator" not in roles:
        role_mod = Role(name="moderator", description="Moderator user")
        db.session.add(role_mod)
    # Config
    config = Config.query.first()
    if not config:
        a = Config(app_name="My reel2bits instance", app_description="This is a reel2bits instance")
        db.session.add(a)

    # Final commit
    db.session.commit()


@db_datas.command(name="000-seeds")
@with_appcontext
def seeds():
    """
    Seed database with default config and roles values

    non breaking.
    """
    make_db_seed(db)


@db_datas.command(name="001-generate-tracks-uuids")
@with_appcontext
def generate_tracks_uuid():
    """
    Generate tracks UUIDs when missing (41_7eb56606e9d6)

    non breaking.
    """
    flake_gen = FlakeId()
    for sound in db.session.query(Sound).all():
        if not sound.flake_id:
            sound.flake_id = UUID(int=flake_gen.get())
    db.session.commit()


@db_datas.command(name="002-set-local-users")
@with_appcontext
def set_local_users():
    """
    Set User.local == user.actor.local (46_a3ada8658a05)

    non breaking.
    """
    for user in db.session.query(User).all():
        if len(user.actor) >= 1:
            if user.actor[0]:
                user.local = user.actor[0].is_local()
    db.session.commit()


@db_datas.command(name="003-set-user-quota")
@with_appcontext
def set_uset_quota():
    """
    Set default user quota (52_d37e30db3df1)

    non breaking.
    """
    for user in db.session.query(User).all():
        if not user.quota:
            user.quota = Reel2bitsDefaults.user_quotas_default
        if not user.quota_count:
            user.quota_count = 0
    db.session.commit()


@db_datas.command(name="004-update-file-sizes")
@with_appcontext
def update_file_sizes():
    """
    Update track files and transcode sizes (52_d37e30db3df1)

    non breaking.
    """
    for track in Sound.query.filter(Sound.file_size.is_(None)).all():
        path_sound = track.path_sound(orig=True)
        if not path_sound:
            continue
        track.file_size = os.path.getsize(os.path.join(current_app.config["UPLOADED_SOUNDS_DEST"], path_sound))
        if track.transcode_needed:
            path_sound = track.path_sound(orig=False)
            if not path_sound:
                continue
            track.transcode_file_size = os.path.getsize(
                os.path.join(current_app.config["UPLOADED_SOUNDS_DEST"], path_sound)
            )
    db.session.commit()


@db_datas.command(name="005-update-user-quotas")
@with_appcontext
def update_user_quotas():
    """
    Update user quotas

    non breaking.
    """
    for user in User.query.filter(User.local.is_(True)).all():
        print(f"computing for {user.name} ({user.id})")
        user.quota_count = user.total_files_size()
    db.session.commit()


@db_datas.command(name="006-generate-albums-uuids")
@with_appcontext
def generate_albums_uuid():
    """
    Generate albums UUIDs when missing (43_b34114160aa4)

    non breaking.
    """
    flake_gen = FlakeId()
    for album in db.session.query(Album).all():
        if not album.flake_id:
            album.flake_id = UUID(int=flake_gen.get())
    db.session.commit()


@db_datas.command(name="007-generate-users-uuids")
@with_appcontext
def generate_users_uuid():
    """
    Generate user UUIDs when missing

    non breaking.
    """
    flake_gen = FlakeId()
    for user in db.session.query(User).all():
        if not user.flake_id:
            user.flake_id = UUID(int=flake_gen.get())
    db.session.commit()

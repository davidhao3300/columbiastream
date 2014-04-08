from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
pic = Table('pic', post_meta,
    Column('id', String(length=100), primary_key=True, nullable=False),
    Column('link', String(length=140)),
    Column('small_link', String(length=140)),
    Column('timestamp', Integer),
    Column('likes', Integer),
    Column('poster', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pic'].columns['small_link'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pic'].columns['small_link'].drop()

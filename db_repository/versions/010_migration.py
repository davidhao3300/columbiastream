from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
followers = Table('followers', pre_meta,
    Column('better_id', Integer),
    Column('pic_id', String),
)

bets = Table('bets', post_meta,
    Column('better_id', Integer, primary_key=True, nullable=False),
    Column('pic_id', Integer, primary_key=True, nullable=False),
    Column('end_time', Integer),
    Column('amount', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['followers'].drop()
    post_meta.tables['bets'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['followers'].create()
    post_meta.tables['bets'].drop()

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
bets = Table('bets', post_meta,
    Column('better_id', Integer, primary_key=True, nullable=False),
    Column('pic_id', String, primary_key=True, nullable=False),
    Column('end_time', Integer),
    Column('amount', Integer),
    Column('expired', Boolean, default=ColumnDefault(False)),
    Column('result', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['bets'].columns['result'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['bets'].columns['result'].drop()

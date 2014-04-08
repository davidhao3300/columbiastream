from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
betters = Table('betters', pre_meta,
    Column('better_id', String),
    Column('pic_id', Integer),
)

followers = Table('followers', post_meta,
    Column('better_id', Integer),
    Column('pic_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['betters'].drop()
    post_meta.tables['followers'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['betters'].create()
    post_meta.tables['followers'].drop()

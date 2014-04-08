from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
better_pic = Table('better_pic', pre_meta,
    Column('better_id', Integer),
    Column('pic_id', Integer),
)

betters = Table('betters', post_meta,
    Column('better_id', Integer),
    Column('pic_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['better_pic'].drop()
    post_meta.tables['betters'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['better_pic'].create()
    post_meta.tables['betters'].drop()

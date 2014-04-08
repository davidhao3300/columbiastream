from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
better = Table('better', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('fullname', String(length=64)),
    Column('profile_pic', String(length=100)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('username', String(length=64)),
    Column('about', String(length=300)),
    Column('website', String(length=120)),
    Column('access_token', String(length=100)),
    Column('followers', Integer),
    Column('currency', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['better'].columns['currency'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['better'].columns['currency'].drop()

import logging
import datetime

from sqlalchemy import *
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import relation, backref, class_mapper, joinedload
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base

from kallithea.lib.dbmigrate.migrate import *
from kallithea.lib.dbmigrate.migrate.changeset import *

from kallithea.model.meta import Base
from kallithea.model import meta
from kallithea.lib.dbmigrate.versions import _reset_base

log = logging.getLogger(__name__)


def upgrade(migrate_engine):
    """
    Upgrade operations go here.
    Don't create your own engine; bind migrate_engine to your metadata
    """
    _reset_base(migrate_engine)


    #==========================================================================
    # UserGroup
    #==========================================================================
    from kallithea.lib.dbmigrate.schema.db_1_7_0 import UserGroup
    tbl = UserGroup.__table__
    user_id = tbl.columns.user_id
    user_id.alter(nullable=False)

    #==========================================================================
    # RepoGroup
    #==========================================================================
    from kallithea.lib.dbmigrate.schema.db_1_7_0 import RepoGroup
    tbl = RepoGroup.__table__
    user_id = tbl.columns.user_id
    user_id.alter(nullable=False)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

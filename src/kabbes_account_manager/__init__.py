import dir_ops as do
import os
import py_starter as ps
import kabbes_config

### Constants
ENCODING = 'utf-8'
DT_FORMAT = '%Y-%m-%d %H:%M'

_Dir      = do.Dir( os.path.abspath( __file__ ) ).ascend()
_src_Dir  = do.Dir( os.path.abspath( __file__ ) ).ascend(level_to_ascend=2)
_repo_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend(level_to_ascend=3)

#
templates_Dir = _Dir.join_Dir( path = 'AccountTemplates/Templates' )
DEFAULT_CONFIG_PATH = _Dir.join_Path( path = 'default_config.json' )
        
from .utils import *
from .Base import Base
from .Key_Value_CRTI import Key_Value_CRTI
from .Key_Value_Base import Key_Value_Base
from .Key import Key
from .Value import Value
from .Entry import Entry
from .Entries import Entries
from .Accounts import Accounts
from .Manager import Manager



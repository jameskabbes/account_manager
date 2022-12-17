import dir_ops as do
import os
import py_starter as ps

### Constants
ENCODING = 'utf-8'
DT_FORMAT = '%Y-%m-%d %H:%M'


# dirs
_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
_src_Dir = _Dir.ascend()                                  #src Dir that is one above
_repo_Dir = _src_Dir.ascend()                    

# Settings
default_settings_Path = _Dir.join_Path( path = 'default_settings.json' )
Settings = ps.Settings( **ps.json_to_dict(default_settings_Path.read()) )

#
templates_Dir = _Dir.join_Dir( path = 'AccountTemplates/Templates' )

from .utils import *
from .Base import Base
from .Key_Value_CRTI import Key_Value_CRTI
from .Key_Value_Base import Key_Value_Base
from .Key import Key
from .Value import Value
from .Entry import Entry
from .Entries import Entries
from .Accounts import Accounts



import kabbes_account_manager
from kabbes_account_manager import Base, Entries
import py_starter as ps
import pandas as pd
import datetime

def make_Account( module, *args, **kwargs ):

    return module.construct( *args, **kwargs )


class BaseAccount( Base ):

    BASE_MAND_ENTRIES =           ['type','id','name','times_accessed','creation_date','access_date','entry_to_copy']
    BASE_IMMUTABLE_ENTRY_KEYS =   ['type','id','name','times_accessed','creation_date','access_date','entry_to_copy']
    BASE_IMMUTABLE_ENTRY_VALUES = ['type','id',       'times_accessed','creation_date','access_date'                ]

    BASE_DICTIONARY = {
        'times_accessed': 0,
        'entry_to_copy': 'name'
    }

    OTHER_MAND_ENTRIES = []
    OTHER_IMMUTABLE_ENTRY_KEYS = []
    OTHER_IMMUTABLE_ENTRY_VALUES = []

    _OVERRIDE_OPTIONS = {
    "1": [ 'Open Entries', 'open_Entries' ],
    "2": [ 'Add Entries', 'add_Entries_user'],
    "5": [ 'Open Accounts', 'run_Accounts' ],
    "7": ['Delete','delete']
    }

    BASE_IMP_ATTS = [ 'name','type' ]
    _ONE_LINE_ATTS = [ 'type','name' ]
    OTHER_IMP_ATTS = []

    _SEARCHABLE_ATTS = ['name']

    def __init__(self, Accounts, dictionary = {}, **kwargs ):

        Base.__init__( self, **kwargs )
        self.Accounts = Accounts

        ### Get mandatory entries
        self.MAND_ENTRIES = self.BASE_MAND_ENTRIES.copy()
        self.MAND_ENTRIES += self.OTHER_MAND_ENTRIES

        ### Get immutable keys and values
        self.IMMUTABLE_ENTRY_KEYS = self.BASE_IMMUTABLE_ENTRY_KEYS.copy()
        self.IMMUTABLE_ENTRY_KEYS += self.OTHER_IMMUTABLE_ENTRY_KEYS

        self.IMMUTABLE_ENTRY_VALUES = self.BASE_IMMUTABLE_ENTRY_VALUES.copy()
        self.IMMUTABLE_ENTRY_VALUES += self.OTHER_IMMUTABLE_ENTRY_VALUES

        ### Get IMP_ATTS
        self._IMP_ATTS = self.BASE_IMP_ATTS.copy()
        self._IMP_ATTS += self.OTHER_IMP_ATTS

        # make sure all MAND_ENTRIES are there
        combined_dict = self.BASE_DICTIONARY.copy()
        combined_dict.update( self.OTHER_DICTIONARY )
        combined_dict.update( dictionary )
        dictionary = self.get_mand_entries( combined_dict )

        # init always with the type autodetected
        self.load_Entries( dictionary = dictionary )
        self.name = self.Entries.get_Entry( 'name' ).Value.val
        self._Children = [ self.Entries ]

    def run_Accounts( self ):
        self.Accounts.run()

    def get_Entry_key_value( self, Entry_key ):

        return self.Entries.get_Entry( Entry_key ).Value.val

    def get_id( self ):

        return self.get_Entry_key_value( 'id' )

    def get_name( self ):

        return self.get_Entry_key_value( 'name' )

    def get_password( self ):

        return self.get_Entry_key_value( 'password' )

    def get_mand_entries( self, dictionary ):

        for entry in self.MAND_ENTRIES:
            if entry not in dictionary:
                value = None

                if entry == 'id':
                    value = kabbes_account_manager.get_nanoid()
                elif entry == 'type':
                    value = self.type
                elif entry == 'creation_date':
                    value = datetime.datetime.now().strftime( kabbes_account_manager.DT_FORMAT )
                elif entry == 'access_date':
                    value = datetime.datetime.now().strftime( kabbes_account_manager.DT_FORMAT )

                dictionary[ entry ] = value

        return dictionary

    def delete_self( self ):

        self.Accounts.delete_Account( self )

    def load_Entries( self, **kwargs ):

        self.Entries = Entries( self, **kwargs )

    def export_to_dict( self ):

        d = { self.get_id(): self.Entries.export_to_dict() }
        return d

    def add_Entries_user( self ):

        self.Entries.make_Entry_user()

    def open_Entries( self ):

        self.Entries.run()

    def pre_run( self ):

        times_accessed_Entry = self.Entries.get_Entry( 'times_accessed' )
        times_accessed_Entry.Value.val += 1

        self.Entries.get_Entry('access_date').Value.val = datetime.datetime.now().strftime( kabbes_account_manager.DT_FORMAT )

        # copy whatever the Entries class does upon running
        self.Entries.pre_run()

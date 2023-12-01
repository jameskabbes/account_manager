from parent_class import ParentClass
import py_seedlings as ps

class Base( ParentClass ):

    DEFAULT_ATT_VALUES = {}

    def __init__( self, **kwargs ):

        ParentClass.__init__( self )

        ### Setup kwargs
        kwargs = ps.replace_default_kwargs( self.DEFAULT_ATT_VALUES, **kwargs )
        self.set_atts( kwargs )

    def delete( self ):

        if input('Type "delete" to delete: ') == 'delete':
            self.delete_self()

    def delete_self( self ):
        pass

from kabbes_menu import Menu
import py_starter as ps

class Base( Menu ):

    DEFAULT_ATT_VALUES = {}

    def __init__( self, **kwargs ):
        Menu.__init__( self )

        ### Setup kwargs
        kwargs = ps.replace_default_kwargs( self.DEFAULT_ATT_VALUES, **kwargs )
        self.set_atts( kwargs )

    def delete( self ):

        if input('Type "delete" to delete: ') == 'delete':
            self.delete_self()

    def delete_self( self ):
        pass

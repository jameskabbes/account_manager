import kabbes_account_manager
import kabbes_client

class Client( kabbes_account_manager.Manager ):

    _BASE_DICT = {}

    def __init__( self, dict={}, root_dict={}, **kwargs ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        root_inst = kabbes_client.Root( root_dict=root_dict )
        self.Package = kabbes_client.Package( kabbes_account_manager._Dir, dict=d, root=root_inst )
        self.cfg = self.Package.cfg

        kabbes_account_manager.Manager.__init__( self, **kwargs )

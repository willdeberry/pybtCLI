
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository.GObject import MainLoop


from .logger import logger
from .service import ManagerService
from .support_service import SupportService



def main():
    """The main entry point for the systemd service."""
    DBusGMainLoop( set_as_default = True )

    service = ManagerService()
    support_service = SupportService()

    try:
        logger.debug( 'entering main loop' )
        MainLoop().run()
    except KeyboardInterrupt:
        pass


from loguru import logger 
from datetime import datetime
import graypy, os


# Setup logger - Modifies an existing logger to add our handlers
def setup_logging(logger):
    # Handlers to return
    handlers = []
    
    # Add Graylog handler
    graylog_handler = graypy.GELFUDPHandler('13.67.218.25', 12201)    
    handlers.append(logger.add(graylog_handler, colorize=False))

    # Add file handler
    logfile = os.path.join('/logs/', 'my_app_' + datetime.now().strftime('%Y%m%d') + '.log')
    handlers.append(logger.add(logfile, rotation="12:00", compression="tar.gz"))
    logger.configure(extra={'application': f'induction: flask-app'})
    
    return handlers

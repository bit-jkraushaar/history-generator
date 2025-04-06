import logging
import sys

def setup_logger(name):
    """Configures and returns a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output
    
    # Formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Global logger instances
event_logger = setup_logger('events')
world_logger = setup_logger('world')

# Configure world logger
world_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure event logger
event_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure dynasty logger
dynasty_logger = logging.getLogger('dynasty')
dynasty_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure marriage logger
marriage_logger = logging.getLogger('marriage')
marriage_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure person logger
person_logger = logging.getLogger('person')
person_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure simulation logger
simulation_logger = logging.getLogger('simulation')
simulation_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure event processor logger
event_processor_logger = logging.getLogger('event_processor')
event_processor_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure fantasy world logger
fantasy_world_logger = logging.getLogger('fantasy_world')
fantasy_world_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure fantasy events logger
fantasy_events_logger = logging.getLogger('fantasy_events')
fantasy_events_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure main logger
main_logger = logging.getLogger('main')
main_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce output

# Configure root logger
logging.basicConfig(
    level=logging.WARNING,  # Change to WARNING to reduce output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) 
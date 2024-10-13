# app.py

import dash
import dash_bootstrap_components as dbc
from layout import get_layout
from callbacks import register_callbacks
import logging
import os
from logging.handlers import RotatingFileHandler

# =============================================================================
# Logging Configuration
# =============================================================================

# Define the directory where log files will be stored
LOG_DIR = 'logs'

# Define the name of the log file
LOG_FILE = 'app.log'

# Create the log directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Construct the full path to the log file
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Retrieve the log level from the environment variable 'LOG_LEVEL'
# Default to 'DEBUG' if not set
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()

# Validate the log level; fallback to 'DEBUG' if invalid
if LOG_LEVEL not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
    LOG_LEVEL = 'DEBUG'  # Fallback to DEBUG if invalid level is set

# Create a RotatingFileHandler to handle log file rotation
file_handler = RotatingFileHandler(
    LOG_PATH, maxBytes=5*1024*1024, backupCount=5
)
file_handler.setLevel(LOG_LEVEL)  # Set the logging level for the file handler
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))  # Define the log message format

# Create a StreamHandler to output logs to the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(LOG_LEVEL)  # Set the logging level for the stream handler
stream_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))  # Define the log message format

# Configure the root logger with the defined handlers
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Base logging level
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Create a logger specific to this module
logger = logging.getLogger(__name__)
logger.info(f"Starting Dash application with log level: {LOG_LEVEL}")

# =============================================================================
# Dash Application Initialization
# =============================================================================

# Initialize the Dash application with Bootstrap stylesheet
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # Apply Bootstrap theme
    suppress_callback_exceptions=True  # Allow callbacks for dynamic components
)

# Expose the underlying Flask server for deployment or additional configurations
server = app.server

# Set the layout of the Dash application by invoking the get_layout function
app.layout = get_layout()

# Register all necessary callbacks by invoking the register_callbacks function
register_callbacks(app)

# =============================================================================
# Application Entry Point
# =============================================================================

if __name__ == '__main__':
    # Run the Dash server in debug mode for development purposes
    app.run_server(debug=True)

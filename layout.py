# layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
from components.graph import GraphComponent
from data import central_node, primary_nodes, subnodes
from utils.helpers import load_graph_elements, load_graph_state
import logging

# Initialize logger for this module
logger = logging.getLogger(__name__)

def load_initial_graph_state():
    """
    Loads the initial graph state from the database.

    Returns:
        dict or None: The saved graph state if available, else None.
    """
    return load_graph_state()

def get_layout():
    """
    Constructs and returns the layout for the Dash application.

    Returns:
        dbc.Container: The Dash layout container with all UI components.
    """
    # Attempt to load the graph's initial state from persistent storage
    initial_state = load_initial_graph_state()

    if initial_state:
        # If a saved state exists, extract elements, zoom, and pan
        elements = initial_state.get('elements', [])
        zoom = initial_state.get('zoom', 1.0)
        pan = initial_state.get('pan', {'x': 0, 'y': 0})
    else:
        # If no saved state, initialize with default data from `data.py`
        elements = load_graph_elements(central_node, primary_nodes, subnodes)
        zoom = 1.0  # Default zoom level
        pan = {'x': 0, 'y': 0}  # Default pan position

    # Log details of loaded elements for debugging purposes
    for elem in elements:
        # Identify node elements by absence of 'source' and 'target' (edge identifiers)
        if 'source' not in elem['data'] and 'target' not in elem['data']:
            node_id = elem['data']['id']
            color = elem['data'].get('color', 'No color specified')
            classes = elem.get('classes', 'No classes specified')
            logger.debug(f"Loaded Node ID: {node_id}, Color: {color}, Classes: {classes}")

    return dbc.Container([
        # =============================================================================
        # Data Storage Components
        # =============================================================================

        # Store to keep original graph elements for reference or reset purposes
        dcc.Store(
            id='original-elements',
            data=elements  # Initialize with loaded or default graph elements
        ),

        # Store to maintain the current graph state, including zoom and pan
        # Uses local storage to persist state across browser sessions
        dcc.Store(
            id='store-graph-state',
            data={'elements': elements, 'zoom': zoom, 'pan': pan},
            storage_type='local'
        ),

        # =============================================================================
        # Header
        # =============================================================================

        # Application Title
        html.H2(
            "Azure Architecture Map",
            className='text-center my-4'  # Centered text with vertical margins
        ),

        # =============================================================================
        # Main Content: Graph and Control Panels
        # =============================================================================

        dbc.Row([
            # -----------------------------------------------------------------------------
            # Left Column: Cytoscape Graph
            # -----------------------------------------------------------------------------
            dbc.Col(
                GraphComponent(
                    elements=elements,  # Pass the graph elements to render
                    zoom=zoom,          # Set the initial zoom level
                    pan=pan             # Set the initial pan position
                ),
                width=8  # Occupies approximately 66% of the row
            ),
            # -----------------------------------------------------------------------------
            # Right Column: Controls and Information Panels
            # -----------------------------------------------------------------------------
            dbc.Col(
                [
                    # -----------------------------------------------------------------------------
                    # 1. Search Input
                    # Allows users to search for specific nodes within the graph
                    # -----------------------------------------------------------------------------
                    dbc.Input(
                        id='node-search',
                        type='text',
                        placeholder='Search nodes...',  # Placeholder guiding the user
                        value='',                        # Initial value is empty
                        className='mb-3'                 # Bottom margin for spacing
                    ),

                    # -----------------------------------------------------------------------------
                    # 2. Zoom Controls
                    # Buttons to control the zoom level of the Cytoscape graph
                    # -----------------------------------------------------------------------------
                    dbc.Button(
                        "Zoom In",
                        id="zoom-in",
                        color="primary",    # Bootstrap primary color (usually blue)
                        className="mb-2 w-100"  # Bottom margin and full-width
                    ),
                    dbc.Button(
                        "Zoom Out",
                        id="zoom-out",
                        color="primary",
                        className="mb-2 w-100"
                    ),
                    dbc.Button(
                        "Reset Zoom",
                        id="reset-zoom",
                        color="secondary",  # Bootstrap secondary color (usually gray)
                        className="mb-4 w-100"  # Additional bottom margin
                    ),

                    # -----------------------------------------------------------------------------
                    # 3. Save and Load State Controls
                    # Buttons to save the current graph state or load a saved state
                    # -----------------------------------------------------------------------------
                    dbc.Button(
                        "Save State",
                        id="save-state",
                        color="success",  # Bootstrap success color (usually green)
                        className="mb-2 w-100"
                    ),
                    dbc.Button(
                        "Load State",
                        id="load-state",
                        color="info",     # Bootstrap info color (usually light blue)
                        className="mb-4 w-100"
                    ),

                    # -----------------------------------------------------------------------------
                    # 4. Node Information and Notes Section
                    # Displays details about selected nodes and allows adding/editing notes
                    # -----------------------------------------------------------------------------
                    dbc.Card(
                        dbc.CardBody([
                            # Node Information Display
                            html.Div(
                                id='node-info',
                                children="Click on a node to see details.",
                                style={'minHeight': '50px'}  # Ensures space allocation
                            ),
                            # Rendered Notes Display (Initially Hidden)
                            html.Div(
                                id='rendered-notes-section',
                                children=[
                                    html.H5("Notes:"),
                                    dcc.Markdown(
                                        id='rendered-notes',
                                        children=''  # Will be populated dynamically
                                    )
                                ],
                                style={'display': 'none'}  # Hidden until notes are present
                            ),
                            # Notes Editing Section (Initially Hidden)
                            html.Div(
                                id='notes-section',
                                children=[
                                    html.H5("Add or Edit Notes:"),
                                    dcc.Textarea(
                                        id='node-notes',
                                        value='',  # Initial notes value is empty
                                        style={'width': '100%', 'height': '100px'}  # Full-width textarea
                                    ),
                                    dbc.Button(
                                        "Save Note",
                                        id='save-note',
                                        color='primary',  # Bootstrap primary color
                                        className='mt-2 w-100'  # Top margin and full-width
                                    )
                                ],
                                style={'display': 'none'}  # Hidden until a node is selected
                            )
                        ])
                    ),

                    # -----------------------------------------------------------------------------
                    # 5. Alerts for User Feedback
                    # Displays temporary messages upon certain actions like saving/loading
                    # -----------------------------------------------------------------------------
                    dbc.Alert(
                        id='save-alert',
                        is_open=False,          # Initially hidden
                        duration=4000,          # Auto-closes after 4 seconds
                        color='success',        # Bootstrap success color
                        children="Graph state saved!"  # Message content
                    ),
                    dbc.Alert(
                        id='load-alert',
                        is_open=False,
                        duration=4000,
                        color='info',
                        children="Graph state loaded!"
                    ),
                    dbc.Alert(
                        id='note-save-alert',
                        is_open=False,
                        duration=2000,          # Auto-closes after 2 seconds
                        color='success',
                        children="Note saved!"
                    )
                ],
                width=4  # Occupies approximately 34% of the row
            )
        ], className='mt-4'),  # Top margin for spacing
    ], fluid=True)  # Makes the container width adapt to the viewport

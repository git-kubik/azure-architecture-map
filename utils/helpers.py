# utils/helpers.py

import math
# from rapidfuzz import process, fuzz
import os
import json
import logging
import sqlite3
from contextlib import contextmanager

# Initialize logger for this module
logger = logging.getLogger(__name__)

# =============================================================================
# Configuration Variables
# =============================================================================

# Define a color palette for primary nodes
PRIMARY_NODE_COLORS = [
    '#1f77b4',  # Blue
    '#ff7f0e',  # Orange
    '#2ca02c',  # Green
    '#d62728',  # Red
    '#9467bd',  # Purple
    '#8c564b',  # Brown
    '#e377c2',  # Pink
    '#7f7f7f',  # Gray
    '#bcbd22',  # Olive
    '#17becf'   # Cyan
]

def create_stylesheet():
    """
    Returns the Cytoscape stylesheet.
    """
    stylesheet = [
        # General node styling
        {
            'selector': 'node',
            'style': {
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'center',
                'color': '#000',  # Text color
                'font-size': '12px',
                'shape': 'roundrectangle',
                'width': 'label',
                'height': 'label',
                'padding': '20px',
                'border-width': 2,
                'border-color': '#555',
                'background-color': 'data(color)',  # Dynamic color from node data
                'content': 'data(label)',
                'text-wrap': 'wrap',
                'text-max-width': '150px',
                'transition-property': 'background-color, border-color, width, height',
                'transition-duration': '0.3s'
            }
        },
        # Central Node Styling
        {
            'selector': '.central-node',
            'style': {
                'background-color': '#87CEEB',  # Specific color for central node
                'font-size': '16px',
                'font-weight': 'bold',
            }
        },
        # Primary Nodes Styling
        {
            'selector': '.primary-node',
            'style': {
                'background-color': 'data(color)',  # Inherits color from node data
            }
        },
        # Subnodes Styling
        {
            'selector': '.subnode',
            'style': {
                'background-color': 'data(color)',  # Inherits color from node data
            }
        },
        # Edge Styling
        {
            'selector': 'edge',
            'style': {
                'line-color': '#888',
                'width': 2,
                'target-arrow-shape': 'triangle',
                'target-arrow-color': '#888',
                'curve-style': 'bezier',
                'transition-property': 'line-color, width',
                'transition-duration': '0.3s'
            }
        },
        # Highlighted Node Styling
        {
            'selector': '.highlighted',
            'style': {
                'background-color': '#FFFF00',
                'border-width': 4,
                'border-color': '#000',
                'width': 'label',
                'height': 'label'
            }
        },
        # Selected Node Styling
        {
            'selector': ':selected',
            'style': {
                'border-width': 4,
                'border-color': '#000'
            }
        }
    ]
    logger.debug(f"Stylesheet created with {len(stylesheet)} style rules.")
    return stylesheet

# Database file path
DATABASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'graph_state.db')

# =============================================================================
# Database Management
# =============================================================================

@contextmanager
def get_db_connection():
    """
    Context manager for SQLite database connection.

    Yields:
        sqlite3.Connection: The SQLite database connection object.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        logger.debug(f"Connected to SQLite database at {DATABASE_FILE}")
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.debug("SQLite database connection closed.")

def initialize_db():
    """
    Initializes the SQLite database by creating the 'graph_state' table if it does not exist.
    """
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS graph_state (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    state TEXT NOT NULL
                )
            ''')
            conn.commit()
            logger.info("Database initialized and 'graph_state' table ensured.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

# Initialize the database when the module is imported
initialize_db()

# =============================================================================
# Utility Functions
# =============================================================================

def perform_fuzzy_search(search_value, all_labels):
    """
    Performs a case-insensitive substring search to find labels that contain the search value.

    Parameters:
        search_value (str): The search string input by the user.
        all_labels (list): The list of all node labels to search through.

    Returns:
        list: A list of labels that contain the search string as a substring.
    """
    if not search_value:
        logger.debug("Empty search value provided; returning empty match list.")
        return []

    try:
        # Convert search_value to lowercase for case-insensitive comparison
        search_value_lower = search_value.lower()
        # Find labels that contain the search_value as a substring
        matching_labels = [
            label for label in all_labels if search_value_lower in label.lower()
        ]
        logger.debug(f"Substring search results for '{search_value}': {matching_labels}")
        return matching_labels
    except Exception as e:
        logger.error(f"Error during substring search: {e}")
        return []

def lighten_color(hex_color, factor=0.5):
    """
    Lightens the given hex color by the specified factor.

    Parameters:
        hex_color (str): The original color in hex format (e.g., '#1f77b4').
        factor (float, optional): The factor by which to lighten the color (0 to 1).

    Returns:
        str: The lightened color in hex format.
    """
    try:
        # Remove the '#' prefix if present
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            # Expand shorthand hex color (e.g., 'abc' -> 'aabbcc')
            hex_color = ''.join([c*2 for c in hex_color])

        # Convert hex to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Calculate new RGB values
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)

        # Format back to hex
        lightened = '#{0:02X}{1:02X}{2:02X}'.format(r, g, b)
        logger.debug(f"Lightened color from #{hex_color} to {lightened} with factor {factor}")
        return lightened
    except Exception as e:
        logger.error(f"Error lightening color '{hex_color}': {e}")
        return hex_color  # Return original color in case of error

# =============================================================================
# Graph State Persistence Functions
# =============================================================================

def save_graph_state(state):
    """
    Saves the graph state to the SQLite database.

    Parameters:
        state (dict): The state dictionary containing elements, zoom, and pan.

    Returns:
        bool: True if saved successfully, False otherwise.
    """
    try:
        state_json = json.dumps(state)
        logger.debug(f"Saving graph state: {state_json}")
        with get_db_connection() as conn:
            c = conn.cursor()
            # Remove existing state to maintain only the latest
            c.execute('DELETE FROM graph_state')
            # Insert new state
            c.execute('INSERT INTO graph_state (state) VALUES (?)', (state_json,))
            conn.commit()
        logger.info("Graph state successfully saved to the database.")
        return True
    except sqlite3.Error as e:
        logger.error(f"SQLite error while saving graph state: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while saving graph state: {e}")
        return False

def load_graph_state():
    """
    Loads the graph state from the SQLite database.

    Returns:
        dict or None: The loaded state dictionary containing elements, zoom, and pan,
                      or None if no state is found.
    """
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            # Retrieve the latest graph state entry
            c.execute('SELECT state FROM graph_state ORDER BY id DESC LIMIT 1')
            row = c.fetchone()
            if row:
                state_json = row[0]
                state = json.loads(state_json)
                logger.info("Graph state successfully loaded from the database.")
                return state
            else:
                logger.warning("No graph state found in the database.")
                return None
    except sqlite3.Error as e:
        logger.error(f"SQLite error while loading graph state: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error while loading graph state: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while loading graph state: {e}")
        return None

# =============================================================================
# Graph Elements Construction
# =============================================================================

def load_graph_elements(central_node, primary_nodes, subnodes):
    """
    Constructs the graph elements for the Cytoscape component.

    Parameters:
        central_node (dict): The central node data.
        primary_nodes (dict): The primary nodes data.
        subnodes (dict): The subnodes data.

    Returns:
        list: A list of nodes and edges for the Cytoscape graph.
    """
    nodes = []
    edges = []

    # Add central node
    central_node_data = {
        'id': central_node['id'],
        'label': central_node['label'].replace('_', ' '),
        'description': central_node['description'],
        'notes': central_node.get('notes', ''),
        'color': '#87CEEB'  # Sky blue
    }
    nodes.append({
        'data': central_node_data,
        'classes': 'central-node'
    })
    logger.debug(f"Added central node: {central_node_data}")

    # Add primary nodes with assigned colors
    for i, (primary_id, primary_desc) in enumerate(primary_nodes.items()):
        color = PRIMARY_NODE_COLORS[i % len(PRIMARY_NODE_COLORS)]
        node_data = {
            'id': primary_id,
            'label': primary_id.replace('_', ' '),
            'description': primary_desc,
            'notes': '',
            'color': color
        }
        nodes.append({
            'data': node_data,
            'classes': 'primary-node'
        })
        logger.debug(f"Added primary node: {node_data}")

        # Create edge from central node to primary node
        edges.append({
            'data': {
                'source': central_node['id'],
                'target': primary_id,
                'id': f"{central_node['id']}_to_{primary_id}"
            }
        })

    # Add subnodes with lighter colors
    for parent_id, children in subnodes.items():
        parent_color = next((node['data']['color'] for node in nodes if node['data']['id'] == parent_id), '#FFFFFF')
        for child_id, child_desc in children.items():
            light_color = lighten_color(parent_color, factor=0.6)
            node_data = {
                'id': child_id,
                'label': child_id.replace('_', ' '),
                'description': child_desc,
                'notes': '',
                'color': light_color
            }
            nodes.append({
                'data': node_data,
                'classes': 'subnode'
            })
            logger.debug(f"Added subnode: {node_data}")

            # Create edge from primary node to subnode
            edges.append({
                'data': {
                    'source': parent_id,
                    'target': child_id,
                    'id': f"{parent_id}_to_{child_id}"
                }
            })

    logger.debug(f"Total nodes: {len(nodes)}, Total edges: {len(edges)}")
    return nodes + edges

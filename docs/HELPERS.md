# HELPERS.md

## Overview of `helpers.py`

The `helpers.py` file, located in the `utils` directory, contains utility functions that support various aspects of the Azure Architecture Map application. These functions are essential for tasks such as constructing graph elements, managing the database, handling search functionality, and defining styles for the graph visualization.

By centralizing these utilities, `helpers.py` promotes code reusability, maintainability, and a cleaner separation of concerns within the application.

---

## Table of Contents

- [Purpose of `helpers.py`](#purpose-of-helperspy)
- [Import Statements](#import-statements)
- [Configuration Variables](#configuration-variables)
- [Functions and Detailed Explanations](#functions-and-detailed-explanations)
  - [1. `create_stylesheet()`](#1-create_stylesheet)
  - [2. `perform_fuzzy_search(search_value, all_labels)`](#2-perform_fuzzy_searchsearch_value-all_labels)
  - [3. `initialize_db()`](#3-initialize_db)
  - [4. `get_db_connection()`](#4-get_db_connection)
  - [5. `save_graph_state(state)`](#5-save_graph_statestate)
  - [6. `load_graph_state()`](#6-load_graph_state)
  - [7. `load_graph_elements(central_node, primary_nodes, subnodes)`](#7-load_graph_elementscentral_node-primary_nodes-subnodes)
- [Integration with the Application](#integration-with-the-application)
- [Conclusion](#conclusion)
- [Additional Notes](#additional-notes)

---

## Purpose of `helpers.py`

- **Utility Functions**: Provides essential helper functions used throughout the application.
- **Modularity**: Centralizes common functionalities to avoid code duplication.
- **Database Management**: Handles interactions with the SQLite database for state persistence.
- **Graph Construction**: Assists in building the graph elements (nodes and edges) based on the data provided.
- **Search Functionality**: Implements the search logic used to highlight nodes based on user input.
- **Styling**: Defines the stylesheet for the Cytoscape graph component.

---

## Import Statements

```python
import math
import os
import json
import logging
import sqlite3
from contextlib import contextmanager

# Initialize logger for this module
logger = logging.getLogger(__name__)
```

- **math**: Provides mathematical functions, though it may not be heavily used in this module.
- **os**: Used for file system operations, such as constructing file paths.
- **json**: Handles serialization and deserialization of JSON data.
- **logging**: Enables logging of events for debugging and monitoring.
- **sqlite3**: Provides an interface for interacting with SQLite databases.
- **contextlib.contextmanager**: Used to create a context manager for database connections.

---

## Configuration Variables

```python
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

# Database file path
DATABASE_FILE = 'graph_state.db'
```

- **PRIMARY_NODE_COLORS**: A list of color codes used to assign colors to primary nodes in the graph.
- **DATABASE_FILE**: Specifies the filename for the SQLite database that stores the graph state.

---

## Functions and Detailed Explanations

### 1. `create_stylesheet()`

```python
def create_stylesheet():
    """
    Returns the Cytoscape stylesheet.
    """
    stylesheet = [
        # Default node style
        {
            'selector': 'node',
            'style': {
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'center',
                'background-color': '#0074D9',
                'color': '#fff',
                'width': '60px',
                'height': '60px',
                'font-size': '12px',
                'border-width': 2,
                'border-color': '#ccc',
                'transition-property': 'background-color, line-color, target-arrow-color',
                'transition-duration': '0.5s',
            }
        },
        # Style for edges
        {
            'selector': 'edge',
            'style': {
                'width': 2,
                'line-color': '#ccc',
                'target-arrow-color': '#ccc',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'arrow-scale': 1.5,
                'transition-property': 'background-color, line-color, target-arrow-color',
                'transition-duration': '0.5s',
            }
        },
        # Style for highlighted nodes
        {
            'selector': '.highlighted',
            'style': {
                'background-color': '#FF4136',
                'border-color': '#FFDC00',
                'border-width': 4,
                'color': '#fff',
                'font-weight': 'bold',
                'text-outline-color': '#FF4136',
                'text-outline-width': 2,
                'z-index': 9999,
            }
        },
        # Styles for specific classes of nodes can be added here
        # ...
    ]
    return stylesheet
```

#### Purpose

- Defines the visual styling of nodes and edges in the Cytoscape graph.
- Returns a list of style dictionaries that Cytoscape uses to render the graph elements.

#### Key Style Definitions

- **Node Styles**:
  - **label**: Displays the label from the node's data.
  - **background-color**: Sets the default node color.
  - **width** and **height**: Controls the size of the nodes.
  - **font-size**: Sets the size of the label text.
  - **border-width** and **border-color**: Defines the node's border appearance.
  - **transition-property** and **transition-duration**: Adds smooth transitions for style changes.

- **Edge Styles**:
  - **width**: Sets the thickness of the edges.
  - **line-color** and **target-arrow-color**: Sets the color of the edges and arrows.
  - **target-arrow-shape**: Defines the shape of the arrowheads.
  - **curve-style**: Determines how edges are curved.

- **Highlighted Nodes**:
  - Applied when nodes have the `'highlighted'` class (e.g., during search).
  - Changes background and border colors, increases border width, and brings the node to the front (`z-index`).

#### Integration

- Used in `graph.py` when creating the `GraphComponent`.
- Ensures consistent styling across the application.

### 2. `perform_fuzzy_search(search_value, all_labels)`

```python
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
```

#### Purpose

- Implements the search functionality used to highlight nodes based on user input.
- Performs a case-insensitive substring search on node labels.

#### Parameters

- **search_value**: The string entered by the user in the search input.
- **all_labels**: A list of all node labels present in the graph.

#### Returns

- A list of labels that contain the `search_value` as a substring.

#### How It Works

- Converts the `search_value` to lowercase to ensure case-insensitive comparison.
- Iterates over `all_labels`, checking if `search_value_lower` is a substring of each label (also converted to lowercase).
- Collects and returns the matching labels.

#### Integration

- Called in `callbacks.py` when handling search input.
- The returned list of matching labels is used to update the classes of nodes, adding the `'highlighted'` class to matching nodes.

### 3. `initialize_db()`

```python
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
```

#### Purpose

- Ensures that the SQLite database and the required table (`graph_state`) exist before the application attempts to read or write data.
- Creates the table if it does not already exist.

#### How It Works

- Opens a database connection using `get_db_connection()`.
- Executes a `CREATE TABLE IF NOT EXISTS` SQL statement to create the `graph_state` table with fields `id` and `state`.
- Commits the changes to the database.

#### Integration

- Called when `helpers.py` is imported, ensuring the database is ready for use when the application starts.
- Supports the state persistence features of the application.

### 4. `get_db_connection()`

```python
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
```

#### Purpose

- Provides a safe and consistent way to manage database connections.
- Ensures that the database connection is properly closed after operations are completed.

#### How It Works

- Uses the `@contextmanager` decorator to create a context manager.
- Opens a connection to the SQLite database specified by `DATABASE_FILE`.
- Yields the connection object to the calling function.
- Ensures the connection is closed in the `finally` block, even if an error occurs.

#### Integration

- Used by other database-related functions like `initialize_db()`, `save_graph_state()`, and `load_graph_state()` to manage database connections.

### 5. `save_graph_state(state)`

```python
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
```

#### Purpose

- Saves the current state of the graph to the database, allowing the user to restore it later.
- The state includes elements (nodes and edges), zoom level, and pan position.

#### Parameters

- **state**: A dictionary containing the graph's state data.

#### How It Works

- Serializes the `state` dictionary into a JSON string.
- Connects to the database and deletes any existing entries in the `graph_state` table to maintain only the latest state.
- Inserts the new state into the table.
- Commits the transaction.

#### Returns

- **True** if the state is saved successfully.
- **False** if an error occurs during the operation.

#### Integration

- Called in `callbacks.py` when the user clicks the "Save State" button.
- Enables state persistence between sessions.

### 6. `load_graph_state()`

```python
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
```

#### Purpose

- Retrieves the saved graph state from the database to restore the graph to its previous configuration.

#### Returns

- The state dictionary if a saved state is found.
- **None** if no state is found or an error occurs.

#### How It Works

- Connects to the database and retrieves the most recent entry from the `graph_state` table.
- Deserializes the JSON string back into a Python dictionary.
- Returns the state dictionary.

#### Integration

- Called in `callbacks.py` when the user clicks the "Load State" button.
- Allows users to restore their saved graph configurations.

### 7. `load_graph_elements(central_node, primary_nodes, subnodes)`

```python
def load_graph_elements(central_node, primary_nodes, subnodes):
    """
    Constructs the graph elements (nodes and edges) based on the provided data.

    Parameters:
        central_node (dict): The central node data.
        primary_nodes (dict): A dictionary of primary nodes and their descriptions.
        subnodes (dict): A nested dictionary of subnodes categorized under primary nodes.

    Returns:
        list: A list of elements (nodes and edges) for the Cytoscape graph.
    """
    elements = []

    # Add central node
    elements.append({
        'data': {
            'id': central_node['id'],
            'label': central_node['label'],
            'description': central_node.get('description', ''),
            'notes': central_node.get('notes', '')
        },
        'position': {'x': 0, 'y': 0},
        'classes': 'central-node'
    })

    # Add primary nodes
    angle = 0
    radius = 200
    angle_increment = 360 / len(primary_nodes)
    color_index = 0

    for node_id, description in primary_nodes.items():
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        elements.append({
            'data': {
                'id': node_id,
                'label': node_id,
                'description': description,
                'notes': ''
            },
            'position': {'x': x, 'y': y},
            'classes': f'primary-node color-{color_index}'
        })
        # Add edge from central node to primary node
        elements.append({
            'data': {
                'source': central_node['id'],
                'target': node_id
            }
        })
        angle += angle_increment
        color_index = (color_index + 1) % len(PRIMARY_NODE_COLORS)

    # Add subnodes
    for parent_id, children in subnodes.items():
        child_angle = 0
        child_radius = 100
        child_angle_increment = 360 / len(children) if len(children) > 0 else 0
        parent_position = next(
            (elem['position'] for elem in elements if elem['data']['id'] == parent_id), {'x': 0, 'y': 0})

        for child_id, description in children.items():
            x = parent_position['x'] + child_radius * math.cos(math.radians(child_angle))
            y = parent_position['y'] + child_radius * math.sin(math.radians(child_angle))
            elements.append({
                'data': {
                    'id': child_id,
                    'label': child_id,
                    'description': description,
                    'notes': ''
                },
                'position': {'x': x, 'y': y},
                'classes': 'sub-node'
            })
            # Add edge from primary node to subnode
            elements.append({
                'data': {
                    'source': parent_id,
                    'target': child_id
                }
            })
            child_angle += child_angle_increment

    return elements
```

#### Purpose

- Constructs the list of graph elements (nodes and edges) based on the data provided.
- Positions nodes in a circular layout around their parent nodes.

#### Parameters

- **central_node**: A dictionary containing the central node's data.
- **primary_nodes**: A dictionary where keys are primary node IDs and values are descriptions.
- **subnodes**: A nested dictionary where keys are primary node IDs, and values are dictionaries of subnode IDs and descriptions.

#### How It Works

- **Central Node**:
  - Added at position `(0, 0)` with the class `'central-node'`.
- **Primary Nodes**:
  - Positioned in a circle around the central node.
  - Uses trigonometric functions to calculate positions based on an angle and radius.
  - Assigned classes like `'primary-node color-0'`, where `color-0` corresponds to a color in `PRIMARY_NODE_COLORS`.
  - Edges are added connecting the central node to each primary node.
- **Subnodes**:
  - Positioned in a smaller circle around their respective primary nodes.
  - Positions are calculated relative to their parent node's position.
  - Assigned the class `'sub-node'`.
  - Edges are added connecting the primary node to each subnode.

#### Integration

- Called in `layout.py` to generate the elements passed to the `GraphComponent`.
- Enables dynamic construction of the graph based on the data in `data.py`.

---

## Integration with the Application

- **Graph Construction**: `load_graph_elements()` is essential for building the graph's nodes and edges based on the data provided.
- **Styling**: `create_stylesheet()` defines how the graph elements appear, ensuring a consistent and visually appealing presentation.
- **State Persistence**: `save_graph_state()` and `load_graph_state()` enable the application to save and restore the graph's state, enhancing user experience.
- **Database Management**: `initialize_db()` and `get_db_connection()` manage the SQLite database used for storing the graph state.
- **Search Functionality**: `perform_fuzzy_search()` provides the logic for searching and highlighting nodes based on user input.
- **Logging**: Throughout `helpers.py`, logging statements provide insights into the application's operations, aiding in debugging and monitoring.

---

## Conclusion

The `helpers.py` file is a cornerstone of the Azure Architecture Map application, providing essential utility functions that support core functionalities such as graph construction, styling, state persistence, and search. By encapsulating these utilities in a separate module, the application achieves better organization, reusability, and maintainability.

Understanding `helpers.py` allows developers to:

- **Modify and Extend Functionality**: Adapt the helper functions to support new features or changes in application requirements.
- **Debug and Optimize**: Use the logging statements and structured code to identify and fix issues.
- **Maintain Consistency**: Ensure that styles and behaviors remain consistent across the application.

---

## Additional Notes

- **Error Handling**: The functions in `helpers.py` include error handling to manage exceptions gracefully, preventing application crashes.
- **Extensibility**: Developers can extend the helper functions or add new ones to accommodate additional needs.
- **Performance Considerations**:
  - The use of mathematical calculations for positioning nodes should be efficient for the size of graphs used.
  - Database operations are straightforward but should be monitored if scaling up to larger datasets.

---

**By thoroughly understanding `helpers.py`, developers can effectively manage the utility aspects of the application, ensuring that all components work harmoniously to deliver a robust and user-friendly experience.**
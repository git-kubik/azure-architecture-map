# CALLBACKS.md

## Overview of `callbacks.py`

The `callbacks.py` file is a crucial part of the Azure Architecture Map Dash application. It contains all the callback functions that handle user interactions, enabling the app to respond dynamically to user input. Callbacks in Dash link user interface events with application logic, updating components based on user actions such as clicking buttons, typing in search fields, or interacting with graph elements.

This file defines a central callback function, `handle_interactions`, which manages multiple user interactions, including:

- Zoom controls (zoom in, zoom out, reset zoom)
- Saving and loading the graph state
- Searching and highlighting nodes
- Displaying node information and notes upon node selection
- Saving notes associated with nodes

---

## Table of Contents

- [Import Statements](#import-statements)
- [Callback Function Registration](#callback-function-registration)
  - [register_callbacks Function](#register_callbacks-function)
- [Combined Callback Function](#combined-callback-function)
  - [Inputs and States](#inputs-and-states)
  - [Outputs](#outputs)
  - [Callback Logic](#callback-logic)
    - [1. Context and Trigger Identification](#1-context-and-trigger-identification)
    - [2. Initialization of Outputs](#2-initialization-of-outputs)
    - [3. Handling Zoom Controls](#3-handling-zoom-controls)
    - [4. Handling Load State](#4-handling-load-state)
    - [5. Handling Save State](#5-handling-save-state)
    - [6. Handling Save Note](#6-handling-save-note)
    - [7. Handling Search](#7-handling-search)
    - [8. Handling Node Tap](#8-handling-node-tap)
- [Detailed Explanation](#detailed-explanation)
  - [Zoom Controls](#zoom-controls)
  - [State Persistence](#state-persistence)
  - [Notes Management](#notes-management)
  - [Search Functionality](#search-functionality)
  - [Node Interaction](#node-interaction)
- [How `callbacks.py` Fits into the Application](#how-callbackspy-fits-into-the-application)
- [Conclusion](#conclusion)

---

## Import Statements

```python
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import callback_context, html
import logging
import copy
from utils.helpers import perform_fuzzy_search, save_graph_state, load_graph_state
```

- **dash.dependencies**:
  - **Input**: Used to specify input components for callbacks.
  - **Output**: Used to specify output components that the callback updates.
  - **State**: Holds the state of components without triggering callbacks.
- **dash.exceptions.PreventUpdate**: Exception to prevent updates in a callback when no action is needed.
- **dash.callback_context**: Provides context about the callback, such as which input triggered it.
- **dash.html**: Contains HTML components used to create Dash layouts.
- **logging**: Python's built-in logging module for tracking events and debugging.
- **copy**: Provides functions for copying objects; `copy.deepcopy` is used to copy complex objects.
- **utils.helpers**:
  - **perform_fuzzy_search**: Function to perform case-insensitive substring searches.
  - **save_graph_state**: Function to save the current graph state to the database.
  - **load_graph_state**: Function to load a saved graph state from the database.

---

## Callback Function Registration

### `register_callbacks` Function

```python
def register_callbacks(app):
    """
    Registers all callbacks with the Dash app.

    Parameters:
        app (dash.Dash): The Dash application instance.
    """
    # Callback definitions...
```

- **Purpose**: This function is called from `app.py` to register all the callbacks defined in `callbacks.py` with the Dash application instance.
- **Parameter**:
  - **app**: The Dash application object to which the callbacks are registered.

---

## Combined Callback Function

A single callback function, `handle_interactions`, is defined to manage multiple user interactions. Combining multiple interactions into one callback helps avoid conflicts and allows for coordinated updates to the application's state.

```python
@app.callback(
    # Outputs, Inputs, and States...
)
def handle_interactions(
    # Parameters...
):
    # Callback logic...
```

### Inputs and States

#### Inputs

- **Zoom Controls**:
  - `Input('zoom-in', 'n_clicks')`
  - `Input('zoom-out', 'n_clicks')`
  - `Input('reset-zoom', 'n_clicks')`
- **State Persistence**:
  - `Input('load-state', 'n_clicks')`
  - `Input('save-state', 'n_clicks')`
- **Notes Management**:
  - `Input('save-note', 'n_clicks')`
- **Search Functionality**:
  - `Input('node-search', 'value')`
- **Node Interaction**:
  - `Input('cytoscape-graph', 'tapNodeData')`

#### States

- **Graph Elements**:
  - `State('cytoscape-graph', 'elements')`
- **Zoom Level**:
  - `State('cytoscape-graph', 'zoom')`
- **Pan Position**:
  - `State('cytoscape-graph', 'pan')`
- **Node Notes**:
  - `State('node-notes', 'value')`
- **Tapped Node Data**:
  - `State('cytoscape-graph', 'tapNodeData')`

### Outputs

- **Graph Updates**:
  - `Output('cytoscape-graph', 'elements')`
  - `Output('cytoscape-graph', 'zoom')`
  - `Output('cytoscape-graph', 'pan')`
- **Node Information Display**:
  - `Output('node-info', 'children')`
- **Notes Display and Management**:
  - `Output('rendered-notes', 'children')`
  - `Output('rendered-notes-section', 'style')`
  - `Output('node-notes', 'value')`
  - `Output('notes-section', 'style')`
- **Alerts**:
  - `Output('save-alert', 'is_open')`
  - `Output('load-alert', 'is_open')`
  - `Output('note-save-alert', 'is_open')`

### Callback Logic

The callback function follows a structured approach to handle different user interactions based on which input triggered the callback.

#### 1. Context and Trigger Identification

```python
ctx = callback_context

if not ctx.triggered:
    # No action triggered; do not update
    raise PreventUpdate

# Identify which input triggered the callback
triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
logger.info(f"Combined Callback triggered by: {triggered_id}")
```

- **callback_context**: Provides context about the current callback execution.
- **ctx.triggered**: A list containing information about the inputs that triggered the callback.
- **triggered_id**: Extracts the ID of the component that triggered the callback.
- **PreventUpdate**: Raises an exception to prevent any update if no input has triggered the callback.

#### 2. Initialization of Outputs

Before handling specific interactions, default values for all outputs are initialized.

```python
# Initialize default outputs
new_elements = copy.deepcopy(current_elements)
new_zoom = current_zoom
new_pan = current_pan
node_info = "Click on a node to see details."
rendered_notes = ''
rendered_notes_style = {'display': 'none'}
node_notes_value = ''
notes_section_style = {'display': 'none'}
save_alert = False
load_alert = False
note_save_alert = False
```

- **copy.deepcopy**: Creates a deep copy of the current graph elements to avoid modifying the original data.
- **Default Messages and Styles**: Sets default messages and styles for UI components.

#### 3. Handling Zoom Controls

```python
if triggered_id in ['zoom-in', 'zoom-out', 'reset-zoom']:
    # Zoom control logic...
```

- **Zoom In**: Increases the zoom level by a predefined factor.
- **Zoom Out**: Decreases the zoom level by the same factor.
- **Reset Zoom**: Resets the zoom level to the default value.
- **Zoom Limits**: Ensures the zoom level stays within defined minimum and maximum limits.

#### 4. Handling Load State

```python
elif triggered_id == 'load-state' and load_clicks:
    # Load state logic...
```

- **Load Graph State**: Retrieves the saved graph state from the database, including elements, zoom level, and pan position.
- **Update Outputs**: Updates the graph elements, zoom, and pan with the loaded state.
- **Alerts**: Sets the `load_alert` to `True` to display a success message.

#### 5. Handling Save State

```python
elif triggered_id == 'save-state' and save_clicks:
    # Save state logic...
```

- **Save Graph State**: Saves the current graph state to the database.
- **Alerts**: Sets the `save_alert` to `True` to display a success message.

#### 6. Handling Save Note

```python
elif triggered_id == 'save-note' and save_note_clicks:
    # Save note logic...
```

- **Update Node Notes**: Updates the `notes` field of the tapped node in the graph elements.
- **Update Display**: Immediately updates the displayed notes in the UI.
- **Alerts**: Sets the `note_save_alert` to `True` to display a success message.
- **Optional State Saving**: Optionally saves the updated graph state to persist the note changes.

#### 7. Handling Search

```python
elif triggered_id == 'node-search':
    # Search logic...
```

- **Clear Previous Highlights**: Removes the 'highlighted' class from all nodes.
- **Empty Search Query**: If the search input is empty, all highlights are removed, and a message is displayed.
- **Perform Search**: Uses `perform_fuzzy_search` to find matching node labels based on the search input.
- **Update Highlights**: Adds or removes the 'highlighted' class on nodes based on whether they match the search query.
- **Node Info Message**: Updates the node information message based on the search results.

#### 8. Handling Node Tap

```python
elif triggered_id == 'cytoscape-graph':
    # Node tap logic...
```

- **Extract Node Data**: Retrieves the label, description, and notes of the tapped node.
- **Update Node Information**: Displays the node's information and notes in the UI.
- **Manage Notes Section**: Shows or hides the notes sections based on whether the node has notes.

---

## Detailed Explanation

### Zoom Controls

- **Zoom Factor**: Defined as `zoom_factor = 0.2`, representing the increment or decrement in zoom level.
- **Zoom Limits**: Ensures `new_zoom` stays between `minZoom` (0.5) and `maxZoom` (2.0).
- **User Feedback**: Updates the graph's zoom level, providing immediate visual feedback to the user.

### State Persistence

- **Saving State**:
  - **State Content**: Saves `elements`, `zoom`, and `pan` to the database.
  - **Database Interaction**: Uses `save_graph_state` from `utils/helpers.py`.
  - **Alert**: Displays a success message upon successful save.
- **Loading State**:
  - **State Retrieval**: Loads the saved state from the database.
  - **State Application**: Updates the graph with the loaded state.
  - **Alert**: Displays a success message upon successful load.

### Notes Management

- **Saving Notes**:
  - **Node Identification**: Uses `tapped_node_state` to identify the node.
  - **Updating Elements**: Modifies the `notes` field in the node's data within `new_elements`.
  - **Immediate Update**: Updates the displayed notes without requiring further interaction.
  - **Optional State Saving**: Optionally saves the updated state to persist the changes.
- **Displaying Notes**:
  - **Rendered Notes**: Shows the notes in the UI under 'Notes:'.
  - **Visibility Control**: Manages the display styles to show or hide the notes sections.

### Search Functionality

- **Search Input**: Triggered whenever the user types in the search field.
- **Matching Logic**:
  - **Case-Insensitive Substring Search**: Finds nodes whose labels contain the search string, regardless of case.
  - **perform_fuzzy_search Function**: Used to perform the search, returning a list of matching labels.
- **Highlighting Nodes**:
  - **Classes Management**: Adds the 'highlighted' class to matching nodes and removes it from non-matching nodes.
  - **Dynamic Updates**: As the search input changes, the highlighting updates accordingly.
- **User Feedback**:
  - **Node Info Messages**: Provides messages to the user based on search results (e.g., "No matching nodes found.").

### Node Interaction

- **Node Selection**:
  - Triggered when a user clicks on a node in the graph.
- **Data Extraction**:
  - Retrieves `label`, `description`, and `notes` from the tapped node's data.
- **Information Display**:
  - Updates the 'Node Information' section with the selected node's details.
- **Notes Display**:
  - Shows the node's notes, if any, in the 'Notes' section.
  - Provides an input area for adding or editing notes.

---

## How `callbacks.py` Fits into the Application

- **Interaction Management**: Centralizes the handling of user interactions, ensuring a responsive and dynamic user experience.
- **Integration with Layout**:
  - The outputs and inputs correspond to component IDs defined in `layout.py`.
  - Updates UI components such as the graph, information panels, and alerts.
- **State Synchronization**:
  - Maintains synchronization between the application's state and the UI.
  - Ensures that changes in the UI reflect in the application's data and vice versa.
- **Performance Considerations**:
  - By combining multiple interactions into a single callback, it reduces the number of callback executions, optimizing performance.

---

## Conclusion

The `callbacks.py` file is a pivotal component of the Azure Architecture Map application, enabling interactivity and dynamic behavior. By managing user inputs and updating the application's state accordingly, it enhances the user experience, making the application more intuitive and responsive.

Understanding `callbacks.py` allows developers to:

- **Extend Functionality**:
  - Add new interactions or modify existing ones.
  - Implement additional features such as filtering, grouping, or custom behaviors.
- **Debug and Optimize**:
  - Use logging to track the application's behavior and identify issues.
  - Optimize callback logic for better performance.
- **Maintain Consistency**:
  - Ensure that the application's state remains consistent across different components and user interactions.
  - Maintain a coherent user experience by properly handling all possible user actions.

---

## Additional Notes

- **Error Handling**:
  - The callback function includes try-except blocks to catch and log exceptions, preventing the application from crashing and providing useful debugging information.
- **Preventing Unnecessary Updates**:
  - Uses `PreventUpdate` to avoid unnecessary updates when no relevant input has triggered the callback.
- **State Management**:
  - Carefully manages the application's state, making deep copies of mutable objects to prevent unintended side effects.
- **Callback Context**:
  - Utilizes `callback_context` to determine which input triggered the callback, allowing for precise control over the application's response to user actions.

By thoroughly understanding `callbacks.py`, developers can effectively manage the interactive aspects of the application, ensuring it remains robust, user-friendly, and adaptable to future requirements.
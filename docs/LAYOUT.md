# LAYOUT.md

## Overview of `layout.py`

The `layout.py` file defines the layout of the Azure Architecture Map Dash application. It constructs the user interface by organizing various components, such as the graph visualization, control panels, search bar, and information sections. The layout is built using Dash and Dash Bootstrap Components (DBC), leveraging Bootstrap's grid system for responsive design.

---

## Table of Contents

- [LAYOUT.md](#layoutmd)
  - [Overview of `layout.py`](#overview-of-layoutpy)
  - [Table of Contents](#table-of-contents)
  - [Import Statements](#import-statements)
  - [Function Definition](#function-definition)
    - [`get_layout` Function](#get_layout-function)
      - [Return Value](#return-value)
  - [Detailed Explanation](#detailed-explanation)
    - [1. Import Statements](#1-import-statements)
    - [2. Logging Setup](#2-logging-setup)
    - [3. `get_layout` Function](#3-get_layout-function)
      - [a. Graph Elements Construction](#a-graph-elements-construction)
      - [b. Layout Structure](#b-layout-structure)
        - [i. Main Container](#i-main-container)
        - [ii. Row and Column Layout](#ii-row-and-column-layout)
        - [iii. Components Included](#iii-components-included)
    - [4. Components Breakdown](#4-components-breakdown)
      - [a. Control Panel](#a-control-panel)
      - [b. Graph Component](#b-graph-component)
      - [c. Information Panel](#c-information-panel)
      - [d. Alerts](#d-alerts)
  - [How `layout.py` Fits into the Application](#how-layoutpy-fits-into-the-application)
  - [Customization](#customization)
    - [Adding or Modifying Components](#adding-or-modifying-components)
    - [Styling and Appearance](#styling-and-appearance)
  - [Conclusion](#conclusion)
  - [Additional Notes](#additional-notes)

---

## Import Statements

```python
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc
from components.graph import GraphComponent
from utils.helpers import create_stylesheet, load_graph_elements
from data import central_node, primary_nodes, subnodes
import logging
```

- **dash_bootstrap_components (dbc)**: Provides Bootstrap components for styling and layout.
- **dash_html_components (html)**: Contains HTML components to build the layout.
- **dash.dcc**: Dash Core Components, provides higher-level components like `Input`, `Slider`, `Graph`, etc.
- **GraphComponent**: Custom component from `components/graph.py`, defines the Cytoscape graph component.
- **create_stylesheet, load_graph_elements**: Utility functions from `utils/helpers.py` for graph styling and element construction.
- **central_node, primary_nodes, subnodes**: Data structures from `data.py` containing the graph's node data.
- **logging**: Python's built-in logging module for tracking events.

---

## Function Definition

### `get_layout` Function

```python
def get_layout():
    """
    Constructs and returns the layout of the Dash application.
    """
    # Function body...
```

#### Return Value

- **dbc.Container**: A Dash Bootstrap Components container that holds the entire layout of the application.

---

## Detailed Explanation

### 1. Import Statements

- **dash_bootstrap_components as dbc**: Imported as `dbc` for concise references to Bootstrap components like `Container`, `Row`, `Col`, `Button`, etc.
- **dash_html_components as html**: Provides HTML elements like `Div`, `H4`, `P`, used to structure the layout.
- **dash.dcc**: Provides higher-level components, such as `Input` for the search bar.
- **GraphComponent**: Imported to include the graph visualization in the layout.
- **Utilities and Data**: `create_stylesheet` and `load_graph_elements` are used to style and construct graph elements. Data for the nodes is imported from `data.py`.
- **logging**: Sets up logging for the module.

### 2. Logging Setup

```python
logger = logging.getLogger(__name__)
```

- **logger**: Creates a logger specific to the `layout.py` module for debugging and tracking.

### 3. `get_layout` Function

#### a. Graph Elements Construction

```python
# Construct the graph elements
elements = load_graph_elements(central_node, primary_nodes, subnodes)
```

- **load_graph_elements**: Function that constructs the list of graph elements (nodes and edges) based on the data provided.
- **elements**: The constructed list of elements to be used in the graph component.

#### b. Layout Structure

The layout is constructed using a combination of Bootstrap components to organize the UI into rows and columns.

##### i. Main Container

```python
return dbc.Container(
    # Children components...
    fluid=True,
    style={'padding': '0px'}
)
```

- **dbc.Container**: The main container for the layout.
- **fluid=True**: Makes the container responsive and full-width.
- **style**: Removes default padding to allow for edge-to-edge content.

##### ii. Row and Column Layout

The layout uses Bootstrap's grid system:

- **Rows**: Define horizontal groups of columns.
- **Columns**: Define vertical sections within a row.

##### iii. Components Included

The main layout includes:

- **Control Panel**: Contains zoom controls, save/load buttons, and the search bar.
- **Graph Component**: Displays the interactive graph.
- **Information Panel**: Shows node information and notes.

The components are arranged using `dbc.Row` and `dbc.Col` to control their placement and size.

---

### 4. Components Breakdown

#### a. Control Panel

```python
# Control Panel Column
dbc.Col(
    # Control Panel Content...
    width=3,
    style={'background-color': '#f8f9fa', 'padding': '15px'}
)
```

- **Width**: Occupies 3 out of 12 columns in the grid (25% of the width).
- **Style**: Light background color and padding for separation and readability.

**Control Panel Content Includes**:

- **Node Search**:
  ```python
  dbc.InputGroup(
      [
          dbc.InputGroupAddon("Search", addon_type="prepend"),
          dbc.Input(id='node-search', placeholder='Enter node name', type='text')
      ],
      className="mb-3"
  )
  ```
  - **dbc.InputGroup**: A Bootstrap component for grouping inputs and labels.
  - **node-search**: An input field for users to type in search queries.

- **Zoom Controls**:
  ```python
  dbc.ButtonGroup(
      [
          dbc.Button("Zoom In", id='zoom-in', color='primary'),
          dbc.Button("Zoom Out", id='zoom-out', color='primary'),
          dbc.Button("Reset Zoom", id='reset-zoom', color='secondary')
      ],
      className="mb-3"
  )
  ```
  - **dbc.ButtonGroup**: Groups the zoom control buttons.
  - **Button IDs**: Used in callbacks to handle user interactions.

- **Save/Load State Buttons**:
  ```python
  dbc.ButtonGroup(
      [
          dbc.Button("Save State", id='save-state', color='success'),
          dbc.Button("Load State", id='load-state', color='info')
      ],
      className="mb-3"
  )
  ```
  - **Functionality**: Allows users to save and load the graph's state.

- **Alerts**:
  ```python
  dbc.Alert("Graph state saved successfully.", id='save-alert', color='success', is_open=False, duration=4000),
  dbc.Alert("Graph state loaded successfully.", id='load-alert', color='info', is_open=False, duration=4000),
  ```
  - **dbc.Alert**: Displays messages when actions like save or load are performed.
  - **is_open**: Controlled by callbacks to show or hide the alert.

#### b. Graph Component

```python
# Graph Column
dbc.Col(
    GraphComponent(elements=elements, zoom=1, pan={'x': 0, 'y': 0}),
    width=6
)
```

- **Width**: Occupies 6 out of 12 columns (50% of the width).
- **GraphComponent**: The Cytoscape graph visualization.
- **Parameters**:
  - **elements**: The nodes and edges to display.
  - **zoom**: Initial zoom level.
  - **pan**: Initial pan position.

#### c. Information Panel

```python
# Information Panel Column
dbc.Col(
    # Information Panel Content...
    width=3,
    style={'background-color': '#f8f9fa', 'padding': '15px'}
)
```

- **Width**: Occupies 3 out of 12 columns (25% of the width).
- **Style**: Matches the control panel for consistency.

**Information Panel Content Includes**:

- **Node Information**:
  ```python
  html.Div(
      id='node-info',
      children="Click on a node to see details.",
      style={'whiteSpace': 'pre-wrap'}
  ),
  ```
  - **id='node-info'**: Used to display information about the selected node.

- **Rendered Notes Section**:
  ```python
  html.Div(
      [
          html.H5("Notes:"),
          html.Div(id='rendered-notes')
      ],
      id='rendered-notes-section',
      style={'display': 'none'}
  ),
  ```
  - **Notes Display**: Shows notes associated with the selected node.
  - **Visibility**: Controlled by the `style` attribute, toggled via callbacks.

- **Notes Editing Section**:
  ```python
  html.Div(
      [
          html.H5("Add/Edit Notes:"),
          dcc.Textarea(
              id='node-notes',
              placeholder='Enter notes here...',
              style={'width': '100%', 'height': 100}
          ),
          dbc.Button("Save Note", id='save-note', color='primary', className='mt-2'),
          dbc.Alert("Note saved successfully.", id='note-save-alert', color='success', is_open=False, duration=4000)
      ],
      id='notes-section',
      style={'display': 'none'}
  )
  ```
  - **Note Input**: A text area for users to add or edit notes.
  - **Save Note Button**: Triggers the saving of notes.
  - **Alert**: Confirms that the note was saved.
  - **Visibility**: Hidden by default, shown when a node is selected.

#### d. Alerts

- **Save Alert**: Notifies the user when the graph state is saved.
- **Load Alert**: Notifies the user when the graph state is loaded.
- **Note Save Alert**: Confirms that a note has been saved.

---

## How `layout.py` Fits into the Application

- **Layout Provider**: The `get_layout` function returns the layout, which is assigned to `app.layout` in `app.py`.
- **Integration of Components**:
  - **GraphComponent**: Imported and embedded in the layout.
  - **Control and Information Panels**: Provide user interaction points and display areas.
- **Callbacks**:
  - Components have IDs that are referenced in `callbacks.py` to handle user interactions.
- **Responsive Design**:
  - Uses Bootstrap's grid system to ensure the application is responsive across different screen sizes.

---

## Customization

### Adding or Modifying Components

- **Control Panel**:
  - Additional buttons or inputs can be added to the control panel by modifying the content within the control panel column.
- **GraphComponent**:
  - Parameters like initial zoom or pan can be adjusted.
- **Information Panel**:
  - More sections can be added to display additional information about nodes.

### Styling and Appearance

- **Bootstrap Themes**:
  - Change the theme by modifying the `external_stylesheets` parameter in `app.py`.
- **Custom Styles**:
  - Update `assets/styles.css` or inline styles to adjust the appearance.
- **Component Styles**:
  - Modify the `style` dictionaries for components to change their appearance.

---

## Conclusion

The `layout.py` file is responsible for constructing the visual structure of the Azure Architecture Map application. By organizing components into a responsive layout using Dash Bootstrap Components, it provides a user-friendly interface that integrates the graph visualization with control elements and information displays.

Understanding `layout.py` enables developers to:

- **Customize the Interface**: Add or modify components to enhance functionality.
- **Adjust Layout**: Rearrange components or change their sizes to improve the user experience.
- **Integrate New Features**: Incorporate additional visual elements or data displays.

---

## Additional Notes

- **Responsive Design**:
  - The use of Bootstrap's grid system ensures that the layout adjusts gracefully on different devices.
- **Component IDs**:
  - IDs assigned to components are crucial for callbacks; changing them requires updating the corresponding callbacks in `callbacks.py`.
- **Modular Design**:
  - By separating the layout construction into its own module, the application maintains a clear separation of concerns.

---

**By understanding `layout.py`, developers can effectively manage the user interface of the application, ensuring it is intuitive, responsive, and aligned with the application's functionality.**
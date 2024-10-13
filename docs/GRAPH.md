# GRAPH.md

## Overview of `graph.py`

The `graph.py` file, located in the `components` directory, defines the `GraphComponent` function, which creates and returns a Dash Cytoscape graph component. This component is responsible for rendering the interactive graph visualization of Azure services within the Dash application.

The graph displays nodes representing Azure services, organized into a hierarchy with edges indicating relationships. The `GraphComponent` function configures the graph's appearance, layout, and interactivity by specifying properties and styles.

---

## Table of Contents

- [Import Statements](#import-statements)
- [Function Definition](#function-definition)
  - [GraphComponent Function](#graphcomponent-function)
    - [Parameters](#parameters)
    - [Return Value](#return-value)
- [Detailed Explanation](#detailed-explanation)
  - [1. Import Statements](#1-import-statements)
  - [2. Logging Setup](#2-logging-setup)
  - [3. GraphComponent Function](#3-graphcomponent-function-1)
    - [a. Function Signature](#a-function-signature)
    - [b. Node and Edge Counts](#b-node-and-edge-counts)
    - [c. Cytoscape Component Creation](#c-cytoscape-component-creation)
      - [i. ID and Elements](#i-id-and-elements)
      - [ii. Layout](#ii-layout)
      - [iii. Style](#iii-style)
      - [iv. Stylesheet](#iv-stylesheet)
      - [v. Zoom and Pan](#v-zoom-and-pan)
      - [vi. User Interaction Settings](#vi-user-interaction-settings)
- [Understanding the Cytoscape Properties](#understanding-the-cytoscape-properties)
  - [Layout Options](#layout-options)
  - [Style and Appearance](#style-and-appearance)
  - [Stylesheet](#stylesheet)
- [How `graph.py` Fits into the Application](#how-graphpy-fits-into-the-application)
- [Conclusion](#conclusion)

---

## Import Statements

```python
import dash_cytoscape as cyto
from utils.helpers import create_stylesheet
import logging
```

- **dash_cytoscape**: The core library for integrating Cytoscape.js graphs into Dash applications.
- **create_stylesheet**: A utility function from `utils/helpers.py` that generates the stylesheet for the graph.
- **logging**: Python's built-in logging module used for debugging and tracking events within the module.

---

## Function Definition

### GraphComponent Function

```python
def GraphComponent(elements, zoom, pan):
    """
    Returns a Cytoscape graph component.
    """
    # Function body...
```

#### Parameters

- **elements (list)**: A list of dictionaries representing the nodes and edges of the graph.
- **zoom (float)**: The initial zoom level of the graph.
- **pan (dict)**: A dictionary specifying the initial pan position of the graph (e.g., `{'x': 0, 'y': 0}`).

#### Return Value

- **cyto.Cytoscape**: A configured Cytoscape component ready to be embedded in the Dash application layout.

---

## Detailed Explanation

### 1. Import Statements

```python
import dash_cytoscape as cyto
from utils.helpers import create_stylesheet
import logging
```

- **dash_cytoscape as cyto**: Imports the `dash_cytoscape` library and aliases it as `cyto` for convenience.
- **from utils.helpers import create_stylesheet**: Imports the `create_stylesheet` function, which generates the styles for the graph elements.
- **import logging**: Imports the logging module to enable logging within this module.

### 2. Logging Setup

```python
logger = logging.getLogger(__name__)
```

- **logger**: Creates a logger specific to the `graph.py` module, using `__name__` to set the logger's namespace.

### 3. GraphComponent Function

#### a. Function Signature

```python
def GraphComponent(elements, zoom, pan):
    """
    Returns a Cytoscape graph component.
    """
    # Function body...
```

- **GraphComponent**: The main function that creates and returns the Cytoscape graph component.

#### b. Node and Edge Counts

```python
node_count = sum(1 for elem in elements if 'source' not in elem['data'])
edge_count = sum(1 for elem in elements if 'source' in elem['data'])
logger.debug(f"Initializing GraphComponent with {node_count} nodes and {edge_count} edges. Zoom: {zoom}, Pan: {pan}.")
```

- **node_count**: Counts the number of nodes by iterating over `elements` and counting elements without a `'source'` key in their `'data'` dictionary (since edges have `'source'` and `'target'` keys).
- **edge_count**: Counts the number of edges by counting elements that have a `'source'` key in their `'data'`.
- **Logging**: Logs a debug message with the counts of nodes and edges, along with the initial zoom and pan values.

#### c. Cytoscape Component Creation

```python
return cyto.Cytoscape(
    id='cytoscape-graph',
    elements=elements,
    layout={'name': 'preset'},
    style={'width': '100%', 'height': '700px', 'border': '1px solid #ccc'},
    stylesheet=create_stylesheet(),
    minZoom=0.5,
    maxZoom=2.0,
    zoom=zoom,
    pan=pan,
    userZoomingEnabled=True,
    userPanningEnabled=True,
    boxSelectionEnabled=False,
    autoungrabify=False,
    responsive=True
)
```

- **cyto.Cytoscape**: Creates a Cytoscape component with specified properties.

Let's break down each parameter:

##### i. ID and Elements

- **id='cytoscape-graph'**: Assigns a unique ID to the Cytoscape component, used for callbacks and referencing in the Dash app.
- **elements=elements**: Sets the graph elements (nodes and edges) provided to the function.

##### ii. Layout

- **layout={'name': 'preset'}**: Specifies the layout algorithm to use. The `'preset'` layout uses positions specified in the elements, allowing for custom positioning and saving/loading of node positions.

##### iii. Style

- **style={'width': '100%', 'height': '700px', 'border': '1px solid #ccc'}**: Defines the style of the Cytoscape component container.
  - **width**: Sets the width to 100% of the parent container.
  - **height**: Sets the height to 700 pixels.
  - **border**: Adds a light gray border around the graph for visual separation.

##### iv. Stylesheet

- **stylesheet=create_stylesheet()**: Applies a stylesheet to the graph elements, defining the appearance of nodes and edges.
  - **create_stylesheet()**: A function imported from `utils/helpers.py` that returns a list of style dictionaries.

##### v. Zoom and Pan

- **minZoom=0.5**: Sets the minimum zoom level to 0.5x.
- **maxZoom=2.0**: Sets the maximum zoom level to 2.0x.
- **zoom=zoom**: Sets the initial zoom level, provided as a parameter to the function.
- **pan=pan**: Sets the initial pan position, provided as a parameter to the function.

##### vi. User Interaction Settings

- **userZoomingEnabled=True**: Allows users to zoom in and out of the graph.
- **userPanningEnabled=True**: Allows users to pan around the graph.
- **boxSelectionEnabled=False**: Disables box selection of multiple elements.
- **autoungrabify=False**: Allows nodes to be draggable if set to `False`.
- **responsive=True**: Ensures the graph responds to changes in the size of its container.

---

## Understanding the Cytoscape Properties

### Layout Options

- **Preset Layout**:
  - **Purpose**: Uses positions specified in the elements for node placement.
  - **Usage**: Ideal when you want to manually position nodes or load saved positions.
  - **Element Positions**: Each node element should include a `'position'` key with `'x'` and `'y'` coordinates.

### Style and Appearance

- **Container Style**:
  - **Width and Height**: The graph container is set to fill the width of its parent and has a fixed height.
  - **Border**: A border is added for visual distinction.

### Stylesheet

- **create_stylesheet() Function**:
  - **Location**: Defined in `utils/helpers.py`.
  - **Purpose**: Provides style definitions for nodes and edges.
  - **Styles Defined**:
    - **Nodes**: Styles for labels, colors, shapes, sizes, and transitions.
    - **Edges**: Styles for line colors, widths, arrow shapes, and transitions.
    - **Classes**: Special styles can be applied based on classes assigned to elements (e.g., `'highlighted'`, `'central-node'`).

---

## How `graph.py` Fits into the Application

- **Component Creation**: `GraphComponent` is responsible for creating the Cytoscape graph component used in the application.
- **Integration**:
  - **layout.py**: The `GraphComponent` function is imported and used in `layout.py` to include the graph in the app's layout.
  - **callbacks.py**: The graph's ID (`'cytoscape-graph'`) is used in callbacks to handle user interactions, such as tapping nodes or updating the graph state.
- **Dynamic Behavior**:
  - **Elements**: The `elements` parameter allows the graph to be updated with new nodes and edges dynamically.
  - **Zoom and Pan**: The `zoom` and `pan` parameters enable the application to control the view of the graph, essential for features like resetting zoom or restoring saved states.
- **User Interaction**:
  - **Draggable Nodes**: With `autoungrabify=False`, nodes can be dragged by the user, allowing for custom arrangement.
  - **Zooming and Panning**: Users can navigate the graph freely, enhancing the exploratory experience.

---

## Conclusion

The `graph.py` file plays a crucial role in the Azure Architecture Map application by defining the `GraphComponent` function that creates the interactive graph visualization. By configuring the Cytoscape component with specific properties and styles, it enables rich user interactions and a visually appealing representation of Azure services.

Understanding `graph.py` allows developers to:

- **Customize the Graph**:
  - Modify properties like layout, styles, and interaction settings.
  - Adjust the initial zoom and pan to focus on specific areas.
- **Enhance Functionality**:
  - Implement additional features by changing how nodes and edges are rendered.
  - Integrate new styles or classes for advanced visual effects.
- **Debug and Maintain**:
  - Use logging statements to troubleshoot issues related to the graph component.
  - Ensure compatibility with other parts of the application, such as callbacks and layout.

---

## Additional Notes

- **Extensibility**:
  - The `GraphComponent` can be extended to accept additional parameters for further customization.
  - Developers can modify the stylesheet returned by `create_stylesheet()` to change the appearance of graph elements.

- **Performance Considerations**:
  - For large graphs, consider optimizing the layout and interaction settings to maintain performance.
  - The choice of layout algorithm can significantly impact rendering speed and user experience.

- **Cytoscape.js Documentation**:
  - For more advanced configurations, refer to the [Cytoscape.js documentation](https://js.cytoscape.org/) to explore available options and properties.

---

By thoroughly understanding `graph.py`, developers can effectively manipulate the core visual component of the application, tailoring it to specific needs and enhancing the overall functionality of the Azure Architecture Map tool.
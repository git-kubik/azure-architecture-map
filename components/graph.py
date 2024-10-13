# components/graph.py

import dash_cytoscape as cyto
from utils.helpers import create_stylesheet
import logging

logger = logging.getLogger(__name__)

def GraphComponent(elements, zoom, pan):
    """
    Returns a Cytoscape graph component.
    """
    node_count = sum(1 for elem in elements if 'source' not in elem['data'])
    edge_count = sum(1 for elem in elements if 'source' in elem['data'])
    logger.debug(f"Initializing GraphComponent with {node_count} nodes and {edge_count} edges. Zoom: {zoom}, Pan: {pan}.")
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
        responsive=True,
        **{'autoRefreshLayout': True}  # Ensure layout updates with new positions
    )

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

def render_flow(diagram):
    """Render interactive visual pipeline using Plotly with better spacing"""

    if not diagram or diagram.get("type") != "flow":
        st.info("No pipeline diagram available.")
        return

    nodes = diagram.get("nodes", [])
    edges = diagram.get("edges", [])

    if not nodes:
        st.info("No nodes defined in diagram.")
        return

    # Create interactive visual flow with improved spacing
    create_interactive_flow_chart(nodes, edges)

def create_interactive_flow_chart(nodes, edges):
    """Create a beautiful interactive flow chart with better spacing"""

    # Calculate positions for vertical flow with more spacing
    positions = calculate_flow_positions(nodes, edges)

    # Create the plot
    fig = go.Figure()

    # Add connecting lines first (so they appear behind nodes)
    add_flow_connections(fig, positions, edges)

    # Add nodes
    add_interactive_nodes(fig, positions, nodes)

    # Style the chart with more height
    style_flow_chart(fig, len(nodes))

    # Display
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

    # Add interactive legend
    add_interactive_legend(nodes)

def calculate_flow_positions(nodes, edges):
    """Calculate optimal positions for nodes in a flow with better spacing"""

    positions = {}

    # Check if we have parallel processes
    parallel_steps = identify_parallel_steps(nodes)

    if parallel_steps:
        # Handle parallel processing layout with more spacing
        positions = calculate_parallel_layout(nodes, parallel_steps)
    else:
        # Simple vertical layout with increased spacing
        positions = calculate_vertical_layout(nodes)

    return positions

def identify_parallel_steps(nodes):
    """Identify steps that should be shown in parallel"""
    parallel_groups = []

    # Look for keyword matching steps
    keyword_steps = [n for n in nodes if any(word in n.lower() for word in ['exact', 'fuzzy', 'partial', 'synonym'])]

    if len(keyword_steps) > 1:
        parallel_groups.append({
            'steps': keyword_steps,
            'after_step': next((n for n in nodes if 'keyword' in n.lower() and n not in keyword_steps), None)
        })

    return parallel_groups

def calculate_vertical_layout(nodes):
    """Calculate positions for simple vertical flow with more spacing"""
    positions = {}

    # Increase spacing between nodes
    vertical_spacing = 3.0  # Increased from default

    for i, node in enumerate(nodes):
        positions[node] = {
            'x': 0,
            'y': (len(nodes) - i - 1) * vertical_spacing,  # More space between nodes
            'level': i
        }

    return positions

def calculate_parallel_layout(nodes, parallel_groups):
    """Calculate positions for layout with parallel processing and better spacing"""
    positions = {}
    vertical_spacing = 3.0  # Increased spacing
    current_y = len(nodes) * vertical_spacing

    for i, node in enumerate(nodes):
        # Check if this node is part of parallel processing
        is_parallel = False
        parallel_index = 0

        for group in parallel_groups:
            if node in group['steps']:
                is_parallel = True
                parallel_index = group['steps'].index(node)
                num_parallel = len(group['steps'])

                # Position parallel steps horizontally with more spacing
                x_offset = (parallel_index - (num_parallel - 1) / 2) * 3.0  # Increased horizontal spacing
                positions[node] = {
                    'x': x_offset,
                    'y': current_y - vertical_spacing,
                    'level': i,
                    'is_parallel': True
                }
                break

        if not is_parallel:
            positions[node] = {
                'x': 0,
                'y': current_y,
                'level': i,
                'is_parallel': False
            }
            current_y -= vertical_spacing * 1.5  # Extra space for main flow steps

    return positions

def add_flow_connections(fig, positions, edges):
    """Add connecting lines between nodes"""

    # Create smooth curved connections
    for edge in edges:
        if len(edge) == 2 and edge[0] in positions and edge[1] in positions:

            start_pos = positions[edge[0]]
            end_pos = positions[edge[1]]

            # Create curved line
            x_curve, y_curve = create_curved_line(
                start_pos['x'], start_pos['y'],
                end_pos['x'], end_pos['y']
            )

            fig.add_trace(go.Scatter(
                x=x_curve,
                y=y_curve,
                mode='lines',
                line=dict(
                    color='#3b82f6',
                    width=3,
                    shape='spline'
                ),
                hoverinfo='skip',
                showlegend=False,
                name='Flow'
            ))

            # Add arrow at end
            add_arrow(fig, end_pos['x'], end_pos['y'], start_pos['x'], start_pos['y'])

def create_curved_line(x1, y1, x2, y2):
    """Create smooth curved line between two points"""

    # Simple curve using control points
    steps = 20
    x_curve = []
    y_curve = []

    for i in range(steps + 1):
        t = i / steps

        # Bezier curve with control point offset
        control_x = (x1 + x2) / 2
        control_y = (y1 + y2) / 2 + 0.5  # Slightly more curve

        x = (1-t)**2 * x1 + 2*(1-t)*t * control_x + t**2 * x2
        y = (1-t)**2 * y1 + 2*(1-t)*t * control_y + t**2 * y2

        x_curve.append(x)
        y_curve.append(y)

    return x_curve, y_curve

def add_arrow(fig, x, y, from_x, from_y):
    """Add smaller arrow pointing to node"""

    # Calculate arrow direction
    dx = x - from_x
    dy = y - from_y
    length = math.sqrt(dx**2 + dy**2)

    if length > 0:
        # Normalize direction
        dx /= length
        dy /= length

        # SMALLER arrow size - reduced from 0.3 to 0.15
        arrow_size = 0.15

        # Arrow points
        arrow_x = [x - dx * arrow_size, x, x - dx * arrow_size]
        arrow_y = [y - dy * arrow_size + arrow_size/2, y, y - dy * arrow_size - arrow_size/2]

        fig.add_trace(go.Scatter(
            x=arrow_x,
            y=arrow_y,
            mode='lines',
            line=dict(color='#3b82f6', width=3),
            fill='toself',
            fillcolor='#3b82f6',
            hoverinfo='skip',
            showlegend=False
        ))

def add_interactive_nodes(fig, positions, nodes):
    """Add interactive nodes to the chart"""

    for node in nodes:
        pos = positions[node]
        config = get_node_config(node)

        # Add node circle - slightly larger for better visibility
        fig.add_trace(go.Scatter(
            x=[pos['x']],
            y=[pos['y']],
            mode='markers+text',
            marker=dict(
                size=90,  # Increased from 80
                color=config['color'],
                line=dict(color=config['border'], width=4),  # Thicker border
                symbol='circle'
            ),
            text=config['icon'],
            textfont=dict(size=28, color='white'),  # Larger icons
            textposition='middle center',
            hovertemplate=f"""
            <b>{node}</b><br>
            Type: {config['type']}<br>
            Description: {config['description']}<br>
            <extra></extra>
            """,
            name=config['type'],
            showlegend=False
        ))

        # Add text label below node - with more spacing
        fig.add_trace(go.Scatter(
            x=[pos['x']],
            y=[pos['y'] - 1.0],  # Increased from -0.6
            mode='text',
            text=[f"<b>{node}</b>"],
            textfont=dict(size=13, color='#1f2937'),  # Slightly larger text
            textposition='middle center',
            hoverinfo='skip',
            showlegend=False
        ))

def get_node_config(node):
    """Get visual configuration for each node type"""

    node_lower = node.lower()

    configs = {
        'input': {'color': '#10b981', 'border': '#065f46', 'icon': '📥', 'type': 'Input', 'description': 'Data ingestion and collection'},
        'preprocessing': {'color': '#3b82f6', 'border': '#1e40af', 'icon': '🔧', 'type': 'Processing', 'description': 'Data cleaning and standardization'},
        'keyword': {'color': '#f59e0b', 'border': '#92400e', 'icon': '🎯', 'type': 'Matching', 'description': 'Rule-based pattern matching'},
        'ai': {'color': '#8b5cf6', 'border': '#5b21b6', 'icon': '🤖', 'type': 'AI/ML', 'description': 'AI-powered classification'},
        'validation': {'color': '#06d6a0', 'border': '#047857', 'icon': '✅', 'type': 'Validation', 'description': 'Quality assurance'},
        'output': {'color': '#fb923c', 'border': '#c2410c', 'icon': '📤', 'type': 'Output', 'description': 'Result generation'},
        'automation': {'color': '#ef4444', 'border': '#991b1b', 'icon': '⚙️', 'type': 'Automation', 'description': 'Automated processing'}
    }

    # Match node to configuration
    for key, config in configs.items():
        if key in node_lower:
            return config

    # Default
    return {'color': '#6b7280', 'border': '#374151', 'icon': '🔹', 'type': 'Process', 'description': 'Data processing step'}

def style_flow_chart(fig, num_nodes):
    """Apply styling to the flow chart with dynamic height"""

    # Calculate height based on number of nodes and spacing
    chart_height = max(600, num_nodes * 150)  # More height per node

    fig.update_layout(
        title={
            'text': '🔄 Interactive Pipeline Flow',
            'x': 0.5,
            'font': {'size': 24, 'color': '#1f2937', 'family': 'Arial Bold'}
        },
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=80, b=60, l=60, r=60),  # More margins
        height=chart_height,
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-5, 5]  # Wider range for better spacing
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            autorange=True
        ),
        annotations=[
            dict(
                text="💡 Hover over nodes for details • Zoom and pan to explore",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.05,
                xanchor="center",
                font=dict(size=12, color="#6b7280")
            )
        ]
    )

def add_interactive_legend(nodes):
    """Add interactive legend showing step types"""

    st.markdown("### 🎨 Step Types")

    # Count step types
    step_types = {}
    for node in nodes:
        config = get_node_config(node)
        step_type = config['type']
        step_types[step_type] = step_types.get(step_type, 0) + 1

    # Display legend in columns
    cols = st.columns(len(step_types))

    for i, (step_type, count) in enumerate(step_types.items()):
        with cols[i]:
            config = next(get_node_config(node) for node in nodes if get_node_config(node)['type'] == step_type)
            st.markdown(f"""
            **{config['icon']} {step_type}**  
            *{count} step{'s' if count != 1 else ''}*
            """)

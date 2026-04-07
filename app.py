"""Streamlit app for artemether chiral center R/S visualization."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Artemether Drug Chiral Center Explorer", layout="wide")

st.title("Artemether Drug: Chiral Center Explorer")
st.write(
    "Public chemistry project for the **artemether drug**: visualize one representative "
    "stereocenter and switch between **R** and **S** configurations in 3D."
)

st.info(
    "Drug focus: **Artemether** (an antimalarial). "
    "This model is a simplified educational view of a single chiral center."
)

config = st.radio("Choose R/S configuration for the Artemether center", ["R", "S"], horizontal=True)

stereo_layouts = {
    "R": {
        "Priority 1: O-CH3": (1.4, 0.6, 0.6),
        "Priority 2: Drug ring fragment": (-1.2, 0.9, 0.35),
        "Priority 3: CH2 side fragment": (0.2, -1.1, 1.25),
        "Priority 4: H": (0.25, 0.05, -1.5),
    },
    "S": {
        "Priority 1: O-CH3": (1.4, 0.6, 0.6),
        "Priority 2: Drug ring fragment": (0.2, -1.1, 1.25),
        "Priority 3: CH2 side fragment": (-1.2, 0.9, 0.35),
        "Priority 4: H": (0.25, 0.05, -1.5),
    },
}

colors = {
    "C*": "#facc15",
    "Priority 1: O-CH3": "#f87171",
    "Priority 2: Drug ring fragment": "#60a5fa",
    "Priority 3: CH2 side fragment": "#34d399",
    "Priority 4: H": "#e5e7eb",
}

layout = stereo_layouts[config]

def build_2d_structure_figure() -> go.Figure:
    """Return a simplified 2D sketch highlighting a representative chiral center."""
    fig2d = go.Figure()

    # Simplified artemether-like framework (educational sketch, not exact coordinates)
    ring_x = [0, 1.1, 2.0, 1.5, 0.5, -0.2, 0]
    ring_y = [0, 0.7, 0.2, -0.9, -1.1, -0.4, 0]
    fig2d.add_trace(
        go.Scatter(
            x=ring_x,
            y=ring_y,
            mode="lines",
            line={"width": 3, "color": "#93c5fd"},
            name="2D skeleton",
            hoverinfo="skip",
        )
    )

    # Side groups (simplified)
    fig2d.add_trace(
        go.Scatter(
            x=[2.0, 2.8],
            y=[0.2, 0.9],
            mode="lines+text",
            text=["", "O-CH3"],
            textposition="top center",
            line={"width": 3, "color": "#fca5a5"},
            showlegend=False,
        )
    )
    fig2d.add_trace(
        go.Scatter(
            x=[-0.2, -1.0],
            y=[-0.4, -0.9],
            mode="lines+text",
            text=["", "CH3"],
            textposition="bottom center",
            line={"width": 3, "color": "#86efac"},
            showlegend=False,
        )
    )

    # Highlight representative chiral center
    fig2d.add_trace(
        go.Scatter(
            x=[1.1],
            y=[0.7],
            mode="markers+text",
            marker={"size": 16, "color": "#facc15", "line": {"color": "#111827", "width": 2}},
            text=["C*"],
            textposition="top right",
            name="Chiral center",
        )
    )

    fig2d.update_layout(
        title="2D structure view (simplified Artemether sketch)",
        xaxis={"visible": False},
        yaxis={"visible": False, "scaleanchor": "x", "scaleratio": 1},
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
    )
    return fig2d


fig = go.Figure()

# Central stereocenter
fig.add_trace(
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode="markers+text",
        marker={"size": 12, "color": colors["C*"]},
        text=["C*"],
        textposition="top center",
        name="Stereocenter",
    )
)

for label, (x, y, z) in layout.items():
    # Bond line from center atom to substituent
    fig.add_trace(
        go.Scatter3d(
            x=[0, x],
            y=[0, y],
            z=[0, z],
            mode="lines",
            line={"color": "#cbd5e1", "width": 5},
            showlegend=False,
            hoverinfo="skip",
        )
    )

    # Substituent atom and label
    fig.add_trace(
        go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode="markers+text",
            marker={"size": 8, "color": colors[label]},
            text=[label],
            textposition="top center",
            name=label,
        )
    )

fig.update_layout(
    margin={"l": 0, "r": 0, "t": 20, "b": 0},
    scene={
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "zaxis": {"visible": False},
        "camera": {"eye": {"x": 1.5, "y": 1.2, "z": 1.2}},
        "aspectmode": "cube",
        "bgcolor": "#020617",
    },
    paper_bgcolor="#020617",
    plot_bgcolor="#020617",
    legend={"orientation": "h", "yanchor": "bottom", "y": -0.1, "x": 0},
)

left_col, right_col = st.columns([1, 1.3])

with left_col:
    st.plotly_chart(build_2d_structure_figure(), use_container_width=True)
    st.caption("2D representation for the Artemether chiral compound (educational sketch).")

with right_col:
    st.plotly_chart(fig, use_container_width=True)

clockwise = "clockwise" if config == "R" else "counterclockwise"
st.success(
    f"{config} configuration: with priority 4 pointed away, "
    f"1 → 2 → 3 traces {clockwise}."
)

st.subheader("How R/S assignment works")
st.markdown(
    """
1. Assign substituent priorities (1 highest to 4 lowest) using Cahn–Ingold–Prelog rules.
2. Orient priority 4 away from the viewer.
3. Trace 1 → 2 → 3:
   - clockwise = **R**
   - counterclockwise = **S**

Artemether contains multiple chiral centers; this app intentionally focuses on one
representative tetrahedral center to teach stereochemistry clearly.
"""
)

st.subheader("Chiral compound details")
st.markdown(
    """
- **Compound name:** Artemether  
- **Type:** Chiral antimalarial drug  
- **Molecular formula:** C16H26O5  
- **Note:** Artemether has multiple chiral centers; this app highlights one representative center for R/S learning.
"""
)

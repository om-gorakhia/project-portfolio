import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

def render_chart(spec):
    """Render interactive charts using Plotly with error handling"""

    data_path = Path(spec["data_path"])
    if not data_path.exists():
        st.warning(f"⚠️ Data file not found: {spec['data_path']}")
        st.info("This chart will be available when data is provided.")
        return

    try:
        df = pd.read_csv(spec["data_path"])
        st.markdown(f"### 📊 {spec.get('title','Chart')}")
        if spec.get("description"):
            st.caption(spec["description"])

        # Special case: trend classification counts
        if "trend_classification.csv" in spec["data_path"]:
            # Melt and count patterns
            dfm = df.melt(
                id_vars=["month"],
                value_vars=["visit_trend","revenue_trend","item_trend"],
                var_name="metric",
                value_name="trend_pattern"
            )
            dfc = dfm["trend_pattern"].value_counts().reset_index()
            dfc.columns = ["trend_pattern","count"]
            fig = px.bar(
                dfc,
                x="trend_pattern",
                y="count",
                color="trend_pattern",
                title=spec.get("title",""),
                labels={"count":"Count","trend_pattern":"Pattern"}
            )

        # Special case: GMS revenue by platform and tier
        elif "cluster_revenue_platform.csv" in spec["data_path"]:
            fig = px.bar(
                df,
                x=spec["x"],
                y=spec["y"],
                color=spec.get("color"),
                barmode="group",
                title=spec.get("title",""),
                hover_data=["sku_count","avg_price_bucket"]
            )

        else:
            # Standard chart types
            if spec["type"] == "bar":
                fig = px.bar(
                    df,
                    x=spec["x"],
                    y=spec["y"],
                    color=spec.get("color"),
                    title=spec.get("title",""),
                    hover_data=df.columns.tolist()
                )
            elif spec["type"] == "line":
                fig = px.line(
                    df,
                    x=spec["x"],
                    y=spec["y"],
                    color=spec.get("color"),
                    title=spec.get("title",""),
                    markers=True,
                    hover_data=df.columns.tolist()
                )
            elif spec["type"] == "scatter":
                fig = px.scatter(
                    df,
                    x=spec["x"],
                    y=spec["y"],
                    color=spec.get("color"),
                    size=spec.get("size"),
                    title=spec.get("title",""),
                    hover_data=df.columns.tolist()
                )
            elif spec["type"] == "pie":
                fig = px.pie(
                    df,
                    values=spec["y"],
                    names=spec.get("color",spec["x"]),
                    title=spec.get("title","")
                )
            elif spec["type"] == "histogram":
                fig = px.histogram(
                    df,
                    x=spec["x"],
                    color=spec.get("color"),
                    title=spec.get("title","")
                )
            else:
                fig = px.bar(
                    df,
                    x=spec["x"],
                    y=spec["y"],
                    color=spec.get("color")
                )

        fig.update_layout(
            height=500,
            showlegend=True,
            hovermode='x unified',
            font=dict(size=12),
            title_font_size=16,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 View Raw Data"):
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Data as CSV",
                data=csv,
                file_name=f"{spec.get('title','chart_data').lower().replace(' ','_')}.csv",
                mime='text/csv'
            )

    except Exception as e:
        st.error(f"❌ Error rendering chart: {str(e)}")
        st.info("Please check the data format and column names.")

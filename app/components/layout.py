import streamlit as st
from components.charts import render_chart
from components.pipeline_diagram import render_flow
import pandas as pd
from pathlib import Path

def pill(text, color="#2563eb"):
    st.markdown(f"""<span style="background:{color};color:white;padding:4px 10px;border-radius:999px;margin-right:6px;font-size:12px;">{text}</span>""", unsafe_allow_html=True)

def render_navigation():
    """Add navigation breadcrumbs and back button"""

    # Check if we're on a project page
    if "project" in st.query_params:
        project_key = st.query_params["project"]

        # Create navigation bar
        col1, col2, col3 = st.columns([2, 6, 2])

        with col1:
            # Back to home button
            if st.button("⬅️ Back to Portfolio", use_container_width=True):
                st.query_params.clear()
                st.rerun()

        with col2:
            # Breadcrumb navigation
            st.markdown("""
            <div style="
                text-align: center; 
                padding: 10px; 
                background: #f8fafc; 
                border-radius: 10px;
                margin: 10px 0;
            ">
                <span style="color: #6b7280;">📁 Portfolio</span> 
                <span style="color: #3b82f6;"> > </span>
                <span style="color: #1f2937; font-weight: 600;">Current Project</span>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            # Project counter or additional nav
            st.markdown(f"""
            <div style="
                text-align: center; 
                padding: 10px; 
                color: #6b7280;
                font-size: 12px;
            ">
                Project View
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")


def render_about_section():
    # Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 20px;">
      <h1 style="margin:0; font-size:2.5rem;">👋 About Om Gorakhia</h1>
      <p style="opacity:0.9; font-size:1.1rem;">Business Analytics Graduate | Data Scientist | AI/ML Engineer</p>
    </div>
    """, unsafe_allow_html=True)

    # Contact & Status
    with st.expander("📞 Contact & Current Status", expanded=False):
        st.write("- **Phone:** +65-87392368")
        st.write("- **Email:** e1519898@u.nus.edu")
        st.write("- **LinkedIn:** linkedin.com/in/omgorakhia")
        st.write("- **Program:** MS Business Analytics, NUS (Jul 2025–Present)")

    # Professional Summary
    with st.expander("💼 Professional Summary", expanded=False):
        st.markdown("""
        Experienced **Business Analyst** and **Data Scientist** with 2+ years transforming
        complex business challenges into data-driven solutions.
        - 🎯 **Strategic Analytics:** Partnered with C-level for B2B data frameworks  
        - 🤖 **AI/ML Engineering:** Built predictive and NLP systems at enterprise scale  
        - 📊 **Business Impact:** Drove $2M+ in insights, 40% conversion lift  
        - 👥 **Leadership:** Managed teams of 4+ data engineering interns
        """)

    # Education
    with st.expander("🎓 Education", expanded=False):
        st.markdown("""
        **NUS Business School, Singapore**  
        • Master of Science in Business Analytics (Jul 2025–Present)  

        **Pandit Deendayal Energy University, India**  
        • B.Tech in ICT (Aug 2019–May 2023) — CGPA: 8.75/10
        """)

    # Technical Expertise
    with st.expander("🛠️ Technical Expertise", expanded=False):
        st.write("**Programming & Development:** Python, R, SQL, PostgreSQL, API Integration")
        st.write("**Data Science & AI:** LLMs, NLP, TensorFlow, BERT, Machine Learning")
        st.write("**Analytics & Modeling:** Regression, A/B-Testing, Predictive Analytics")
        st.write("**BI & Visualization:** Power BI, Excel Dashboards")
        st.write("**Automation & Platforms:** Power Apps, N8N, No-Code Workflows")

    # Key Achievements
    with st.expander("🏆 Key Achievements", expanded=False):
        st.markdown("""
        - 🎯 **94% Accuracy** in NLP-based industry classification  
        - 📈 **40% Conversion Lift** via no-code lead qualification platform  
        - 💰 **$2M+ Insights** delivered to Fortune 500 clients  
        - 👥 **Team Leadership:** Managed 4+ data engineering interns  
        - 🚀 **Entrepreneurial:** Co-founded events startup for 1,000+ attendees
        """)

    # Languages
    with st.expander("🌐 Languages", expanded=False):
        st.write("- **English:** Fluent")
        st.write("- **Hindi:** Native")


def render_home(projects):
    """Enhanced home page with better navigation and about section"""

    # Add About section first
    render_about_section()

    # Quick stats
    st.markdown("### 📊 Portfolio Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Projects", len(projects))

    with col2:
        ai_projects = len([p for p in projects if any('ai' in tag.lower() for tag in p.get('tags', []))])
        st.metric("AI/ML Projects", ai_projects)

    with col3:
        nlp_projects = len([p for p in projects if any('nlp' in tag.lower() for tag in p.get('tags', []))])
        st.metric("NLP Projects", nlp_projects)

    with col4:
        total_tags = len(set([tag for p in projects for tag in p.get('tags', [])]))
        st.metric("Technologies", total_tags)

    st.markdown("---")

    # Projects grid with improved cards
    st.markdown("### 🚀 Featured Projects")

    for i in range(0, len(projects), 2):
        cols = st.columns(2)

        for j, col in enumerate(cols):
            if i + j < len(projects):
                project = projects[i + j]

                with col:
                    render_project_card_clean(project, i + j + 1)

def render_project_card_clean(project, index):
    """Render clean project card using only Streamlit components"""

    # Create a container with clean styling
    with st.container():
        # Project header
        st.markdown(f"### {index}. {project['title']}")

        # Project summary
        st.write(project['summary'])

        # Tags section
        if project.get("tags"):
            st.markdown("**🏷️ Technologies:**")
            for tag in project["tags"]:
                pill(tag)
            st.markdown("")

        # Action buttons
        col1, col2 = st.columns([3, 1])

        with col1:
            if st.button(f"🔍 Explore Project", key=f"explore_{project['key']}", use_container_width=True):
                st.query_params["project"] = project["key"]
                st.rerun()

        with col2:
            # Quick info button
            with st.popover("ℹ️"):
                st.write("**Quick Info:**")
                if project.get("tools"):
                    st.write("🛠️ **Tools:**", ", ".join(project["tools"][:3]))
                if project.get("impact"):
                    st.write("📈 **Key Impact:**", project["impact"][0] if project["impact"] else "N/A")

        # Add spacing between cards
        st.markdown("---")

def render_project_page(project):
    """Enhanced project page with better navigation and layout"""

    # Add navigation first
    render_navigation()

    # Project header with enhanced styling
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    ">
        <h1 style="margin: 0; font-size: 2.2rem;">{project["title"]}</h1>
        <p style="margin: 15px 0 0 0; font-size: 1.1rem; opacity: 0.9;">{project.get("summary","")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Tags with improved styling
    if project.get("tags"):
        st.markdown("### 🏷️ Technologies & Methods")
        tag_cols = st.columns(len(project["tags"]))
        for i, tag in enumerate(project["tags"]):
            with tag_cols[i]:
                pill(tag)
        st.markdown("")

    # Create tabs for better organization
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "🔄 Pipeline", "📊 Visualizations", "📈 Impact", "💼 Resources"])

    with tab1:
        # Objectives section
        if project.get("objectives"):
            st.markdown("### 🎯 Project Objectives")
            for i, obj in enumerate(project.get("objectives", []), 1):
                st.markdown(f"**{i}.** {obj}")
            st.markdown("")

        # Tools section with better formatting
        if project.get("tools"):
            st.markdown("### 🛠️ Tools & Technologies")

            # Categorize tools
            tool_categories = {
                "Programming": [t for t in project["tools"] if any(lang in t.lower() for lang in ['python', 'sql', 'r'])],
                "AI/ML": [t for t in project["tools"] if any(ai in t.lower() for ai in ['ai', 'ml', 'powerapp', 'azure'])],
                "Data": [t for t in project["tools"] if any(data in t.lower() for data in ['excel', 'csv', 'db', 'database'])],
                "Other": []
            }

            # Assign remaining tools to "Other"
            assigned_tools = [tool for category in tool_categories.values() for tool in category]
            tool_categories["Other"] = [t for t in project["tools"] if t not in assigned_tools]

            for category, tools in tool_categories.items():
                if tools:
                    st.markdown(f"**{category}:**")
                    for tool in tools:
                        st.markdown(f"• {tool}")

    with tab2:
        st.markdown("### 🔄 Pipeline Architecture")
        render_flow(project.get("diagram", {}))

    with tab3:
        if project.get("visuals"):
            st.markdown("### 📊 Interactive Data Visualizations")
            for i, viz in enumerate(project["visuals"]):
                st.markdown(f"#### 📈 {viz.get('title', f'Visualization {i+1}')}")
                render_chart(viz)
                st.markdown("---")
        else:
            st.info("📊 Visualizations will be added as data becomes available.")

    with tab4:
        if project.get("impact"):
            st.markdown("### 📈 Project Impact & Results")

            # Display impact in cards
            for i, impact_item in enumerate(project["impact"]):
                impact_type = "efficiency" if "efficiency" in impact_item.lower() else "accuracy" if "accuracy" in impact_item.lower() else "general"

                icon_map = {
                    "efficiency": "⚡",
                    "accuracy": "🎯",
                    "general": "📈"
                }

                color_map = {
                    "efficiency": "#10b981",
                    "accuracy": "#3b82f6",
                    "general": "#8b5cf6"
                }

                st.markdown(f"""
                <div style="
                    background: {color_map[impact_type]}15;
                    border-left: 4px solid {color_map[impact_type]};
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                ">
                    <strong>{icon_map[impact_type]} {impact_item}</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📈 Impact metrics will be added upon project completion.")

    with tab5:
        if project.get("downloads"):
            st.markdown("### 💾 Download Resources")

            for download in project["downloads"]:
                path = Path(download["path"])
                if path.exists():
                    with open(path, "rb") as f:
                        st.download_button(
                            f"📁 {download['label']}",
                            data=f.read(),
                            file_name=path.name,
                            mime="text/csv" if path.suffix == ".csv" else "application/octet-stream"
                        )
                else:
                    st.info(f"📁 {download['label']} (file will be available soon)")
        else:
            st.info("📁 Downloadable resources will be added as they become available.")

        # Add project metadata
        st.markdown("---")
        st.markdown("### 📋 Project Metadata")

        metadata_col1, metadata_col2 = st.columns(2)

        with metadata_col1:
            st.markdown("**🔑 Project Key:** `" + project.get("key", "N/A") + "`")
            st.markdown("**📊 Visualization Count:** " + str(len(project.get("visuals", []))))

        with metadata_col2:
            st.markdown("**🏷️ Tag Count:** " + str(len(project.get("tags", []))))
            st.markdown("**🎯 Objective Count:** " + str(len(project.get("objectives", []))))

def add_sidebar_navigation(projects):
    """Add clean sidebar navigation WITHOUT extra empty lines"""

    with st.sidebar:
        st.markdown("### 🧭 Navigation")

        # Quick home link
        if st.button("🏠 Portfolio Home", use_container_width=True):
            st.query_params.clear()
            st.rerun()

        st.markdown("---")

        # Project quick links
        st.markdown("### 🚀 Quick Jump to Projects")

        for i, project in enumerate(projects, 1):
            if st.button(f"{i}. {project['title']}", key=f"sidebar_{project['key']}", use_container_width=True):
                st.query_params["project"] = project["key"]
                st.rerun()

        # Only add separator if there are filters below
        # REMOVED extra st.markdown("---") to eliminate empty space

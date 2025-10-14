import streamlit as st
from loaders.projects_loader import load_projects
from components.layout import render_project_page, render_home, add_sidebar_navigation

st.set_page_config(
    page_title="Analytics Projects Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom button styling */
.stButton button {
    border-radius: 10px;
    border: 2px solid #e5e7eb;
    transition: all 0.3s ease;
}

.stButton button:hover {
    border-color: #3b82f6;
    color: #3b82f6;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 12px 20px;
    font-weight: 600;
}

/* Metric styling */
.metric-container {
    background: white;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    text-align: center;
}

/* Sidebar styling */
.css-1d391kg {
    padding-top: 2rem;
}

/* Main content padding */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
</style>
""", unsafe_allow_html=True)

# Load projects
projects = load_projects("data/projects")

# Add sidebar navigation
add_sidebar_navigation(projects)

# Filter functionality in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔍 Filters")

    # Get all unique tags
    all_tags = sorted({t for p in projects for t in p.get("tags", [])})

    # Tag filter
    selected_tags = st.multiselect("Filter by Technology", options=all_tags, key="tag_filter")

    # Search filter
    search_term = st.text_input("🔎 Search Projects", key="search_filter")

    # Apply filters
    filtered_projects = []
    for project in projects:
        # Tag filter
        tag_match = True
        if selected_tags:
            tag_match = all(tag in project.get("tags", []) for tag in selected_tags)

        # Search filter
        search_match = True
        if search_term:
            search_text = (project.get("title", "") + " " + project.get("summary", "")).lower()
            search_match = search_term.lower() in search_text

        if tag_match and search_match:
            filtered_projects.append(project)

    # Show filter results
    if selected_tags or search_term:
        st.markdown(f"**📊 Showing {len(filtered_projects)} of {len(projects)} projects**")

# Main content area
st.markdown('<div class="main">', unsafe_allow_html=True)

# Route to appropriate page
if "project" in st.query_params:
    # Project detail page
    project_key = st.query_params["project"]
    current_project = next((p for p in projects if p["key"] == project_key), None)

    if current_project:
        render_project_page(current_project)
    else:
        st.error("🚫 Project not found!")
        st.info("The requested project does not exist or may have been moved.")

        if st.button("🏠 Return to Portfolio Home"):
            st.query_params.clear()
            st.rerun()
else:
    # Home page
    projects_to_show = filtered_projects if (selected_tags or search_term) else projects
    render_home(projects_to_show)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px 0;">
    <p>📊 <strong>Analytics Projects Portfolio</strong> | Built with Streamlit & Python | 
    <a href="#" style="color: #3b82f6; text-decoration: none;">Interactive Data Science Showcase</a></p>
</div>
""", unsafe_allow_html=True)

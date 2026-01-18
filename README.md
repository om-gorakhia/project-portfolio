# 📊 Analytics Projects Portfolio

**Interactive Streamlit-based Portfolio Showcase | Data Science & Business Analytics Projects**

![Python](https://img.shields.io/badge/Python-99.7%25-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🎯 Project Overview

An **interactive web-based portfolio application** built with Streamlit to showcase data analytics and business intelligence projects. Features a modern, user-friendly interface with dynamic project filtering, search capabilities, and detailed project presentations including visualizations, methodologies, and technical implementations.

**Key Highlight:** Fully functional portfolio website with sidebar navigation, multi-criteria filtering, and responsive design for optimal viewing across devices.

---

## ✨ Key Features

### 🔍 **Smart Project Discovery**
- **Technology-based Filtering**: Filter projects by tech stack (Python, Plotly, NetworkX, etc.)
- **Real-time Search**: Search across project titles and descriptions instantly
- **Dynamic Results Counter**: Live feedback showing filtered vs. total projects

### 🎨 **Professional Design**
- **Custom CSS Styling**: Modern UI with smooth transitions and hover effects
- **Responsive Layout**: Wide layout optimized for desktop viewing
- **Clean Interface**: Hidden Streamlit default elements for distraction-free browsing

### 📱 **Enhanced Navigation**
- **Sidebar Project Menu**: Quick access to all projects
- **URL-based Routing**: Direct links to individual project pages
- **Breadcrumb Navigation**: Easy return to portfolio home

### 📊 **Rich Project Pages**
- **Detailed Descriptions**: Comprehensive project summaries and objectives
- **Visual Demonstrations**: Embedded charts, graphs, and interactive visualizations
- **Technical Specifications**: Technologies used, methodologies applied
- **Impact Metrics**: Key achievements and business outcomes

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Framework** | Streamlit |
| **Data Processing** | Pandas, PyYAML |
| **Visualizations** | Plotly, Altair, Matplotlib |
| **Network Analysis** | NetworkX, PyVis |
| **File Management** | Pathlib |
| **Languages** | Python (99.7%), CSS (0.3%) |

---

## 📂 Project Structure

```
project-portfolio/
│
├── app/
│   ├── app.py                    # Main Streamlit application
│   ├── assets/                   # Images, icons, styling resources
│   ├── components/               # Reusable UI components
│   │   └── layout.py            # Page rendering functions
│   └── loaders/                  # Data loading utilities
│       └── projects_loader.py   # YAML project parser
│
├── Data/                         # Project data files (YAML format)
│   └── projects/                # Individual project configurations
│
├── docs/                         # Documentation files
│
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/om-gorakhia/project-portfolio.git
   cd project-portfolio
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd app
   streamlit run app.py
   ```

4. **Access the portfolio**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will automatically open in your default browser

---

## 💡 How It Works

### Data Loading
Projects are stored as YAML files in the `Data/projects/` directory. Each project file contains:
- Project metadata (title, summary, key)
- Technology tags for filtering
- Detailed descriptions
- Links to visualizations and resources

### Filtering & Search
The sidebar provides two filtering mechanisms:
1. **Tag Filter**: Select multiple technologies to find projects using specific tools
2. **Text Search**: Search by keywords in project titles or summaries

Filters work in combination - projects must match ALL selected criteria.

### Navigation
- **Home Page**: Displays all projects (or filtered subset) as cards
- **Project Pages**: Click any project to view detailed information
- **URL Parameters**: Direct links like `?project=loan-default` work for sharing

---

## 🎨 Customization

### Adding New Projects
1. Create a YAML file in `Data/projects/`
2. Follow the existing project structure:
   ```yaml
   key: project-key
   title: "Project Title"
   summary: "Brief description"
   tags: ["Python", "Plotly", "ML"]
   # Additional fields...
   ```
3. Restart the application - new project appears automatically!

### Styling
Custom CSS is embedded in `app.py`. Modify the `st.markdown()` section to adjust:
- Button styles and hover effects
- Tab appearances
- Metric containers
- Overall spacing and layout

---

## 📊 Use Cases

✅ **For Recruiters**: Quickly browse data analytics projects by technology
✅ **For Hiring Managers**: Assess technical skills across multiple domains
✅ **For Career Growth**: Document project portfolio in professional format
✅ **For Collaborators**: Share project work with stakeholders via clean interface

---

## 🎓 Skills Demonstrated

- **Web Development**: Streamlit application architecture
- **UI/UX Design**: Custom styling and responsive layouts
- **Data Engineering**: YAML parsing and dynamic content loading
- **Software Engineering**: Modular component design and clean code practices
- **Business Analytics**: Portfolio presentation optimized for analyst roles

---

## 📝 License

MIT License - Educational and research purposes.

---

## 👤 Author

**Om Gorakhia**
🎓 NUS MSBA Student | Sustainability | Analytics Enthusiast

---

## 🔗 Quick Links

- **Author Profile:** [@om-gorakhia](https://github.com/om-gorakhia)
- **Portfolio Website:** [View Live Projects](#)
- **LinkedIn:** [Connect with me](https://www.linkedin.com/in/om-gorakhia)

---

**📊 Analytics Projects Portfolio** | Built with Streamlit & Python | Interactive Data Science Showcase

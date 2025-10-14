import yaml, os, glob

def load_projects(path):
    projects = []
    for f in glob.glob(os.path.join(path, "*.yaml")):
        with open(f, "r", encoding="utf-8") as fh:
            projects.append(yaml.safe_load(fh))
    projects.sort(key=lambda x: x.get("title",""))
    return projects

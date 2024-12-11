import os
import yaml
import subprocess
import sys
from git import Repo
from pathlib import Path
import argparse

# Function to parse the YAML configuration file
def parse_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Function to extract commit dependencies
def extract_commit_dependencies(repo_path, target_file):
    repo = Repo(repo_path)
    commits = list(repo.iter_commits('--all'))
    dependency_graph = {}

    for commit in commits:
        files_changed = commit.stats.files.keys()
        if any(target_file in file for file in files_changed):
            dependency_graph[commit.hexsha] = list(files_changed)

    return dependency_graph

# Function to create a Mermaid graph representation
def create_mermaid_graph(dependency_graph):
    mermaid_graph = ["graph TD"]

    for commit, files in dependency_graph.items():
        commit_node = f"{commit[:7]}"
        for file in files:
            file_node = file.replace('/', '_').replace('.', '_')
            mermaid_graph.append(f"    {commit_node} --> {file_node}")

    return '\n'.join(mermaid_graph)

# Function to save the Mermaid graph to a file
def save_graph_to_file(graph_code, output_path):
    with open(output_path, 'w') as file:
        file.write(graph_code)

# Main function to handle CLI arguments and orchestrate operations
def main():
    parser = argparse.ArgumentParser(description="Visualize Git commit dependencies as a Mermaid graph.")
    parser.add_argument('--config', required=True, help="Path to the YAML configuration file.")

    args = parser.parse_args()
    config = parse_config(args.config)

    repo_path = config['repo_path']
    target_file = config['target_file']
    output_path = config['output_path']

    if not os.path.exists(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist.")
        sys.exit(1)

    dependency_graph = extract_commit_dependencies(repo_path, target_file)

    if not dependency_graph:
        print(f"No dependencies found for the file '{target_file}' in the repository.")
        sys.exit(0)

    mermaid_graph = create_mermaid_graph(dependency_graph)
    save_graph_to_file(mermaid_graph, output_path)

    print("Dependency graph has been successfully generated and saved.")
    print(mermaid_graph)

if __name__ == '__main__':
    main()

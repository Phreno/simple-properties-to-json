import argparse
import yaml
import sys

"""
given a texte `file` containing some properties, render a valid yaml file
"""
json_props = {}


def read_properties(file_name):
    """
    Given a `file_name`, returns the text of the file if exists, throw error otherwise
    """
    try:
        with open(file_name, 'r') as f:
            return f.read()
    except IOError:
        print("Error: file '{}' not found".format(file_name))
        sys.exit(1)


def filter_non_valuable_lines(properties):
    """
    Given `properties`, returns all the lines that valid and non comment
    """
    return [line for line in properties.split('\n') if line.strip() and not line.startswith('#')]


def update_properties_tree(line):
    """
    Given a `line` that represent a property path, split on each point to create a nested property and update the value
    """
    prop = line.split("=")[0].strip()
    val = line.split("=")[1].strip()
    path = prop.split('.')
    current_node = json_props
    for node in path[:-1]:
        if node not in current_node:
            current_node[node] = {}
        current_node = current_node[node]
    current_node[path[-1]] = val


def render_json(properties):
    """
    Given `properties`, render a yaml file
    """
    for line in filter_non_valuable_lines(properties):
        update_properties_tree(line)
    return json_props


def convert_json_to_yaml(json):
    """
    Given `json`, convert it to yaml
    """
    return yaml.dump(json, default_flow_style=False)


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        description='Convert a properties file to a yaml file')
    parser.add_argument('file', help='The file to convert')
    args = parser.parse_args()
    properties = read_properties(args.file)
    yaml_props = render_json(properties)
    print(convert_json_to_yaml(yaml_props))


if __name__ == '__main__':
    main()

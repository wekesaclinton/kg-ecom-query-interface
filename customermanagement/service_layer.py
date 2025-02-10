import json
import os
from rdflib import Graph, Namespace, Literal, URIRef



def process_request(request):
    g = load_model()
    try:
        if request['bind']:
            results = g.query(request['query'], initBindings=request['bind'])
        else:
            results = g.query(request['query'])
        results_list = []
        for row in results:
            # Convert each row (a tuple) into a dictionary:
            row_dict = {}
            for i, var in enumerate(results.vars):  # results.vars contains the variable names
                row_dict[str(var)] = str(row[i])  # Convert RDF terms to strings
            results_list.append(row_dict)
        # Now you can serialize the list of dictionaries to JSON:
        json_data = json.dumps(results_list)
        return json_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def data_to_obj_create_body(str_data):
    if str_data:
        try:
            data = json.loads(str_data)
            if isinstance(data, list):
                return data
            else:
                return []
        except Exception as e:
            return []
    else:
        return []

def load_ontology(file_path):
    """Loads an ontology from a Turtle file."""
    graph = Graph()
    try:
        graph.parse(file_path, format="turtle")  # Explicitly set the format
        return graph
    except Exception as e:
        print(f"Error loading ontology: {e}")  # Handle errors gracefully
        return None  # Or raise the exception if you prefer

def load_model():
    ontology_path = os.path.join(os.path.dirname(__file__), 'datafiles', 'ecommerce_inferred_ontology.ttl')  # Relative path
    return load_ontology(ontology_path)
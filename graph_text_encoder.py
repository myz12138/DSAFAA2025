
"""Library for encoding graphs in text."""

import networkx as nx

import name_dictionaries

TEXT_ENCODER_DICT = {
    "adjacency": name_dictionaries.create_name_dict("integer"),
    "incident": name_dictionaries.create_name_dict("integer"),
    "friendship": name_dictionaries.create_name_dict("popular"),
    "south_park": name_dictionaries.create_name_dict("south_park"),
    "got": name_dictionaries.create_name_dict("got"),
    "politician": name_dictionaries.create_name_dict("politician"),
    "social_network": name_dictionaries.create_name_dict("popular"),
    "expert": name_dictionaries.create_name_dict("alphabet"),
    "coauthorship": name_dictionaries.create_name_dict("popular"),
    "random": name_dictionaries.create_name_dict("random_integer"),
    "code": name_dictionaries.create_name_dict("integer"),
}


def create_node_string(name_dict, nnodes):
  node_string = ""
  for i in range(nnodes - 1):
    node_string += name_dict[i] + ", "
  #node_string += "and " + name_dict[nnodes - 1]
  node_string += name_dict[nnodes - 1]
  return node_string


def adjacency_encoder(node_list,edge_list, name_dict):
  """Encoding a graph as entries of an adjacency matrix."""
  graph=nx.Graph()
  for node in node_list:
       graph.add_node(node)
  graph.add_edges_from(edge_list)
  if graph.is_directed():
    output = (
        "In a directed graph, (i,j) means that there is an edge from node i to"
        " node j. "
    )
  else:
    output = (
        "In an undirected graph, (i,j) means that node i and node j are"
        " connected with an undirected edge. "
    )
  nodes_string = create_node_string(name_dict, len(graph.nodes()))
  output += "G describes a graph among nodes %s.\n" % nodes_string
  if graph.edges():
    output += "The edges in G are: "
  for i, j in graph.edges():
    output += "(%s, %s) " % (name_dict[i], name_dict[j])
  return output.strip() + ". "


def friendship_encoder(graph, name_dict):
  """Encoding a graph as a friendship graph."""
  if graph.is_directed():
    raise ValueError("Friendship encoder is not defined for directed graphs.")
  nodes_string = create_node_string(name_dict, len(graph.nodes()))
  output = (
      "G describes a friendship graph among nodes %s.\n" % nodes_string.strip()
  )
  if graph.edges():
    output += "We have the following edges in G:\n"
  for i, j in graph.edges():
    output += "%s and %s are friends.\n" % (name_dict[i], name_dict[j])
  return output


def coauthorship_encoder(graph, name_dict):
  """Encoding a graph as a coauthorship graph."""
  if graph.is_directed():
    raise ValueError("Coauthorship encoder is not defined for directed graphs.")
  nodes_string = create_node_string(name_dict, len(graph.nodes()))
  output = (
      "G describes a coauthorship graph among nodes %s.\n"
      % nodes_string.strip()
  )
  if graph.edges():
    output += "In this coauthorship graph:\n"
  for i, j in graph.edges():
    output += "%s and %s wrote a paper together.\n" % (
        name_dict[i],
        name_dict[j],
    )
  return output.strip() + ".\n"


def incident_encoder(node_list,edge_list, name_dict):
  """Encoding a graph with its incident lists."""
  graph=nx.Graph()
  for node in node_list:
       graph.add_node(node)
  graph.add_edges_from(edge_list)
  nodes_string = create_node_string(name_dict, len(graph.nodes()))
  output = "G describes a graph among nodes %s.\n" % nodes_string
  if graph.edges():
    output += "In this graph:\n"
  for source_node in graph.nodes():
    target_nodes = graph.neighbors(source_node)
    target_nodes_str = ""
    nedges = 0
    for target_node in target_nodes:
      target_nodes_str += name_dict[target_node] + ", "
      nedges += 1
    if nedges > 1:
      output += "Node %s is connected to nodes %s.\n" % (
          source_node,
          target_nodes_str[:-2],
      )
    elif nedges == 1:
      output += "Node %d is connected to node %s.\n" % (
          source_node,
          target_nodes_str[:-2],
      )
  return output


def social_network_encoder(graph, name_dict):
  """Encoding a graph as a social network graph."""
  if graph.is_directed():
    raise ValueError(
        "Social network encoder is not defined for directed graphs."
    )
  nodes_string = create_node_string(name_dict, len(graph.nodes()))
  output = (
      "G describes a social network graph among nodes %s.\n"
      % nodes_string.strip()
  )
  if graph.edges():
    output += "We have the following edges in G:\n"
  for i, j in graph.edges():
    output += "%s and %s are connected.\n" % (name_dict[i], name_dict[j])
  return output


def expert_encoder(graph, name_dict):
  nodes_string = create_node_string(name_dict, len(graph.nodes()))
  output = (
      "You are a graph analyst and you have been given a graph G among nodes"
      " %s.\n"
      % nodes_string.strip()
  )
  output += "G has the following undirected edges:\n" if graph.edges() else ""
  for i, j in graph.edges():
    output += "%s -> %s\n" % (name_dict[i], name_dict[j])
  return output

def code_encoder(graph,name_dict):
  nodes_string = create_node_string(name_dict, len(graph.nodes()))
  output=(
    "You are a graph analyst and you have been given a graph G represented in code form: Graph[name='G']{"
    "node_list=[%s];"
    %nodes_string.strip()
    )
  output+=' edge_list=['
  for i, j in graph.edges():
    output += "(%s <-> %s)," % (name_dict[i], name_dict[j])
  output+=']'
  return output

TEXT_ENCODER_FN = {
    "adjacency": adjacency_encoder,
    "incident": incident_encoder,
    "friendship": friendship_encoder,
    "south_park": friendship_encoder,
    "got": friendship_encoder,
    "politician": social_network_encoder,
    "social_network": social_network_encoder,
    "expert": expert_encoder,
    "coauthorship": coauthorship_encoder,
    "random": adjacency_encoder,
    'code':code_encoder,
}


def with_ids(graph, text_encoder):
  nx.set_node_attributes(graph, TEXT_ENCODER_DICT[text_encoder], name="id")
  return graph


def encode_graph(node_list,edge_list, text_encoder):
  """Encoding a graph according to the given text_encoder method."""
  name_dict = TEXT_ENCODER_DICT[text_encoder]
  return TEXT_ENCODER_FN[text_encoder](node_list,edge_list, name_dict)

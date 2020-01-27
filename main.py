import re
import click
import os
from graphviz import Digraph
import pygraphviz as pgv
import matplotlib.pyplot as plt

INCLUDE = re.compile('#include\s+[<"](.*)[">]')

def normalize(filename):
    return os.path.splitext(os.path.basename(filename))[0]

@click.command()
@click.argument('basedir', type=click.Path(exists=True))
def dgraph(basedir):
    G = Digraph()

    for root, dirs, files in os.walk(basedir):
        for fname in files:
            path = os.path.join(root, fname)

            with open(path, "r") as fp:
                includes = re.findall(INCLUDE, fp.read())

                for include in includes:
                    src = normalize(fname)
                    dst = normalize(include)

                    G.edge(src, dst)

    dot = pgv.AGraph(G.source)
    dot.draw('dependency_graph.svg', prog='dot')
    dot.write('dependency_graph.dot')


if __name__ == '__main__':
    dgraph()

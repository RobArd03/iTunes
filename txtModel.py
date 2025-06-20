from flet_core.icons import WHERE_TO_VOTE
from jinja2.nodes import FromImport

from model.model import Model

myModel = Model()
myModel.buildGraph(60)
n, e = myModel.getGraphDetails()
print(f"numero di nodi: {n}, Numero di archi {e}")







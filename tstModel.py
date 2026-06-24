from model.model import Model

mm = Model()
mm.buildGraph("peroxisome")
n,a= mm.getGraphDetails()
print(n,a)
edges = mm.getArchiPesoCres()
for e in edges:
    print(e)
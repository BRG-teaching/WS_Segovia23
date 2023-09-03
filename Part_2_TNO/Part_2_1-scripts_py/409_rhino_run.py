# This script should be run at Rhino Python Editor

from compas_tno.diagrams import FormDiagram
from compas_tno.plotters import TNOPlotter

ad = '/Users/mricardo/compas_dev/me/anagni/mesh-B/sangelo_vault_top_final_mesh-B_n_0.09_max.json'
form = FormDiagram.from_json(ad)

plt = TNOPlotter(form)
plt.draw_form_independents()
plt.draw_supports()
plt.show()
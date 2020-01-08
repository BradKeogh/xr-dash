# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
#

# %%
import panel as pn

pn.extension()


intro = pn.pane.Markdown("""
# Minimal Panel

Welcome! Minimal panel is a project by [Eric J. Ma](https://ericmjl.github.io) 
to showcase how to build a multi-source app using [`panel`](https://panel.pyviz.org),
a project that is part of the PyViz family of projects
sponsored by Anaconda and built by the Python data science community.
""")


contents = pn.pane.Markdown("""
## Contents

1. [HIV Drug Resistance Prediction](/minimal-panel)
2. [Iris Data Explorer](/iris)

The source repository is available [on GitHub](https://github.com/ericmjl/minimal-panel-app)
""")


# %%
#from utils import navpane - good exmaple of using external files with functions.
pn.Column(intro, contents).servable()


# %%




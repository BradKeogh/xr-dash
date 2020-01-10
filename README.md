# xr-dash
Repo to serve initial panel app for xr impact dashboard using Heroku free services.

The working online app is [here](https://xr-dash.herokuapp.com/main).

# Why this project exists
* To share python panel app for ongoing development.
* Provide a template to serve panel apps on heroku in future

# getting set up
You need heroku and git installed on your machine. Follow the walkthrough below for commands to serve locally and to push to heroku servers. 

# Resources to get this going:
* walkthrough for [python web apps](https://becominghuman.ai/steps-to-create-and-deploy-python-web-app-on-heroku-95b6c4f570b0)
* [heroku walkthrough](https://devcenter.heroku.com/articles/getting-started-with-python#define-a-procfile)
* [panel app example](https://github.com/ericmjl/minimal-panel-app)

# known issues

* Normally panel (and underneath bokeh) can serve app.ipynb files as well as app.py files. Currently .ipynb extensions do not appear to work due to the requirements.txt file not having all its conflicts solved. Ideally need someone who knows pip better than me to take a look at this.  

* for the hvplots we are using in the main.py file the pip environment does not work (there is some sort of conflict). The conda envrironment i use in windwos works (and serves locally using heroku fine). I think heroku server is linux and python 3.6.10.
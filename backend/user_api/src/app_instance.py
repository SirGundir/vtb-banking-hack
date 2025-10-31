from api.app import init_app, lifespan


app = init_app(lifespan, allow_origins=['*'], debug=True) # ToDo not inprod!

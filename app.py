# Here is where the app is just run.
from puppycompanyblog import app
# this is all the app.py will be doing and the whole heavy lifting will be done in the __init__.py in the puppycompanyblog folder.

if __name__=='__main__':
    app.run(debug=True)
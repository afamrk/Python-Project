from project import app, db
from project.models import User,Folder

import os

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Folder':Folder}

if __name__ == '__main__':
    app.run()

# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from tracker import create_app
from tracker.models import User, Comment, Expense
from tracker.extensions import db



app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run(host='0.0.0.0',port=5029)


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()




manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()

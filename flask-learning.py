#这个版本是没有MigrateCommand，且利用的是shell_context_processor而不是scripts的shell模块！
import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
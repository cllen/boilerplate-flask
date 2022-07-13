import os
import click

from applications import create_app

from data import insert_dev_data
from data import insert_test_data

from etc import config, DevelopmentConfig

config_setup = os.getenv('APP_CONFIG') or 'default'
config_class = config[config_setup]

app = create_app(config_setup)

def _deploy():
        
    print('>>>> environment model:',str(config_class))

    environment_models = ['default', 'development','production']
    if config_setup not in environment_models:
        raise Exception('>>>> environment model error! it must be in '+"".join(environment_models)+"!")

    if config_setup in ['development','default']:
        print('>>>> 1/3 droping databse...')
        app.db.drop_all()
        print('>>>> 2/3 create_all()...')
        app.db.create_all()
        app.db.session.commit()
        print('>>>> 3/3 inserting data into devlopment database...')
        insert_dev_data(app.db.session)
        app.db.session.commit()
        print('>>>> deployed development database successfully!')
        print('>>>> databse exists already! can not deploy again!')

    if config_setup == 'production':
        raise Exception(">>>> production model did not be implemented yet!")

# 运行测试程序命令
@app.cli.command('deploy')
def deploy():
    """deploys database"""
    _deploy()



# 运行测试程序命令
@app.cli.command('test')
@click.argument('test_names', nargs=-1)
def test(test_names=None):

    print('>>>> environment model:',str(config_class))

    """deploys database"""
    print('>>>> 1/3 droping databse...')
    app.db.drop_all()
    print('>>>> 2/3 create_all()...')
    app.db.create_all()
    app.db.session.commit()
    print('>>>> 3/3 inserting data into test database...')
    insert_test_data(app.db.session)
    app.db.session.commit()
    print('>>>> deployed development database successfully!')

    print('>>>> 1/3 setting up code coverage detector...')
    
    # code coverage detector.
    COV = None
    # if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='./*')
    COV.start()

    """runs tests"""
    print('>>>> 2/3 running tests...')

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


    """makes code coverage report"""
    print('>>>> 3/3 making code coverage report...')
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp','coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s' % os.path.join(covdir,'index.html'))
    
    print('>>>> has tests done!')

if __name__ == '__main__':
    app.run(debug=True, port='80')# ,port=80,host='0.0.0.0'

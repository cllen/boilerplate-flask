import os
import click

from applications import create_app

from data import insert_dev_data
# from tests import insert_test_data

from etc import config, DevelopmentConfig

config_setup = os.getenv('APP_CONFIG') or 'default'
config_class = config[config_setup]

app = create_app(config_setup)

def _depoly():
        
    print('当前运行环境：'+str(config_class))

    if not app.db.engine.table_names() or config_setup in ['testing', 'default', 'development']:

        if config_setup == 'testing':
            print('正在删除测试数据库...')
            app.db.drop_all()
            print('正在创建测试数据库...')
            app.db.create_all()
            app.db.session.commit()

            # pre_db(app.db.session)

        elif config_class == DevelopmentConfig:
            print('正在删除开发数据库...')
            app.db.drop_all()
            print('正在创建开发数据库...')
            app.db.create_all()
            app.db.session.commit()

        else:
            raise Exception('环境变量设置错误！')

        print('正在导入数据...')
        insert_dev_data(app.db.session)
        app.db.session.commit()

        print('创建数据库成功！')

    else:
        print('数据库已存在！不再创建！')

# 运行测试程序命令
@app.cli.command('deploy')
def deploy():
    _depoly()



# 运行测试程序命令
@app.cli.command('run-tests')
@click.argument('test_names', nargs=-1)
def run_tests(test_names=None):

    """
        初始化测试数据库
    """
    print('>>> 正在初始化数据库... <<<')

    print('1/2 正在创建数据表...')

    app.db.drop_all()
    app.db.create_all()
    # insert_test_data(app.db.session)
    app.db.session.commit()

    print('2/2 正在插入测试数据...')

        

        
    print('>>> 初始化数据库成功! <<<')
        
    print('>>> 正在运行测试...   ')
    """
        检测代码覆盖
    """
    COV = None
    # if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='./*')
    COV.start()

    """
        运行测试
    """
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    """
        生曾代码覆盖报告
    """
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)

if __name__ == '__main__':
    app.run(debug=True, port='80')# ,port=80,host='0.0.0.0'

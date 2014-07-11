
from envisage.core_plugin import CorePlugin
from envisage.ui.tasks.tasks_plugin import TasksPlugin

from pikos.apikos.application import ApikosApplication
from pikos.apikos.plugin import ApikosPlugin


def main(argv):
    from traits.etsconfig.etsconfig import ETSConfig
    ETSConfig.toolkit = 'qt4'

    plugins = [CorePlugin(), TasksPlugin(), ApikosPlugin()]
    app = ApikosApplication(plugins)
    app.run()


if __name__ == '__main__':
    import sys
    main(sys.argv)

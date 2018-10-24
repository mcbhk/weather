import logging


class TearDown:

    def __init__(self):
        self._teardown_list = []

    def teardown(self):
        """

        :return:
        """
        for name, function in self._teardown_list:
            logging.info("Tearing down '%s'" % name)
            function()

    def add_teardown_function(self, name, function):
        """

        :param function:
        :return:
        """
        self._teardown_list.append((name, function))

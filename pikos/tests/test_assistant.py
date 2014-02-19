class TestAssistant(object):

    def assertFieldValueExist(self, records, fields, values, times=None,
                              msg=None):
        """ Assert that the records containt a specific set of field entries.

        Parameters
        ----------
        records : iterateable
            An iterateable of records entrys to check.

        fields : list
            List of field names to look into

        value : tuple
            The corresponding value(s) to match over the fields of each entry.

        times : int
            The number of times that the value should be present in the fields.
            Default is to any number of times (i.e. None).

        msg : str
            overide the default assertion message.

        """
        count = 0
        for entry in records:
            data = [getattr(entry, field) for field in fields]
            if all(item == value for item, value in zip(data, values)):
                count += 1
        if times is None:
            msg = 'The value set {0} could not be found in the records'.\
                  format(zip(fields, values))
            self.assertGreater(count, 0, msg=msg)
        else:
            msg = ('The value set {0} was found {1} and not {2} times in the '
                   'records.'.format(zip(fields, values), count, times))
            self.assertEqual(count, times, msg=msg)

    def assertFieldValueNotExist(self, records, fields, values):
        """ Assert that the records do not containt a specific set of field
        entries.

        Parameters
        ----------
        records : iteratable
            An iterateable of records entrys to check.

        fields : list
            List of field names to look into

        value : tuple
            The corresponding value(s) to match over the fields of each entry.

        msg : str
            overide the default assertion message.

        """
        msg = 'The value set {0} was unexpectedly found in the records'.\
              format(zip(fields, values))
        self.assertFieldValueExist(records, fields, values, times=0, msg=msg)

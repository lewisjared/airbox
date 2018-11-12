

class BasePlotter(object):
    def get_day(self, d):
        """
        Extracts a days worth of data
        :param d: Date to extract (UTC TZ)
        :return: Pandas Dataset or None if no data is available
        """
        return None

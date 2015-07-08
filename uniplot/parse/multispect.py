"""Parses Kromek Multi-Spect files."""
import numpy
import os.path
import configparser


class MultiSpectParser:

    """Parses spectrum files from Kromek Multi-Spect."""

    def __init__(self, filename):
        """Set internal variables."""
        self._name = filename
        self._handle = None

    def isfiletype(self):
        """Determine if file came from Kromek Multi-Spect.

        First line should be '$SPEC_REM:' and the second should be
        'Multi-Spect'.
        """
        # open file, saving handle so we don't need to open again in parse()
        self._handle = open(self._name)
        # consume and save first two lines
        lines = [self._handle.readline().strip()]
        lines.append(self._handle.readline().strip())

        if lines[0] == '$SPEC_REM:' and lines[1] == 'Multi-Spect':
            return True
        else:
            self._handle.close()
            return False

    def parse(self):
        """Parse Multi-Spect file."""
        try:
            if self._handle.closed:
                raise Exception('{} was prematurely closed'.format(self._name))
        except AttributeError:
            raise Exception('{} was never opened'.format(self._name))

        data = {}
        data['labels'] = {}
        # TODO: make s \mathrm
        data['labels']['y'] = 'Intensity ($s^{-1}$)'
        # TODO: make this a dict when possible
        data['axes'] = []
        settings = self.settings()
        if 'title' in settings:
            data['title'] = settings['title']

        with self._handle as f:
            while True:
                line = f.readline()
                # TODO: we can actually recover from `line.strip() == '$DATA:'`
                if line == '' or line.strip() == '$DATA:':
                    raise Exception("'$MEAS_TIM:' was not found")
                elif line.strip() == '$MEAS_TIM:':
                    break

            time = float(f.readline().split()[0])

            while True:
                line = f.readline()
                if line == '':
                    raise Exception("'$DATA:' was not found")
                elif line.strip() == '$DATA:':
                    break

            # start and end are the first and last INDEX
            start, end = map(int, f.readline().split())
            x = numpy.arange(start, end+1)
            y = numpy.empty_like(x)
            for i in range(start, end+1):
                y[i] = int(f.readline())

            y = y/time

            while True:
                line = f.readline()
                if line == '':
                    break
                elif line.strip() == '$ENER_FIT:':
                    data['labels']['x'] = 'Energy (keV)'
                    m, c = map(float, f.readline().split())
                    x = m*x + c
                    break

            data['labels'].setdefault('x', 'Channel')

            if 'LowX' in settings:
                indices = float(settings['LowX']) < x
                x = x[indices]
                y = y[indices]

            if 'HighX' in settings:
                indices = x < float(settings['HighX'])
                x = x[indices]
                y = y[indices]

            data['axes'].append({'x': x, 'y': y})

        return data

    def settings(self):
        """Parse settings file if available.

        Assume settings file is an INI file with the same file name as the
        spectrum file minus the file extension.
        """
        settings_file = os.path.splitext(self._name)[0]
        if os.path.exists(settings_file):
            with open(settings_file) as f:
                config = configparser.ConfigParser()
                config.read_file(f, source=settings_file)

            return config['Plot']
        else:
            return {}

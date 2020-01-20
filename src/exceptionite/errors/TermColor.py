import sys

class TermColor:

    end = '\033[0m'

    colors = {
        'header': '\033[95m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'warning': '\033[93m',
        'red': '\033[91m',
        'end': '\033[0m',
        'default': '\033[0;00m',
    }

    bgcolors = {
        'red': '\033[41m',
    }

    options = {
        'bold': '\033[1m',
        'underline': '\033[4m',
    }

    def is_verbose(self, level=1):
        if level is 0:
            return True
        elif level is 1:
            return '-v' in sys.argv
        elif level is 2:
            return '-vv' in sys.argv

    def danger(self, message, verbose=0, padding=0):
        self.start_color = self.colors['red']
        return self.write_line(message, verbose=verbose, padding=padding)

    def info(self, message):
        pass

    def success(self, message):
        pass

    def warning(self, message, verbose=0, padding=0):
        self.start_color = self.colors['warning']
        return self.write_line(message, verbose=verbose, padding=padding)

    def line(self, message, verbose=0, padding=0):
        self.start_color = ''
        message = message.replace(
            '<default>', self.colors['default']).replace('</default>', self.end)
        message = message.replace(
            '<bgred>', self.bgcolors['red']).replace('</bgred>', self.end)
        self.write_line(message, verbose=verbose)

    def color(self, color):
        return 
    
    def write_line(self, message, verbose=0, padding=0):
        if self.is_verbose(level=verbose):
            for pad in range(0, padding):
                print('')

            print(self.start_color + message + self.end)

            for pad in range(0, padding):
                print('')

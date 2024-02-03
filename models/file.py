import io


class File:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self, newline=False):
        file = io.open(self.file_path, encoding='utf-8')
        if newline:
            text = file.readlines()
        else:
            text = file.read()
        file.close()
        return text

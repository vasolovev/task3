from models.file import File


class Template:
    def __init__(self, header='templates/head.tex', begin_test='templates/qStart.tex', metadata='templates/qStart2.tex',
                 end_test='templates/qFinish.tex', footer='templates/tail.tex'):
        self.header = File(header).read_file()
        self.begin_test = File(begin_test).read_file()
        self.metadata = File(metadata).read_file()
        self.end_test = File(end_test).read_file()
        self.footer = File(footer).read_file()


import argparse

FILE_TYPE_FILE = "file"
FILE_TYPE_DIR = "dir"

FAIL = 1
SUCCESS = 0


class FileBase:
    file_type_ = ""
    file_name_ = ""

    def __init__(self, file_name):
        self.file_name_ = file_name

    def __eq__(self, target_file):
        if isinstance(target_file, FileBase):
            return self.file_name_ == target_file.file_name_
        if isinstance(target_file, str):
            return self.file_name_ == target_file
        return False


class File(FileBase):
    file_type_ = FILE_TYPE_FILE


class Folder(FileBase):
    file_type_ = FILE_TYPE_DIR

    def __init__(self, file_name, upper_dir):
        super().__init__(file_name)
        self.content_ = []
        self.upper_dir_ = upper_dir

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.content_[key]
        if isinstance(key, FileBase):
            for file in self.content_:
                if file == key:
                    return file
        if isinstance(key, str):
            for file in self.content_:
                if file.file_name_ == key:
                    return file

    def add_file(self, file: FileBase):
        if file in self.content_:
            print("[ERROR] File \"%s\" already exists" % file.file_name_)
        else:
            self.content_.append(file)


class Filesystem:
    """ File system simulation class """

    def __init__(self):
        self.root_path_ = "/"
        self.root_ = Folder(self.root_path_, None)
        self.current_dir_ = self.root_
        self.current_path_ = self.root_path_

    def cd(self, path):
        """ Change directory """
        if path[0] == "/":
            current_dir = self.root_
        else:
            current_dir = self.current_dir_

        dirs = [target_dir for target_dir in path.split('/') if target_dir != '']
        for target_dir in dirs:
            if target_dir in current_dir.content_:
                if current_dir[target_dir].file_type_ == FILE_TYPE_DIR:
                    current_dir = current_dir[target_dir]
                else:
                    print("[ERROR] \"%s\" is not a directory" % target_dir)
                    return FAIL
            elif target_dir == "..":
                current_dir = current_dir.upper_dir_
                if current_dir == None:
                    print("[ERROR] %s does not exists" % path)
                    return FAIL
            else:
                print("[ERROR] %s does not exists" % path)
                return FAIL

        self.current_dir_ = current_dir
        self.current_path_ = self.get_current_folder()
        return SUCCESS

    def ls(self, target_dir=None):
        """ List files in directory """
        if target_dir != None:
            current_path = self.current_path_
            rc = self.cd(target_dir)
            if rc == FAIL:
                return FAIL

        print(self.current_dir_.file_name_, ":")
        for file in self.current_dir_.content_:
            print("[%s]\t%s" % (file.file_type_, file.file_name_))

        if target_dir != None:
            self.cd(current_path)

    def mkdir(self, dir_name, target_dir=None):
        """ Create folder """
        if target_dir == None:
            target_dir = self.current_dir_

        folder = Folder(dir_name, self.current_dir_)
        target_dir.add_file(folder)

    def touch(self, dir_name, target_dir=None):
        """ Create file """
        if target_dir == None:
            target_dir = self.current_dir_

        file = File(dir_name)
        target_dir.add_file(file)

    def get_current_folder(self):
        """ Get current dir abs path """
        upper = self.current_dir_
        path = ""
        while upper:
            path = f"{ upper.file_name_ }/{ path }"
            upper = upper.upper_dir_

        self.current_path_ = path
        return path

    def eval(self, string):
        """ eval command from string """
        command = string.split(" ")[0]
        if len(string.split(" ")) > 1:
            arg = string.split(" ")[1]
        else:
            arg = False

        # print(f"command: { command }\narg: { arg }")

        if command == "cd":
            if arg:
                self.cd(arg)
            else:
                print("[ERROR] Please define path to change dir")
        if command == "mkdir":
            if arg:
                self.mkdir(arg)
            else:
                print("[ERROR] Please define folder name")
        if command == "ls":
            if arg:
                self.ls(arg)
            else:
                self.ls()
        if command == "touch":
            if arg:
                self.touch(arg)
            else:
                print("[ERROR] Please define file name")
        if command == "exit":
            raise KeyboardInterrupt

def test_fs(fs):
    fs.eval("mkdir")
    fs.eval("mkd")
    fs.eval("m a")
    print("Test mk 1")
    fs.mkdir("test_dir_1")
    fs.mkdir("test_dir_2")
    fs.ls()
    print("Test mk 2")
    fs.cd("test_dir_1")
    fs.ls()
    fs.mkdir("test_dir_internal_1")
    fs.mkdir("test_dir_internal_2")
    fs.mkdir("test_dir_internal_3")
    fs.ls()
    print("Test mk 3")
    fs.cd("/qwe/qwe")
    fs.cd("/")
    fs.ls()
    fs.cd("/test_dir_1/test_dir_internal_3")
    fs.mkdir("aa")
    fs.mkdir("aa")
    fs.mkdir("bb")
    fs.cd("/")
    fs.ls("/test_dir_1/test_dir_internal_3")
    print(fs.get_current_folder())


if __name__ == '__main__':
    fs = Filesystem()
    test_fs(fs)
    try:
        while True:
            command = input()
            fs.eval(command)
    except KeyboardInterrupt:
        pass

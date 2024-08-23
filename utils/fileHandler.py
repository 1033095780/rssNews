import os


class FileHandler:
    @staticmethod
    def mkdir(dir_path):
        os.mkdir(dir_path)

    @staticmethod
    def read_file(file_path) -> str:
        with open(file_path, "r") as fileObj:
            file_context = fileObj.read()

        return file_context

    @staticmethod
    def write_file(file_path, context) -> bool:
        with open(file_path, "a+") as fileObj:
            fileObj.write(context + "\r")
        return True


    @staticmethod
    def check_file_exists(file_path) -> bool:
        return os.path.exists(file_path)

    @staticmethod
    def get_path() -> str:
        return os.getcwd()

    @staticmethod
    def join(a: str, b: str) -> str:
        return os.path.join(a, b)

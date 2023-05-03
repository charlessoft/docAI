# from .utils import ShellParser
import os

from pdf2image.core.textract import LIB_DIR
from pdf2image.core.textract.parsers.utils import ShellParser


class Parser(ShellParser):
    """Extract text from doc files using antiword.
    """

    def extract(self, filename, **kwargs):
        stdout, stderr = self.run(
            [
                "java",
                "-jar",
                os.path.join(LIB_DIR, "tika-app-1.19.jar"),
                "--text",
                filename,
            ]
        )
        return stdout

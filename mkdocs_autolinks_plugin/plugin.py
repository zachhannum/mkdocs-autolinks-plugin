import logging
import os
import pathlib
import re
from urllib.parse import quote
import logging
from collections import defaultdict

from mkdocs.plugins import BasePlugin

LOG = logging.getLogger("mkdocs.plugins." + __name__)

# For Regex, match groups are:
#       0: Whole markdown link e.g. [Alt-text](url)
#       1: Alt text
#       2: Full URL e.g. url + hash anchor
#       3: Filename e.g. filename.md
#       4: File extension e.g. .md, .png, etc.
#       5. hash anchor e.g. #my-sub-heading-link
#       6. Image title (in quotation marks)

AUTOLINK_RE = (
    r"(?:\!\[\]|\[([^\]]+)\])\((([^)/]+\.(md|png|jpg|jpeg|bmp|gif|svg|webp))(#[^)]*)*)(\s(\".*\"))*\)"
)

class AutoLinkReplacer:
    def __init__(self, base_docs_dir, abs_page_path, filename_to_abs_path):
        self.base_docs_dir = base_docs_dir
        self.abs_page_path = abs_page_path
        self.filename_to_abs_path = filename_to_abs_path

    def __call__(self, match):
        # Name of the file
        filename = match.group(3).strip()

        # Absolute path to the directory of the linker
        abs_linker_dir = os.path.dirname(self.abs_page_path)

        # Check if the filename exists in the filename to abs path lookup defaultdict
        if filename not in self.filename_to_abs_path:
            # An if-statement is necessary because self.filename_to_abs_path is a
            # defaultdict, so the more pythonic try: except: wouldn't work.
            LOG.warning(
                "AutoLinksPlugin unable to find %s in directory %s",
                filename,
                self.base_docs_dir,
            )
            return match.group(0)

        abs_link_paths = self.filename_to_abs_path[filename]

        # Check for duplicates
        if len(abs_link_paths) > 1:
            LOG.warning(
                "AutoLinksPlugin: Duplicate filename referred to in '%s': '%s' exists at %s",
                self.abs_page_path,
                filename,
                abs_link_paths,
            )

        abs_link_path = abs_link_paths[0]
        rel_link_path = quote(pathlib.PurePath(os.path.relpath(abs_link_path, abs_linker_dir)).as_posix())

        # Construct the return link by replacing the filename with the relative path to the file
        return match.group(0).replace(match.group(3), rel_link_path)


class AutoLinksPlugin(BasePlugin):
    def __init__(self):
        self.filename_to_abs_path = None

    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        # Initializes the filename lookiup dict if it hasn't already been initialized
        if self.filename_to_abs_path is None:
            self.init_filename_to_abs_path(files)

        # Getting the root location of markdown source files
        base_docs_dir = config["docs_dir"]

        # Getting the page path that we are linking from
        abs_page_path = page.file.abs_src_path

        # Look for matches and replace
        markdown = re.sub(
            AUTOLINK_RE,
            AutoLinkReplacer(base_docs_dir, abs_page_path, self.filename_to_abs_path),
            markdown,
        )

        return markdown

    def init_filename_to_abs_path(self, files):
        self.filename_to_abs_path = defaultdict(list)
        for file_ in files:
            filename = os.path.basename(file_.abs_src_path)
            self.filename_to_abs_path[filename].append(file_.abs_src_path)

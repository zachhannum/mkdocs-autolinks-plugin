import os
from urllib.parse import quote
import re
import logging

from mkdocs.utils import warning_filter
from mkdocs.plugins import BasePlugin


LOG = logging.getLogger("mkdocs.plugins." + __name__)
LOG.addFilter(warning_filter)

# For Regex, match groups are:
#       0: Whole markdown link e.g. [Alt-text](url)
#       1: Alt text
#       2: Full URL e.g. url + hash anchor
#       3: Filename e.g. filename.md
#       4: File extension e.g. .md, .png, etc.
#       5. hash anchor e.g. #my-sub-heading-link

AUTOLINK_RE = r'(?:\!\[\]|\[([^\]]+)\])\((([^)/]+\.(md|png|jpg|jpeg|bmp|gif))(#[^)]*)*)\)'


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

        # Look up the filename in the filename to absolute path lookup dict
        try:
            abs_link_path = self.filename_to_abs_path[filename]
        except KeyError:
            LOG.warning(
                "AutoLinksPlugin unable to find %s in directory %s",
                filename,
                self.base_docs_dir,
            )
            return match.group(0)

        rel_link_path = quote(os.path.relpath(abs_link_path, abs_linker_dir))

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
        self.filename_to_abs_path = {}
        for file_ in files:
            filename = os.path.basename(file_.abs_src_path)

            if filename in self.filename_to_abs_path:
                LOG.warning(
                    "Duplicate filename: '%s' exists at both '%s' and '%s'",
                    filename,
                    file_.abs_src_path,
                    self.filename_to_abs_path[filename],
                )
                continue

            self.filename_to_abs_path[filename] = file_.abs_src_path

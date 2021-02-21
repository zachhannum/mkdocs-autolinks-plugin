import os
from urllib.parse import quote
import re

from mkdocs.plugins import BasePlugin

# For Regex, match groups are:
#       0: Whole markdown link e.g. [Alt-text](url)
#       1: Alt text
#       2: Full URL e.g. url + hash anchor
#       3: Filename e.g. filename.md
#       4: File extension e.g. .md, .png, etc.
#       5. hash anchor e.g. #my-sub-heading-link

AUTOLINK_RE = r'(?:\!\[\]|\[([^\]]+)\])\((([^)/]+\.(md|png|jpg|jpeg|bmp|gif))(#.*)*)\)'

class AutoLinkReplacer:
    def __init__(self, base_docs_dir, abs_page_path):
        self.base_docs_dir = base_docs_dir
        self.abs_page_path = abs_page_path

    def __call__(self, match):
        # Name of the markdown file
        filename = match.group(3).strip()

        # Absolute path to the directory of the linker
        abs_linker_dir = os.path.dirname(self.abs_page_path)

        # Find the path to the target file
        rel_link_path = None
        # Walk through all files in docs directory to find a matching file
        for root, dirs, files in os.walk(self.base_docs_dir):
            for name in files:
                # If we have a match, create the relative path from linker to the link
                if name == filename:
                    # Absolute path to the file we want to link to
                    abs_link_path = os.path.join(root, name)
                    # Constructing relative path from the linker to the link
                    rel_link_path = os.path.relpath(abs_link_path, abs_linker_dir)

        if rel_link_path is None:
            print(
                "WARNING: AutoLinksPlugin unable to find "
                + filename
                + " in directory "
                + self.base_docs_dir
            )
            return match.group(0)

        rel_link_path = quote(rel_link_path)
        # Construct the return link by replacing the filename with the relative path to the file
        if match.group(5) is None:
            link = match.group(0).replace(match.group(2), rel_link_path)
        else:
            link = match.group(0).replace(match.group(2), rel_link_path + match.group(5))

        return link


class AutoLinksPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):

        # Getting the root location of markdown source files
        base_docs_dir = config["docs_dir"]

        # Getting the page path that we are linking from
        abs_page_path = page.file.abs_src_path

        # Look for matches and replace
        markdown = re.sub(
            AUTOLINK_RE, AutoLinkReplacer(base_docs_dir, abs_page_path), markdown
        )

        return markdown

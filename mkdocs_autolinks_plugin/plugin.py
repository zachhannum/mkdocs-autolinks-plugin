import os
from urllib.parse import quote
import re
import logging
from bs4 import BeautifulSoup

from mkdocs.utils import warning_filter
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options, Config


LOG = logging.getLogger("mkdocs.plugins." + __name__)
LOG.addFilter(warning_filter)

# For Regex, match groups are:
#       0: Whole markdown link e.g. [Alt-text](url)
#       1: Alt text
#       2: Full URL e.g. url + hash anchor
#       3: Filename e.g. filename.md
#       4: File extension e.g. .md, .png, etc.
#       5. hash anchor e.g. #my-sub-heading-link

AUTOLINK_RE = (
    r"(?:\!\[\]|\[([^\]]+)\])\((([^)/]+\.(md|png|jpg|jpeg|bmp|gif))(#[^)]*)*)\)"
)


# {'source filename': ['url + hash anchor1', 'url + hash anchor2', ... ], ...}
_target_anchors_per_file = {}


class AutoLinkReplacer:
    def __init__(
        self,
        base_docs_dir,
        abs_page_path,
        filename_to_abs_path,
        html_error_if_invalid,
        warn_not_found_anchors,
    ):
        self.base_docs_dir = base_docs_dir
        self.abs_page_path = abs_page_path
        self.filename_to_abs_path = filename_to_abs_path
        self.html_error_if_invalid = html_error_if_invalid
        self.warn_not_found_anchors = warn_not_found_anchors

        if self.warn_not_found_anchors:
            try:
                self.anchors_list = _target_anchors_per_file[self.abs_page_path]
            except KeyError:
                _target_anchors_per_file[self.abs_page_path] = []
                self.anchors_list = _target_anchors_per_file[self.abs_page_path]

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

            if self.html_error_if_invalid:
                return f'<a href=".">ERROR : unable to find "{match.group(3)}"</a>'

            return match.group(0)

        rel_link_path = quote(os.path.relpath(abs_link_path, abs_linker_dir))

        # Track hash anchors for warning after the build
        if self.warn_not_found_anchors:
            if match.group(5) is not None:
                self.anchors_list.append(match.group(2))

        # Construct the return link by replacing the filename with the relative path to the file
        return match.group(0).replace(match.group(3), rel_link_path)


class AutoLinksPlugin(BasePlugin):

    config_scheme = (
        ("html_error_if_invalid", config_options.Type(bool, default=False)),
        ("warn_not_found_anchors", config_options.Type(bool, default=False)),
    )

    def __init__(self):
        self.filename_to_abs_path = None

        # [ 'page.file.abs_src_path + hash anchor, ...]
        self.existing_anchors = []

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
            AutoLinkReplacer(
                base_docs_dir,
                abs_page_path,
                self.filename_to_abs_path,
                self.config["html_error_if_invalid"],
                self.config["warn_not_found_anchors"],
            ),
            markdown,
        )

        return markdown

    def on_page_content(self, html, page, config, files):

        if self.config["warn_not_found_anchors"]:
            soup = BeautifulSoup(html, "html.parser")
            titles = soup.find_all(("h1", "h2", "h3", "h4", "h5", "figure"))

            for title in titles:
                self.existing_anchors.append(
                    page.file.name + ".md#" + title.attrs["id"]
                )

        return html

    def on_post_build(self, config):

        if self.config["warn_not_found_anchors"]:
            for src_filename, hash_targets in _target_anchors_per_file.items():

                for hash_target in hash_targets:
                    if hash_target not in self.existing_anchors:
                        LOG.warning(
                            f"{src_filename} has link to {hash_target} which is not valid"
                        )

    def init_filename_to_abs_path(self, files):
        self.filename_to_abs_path = {}
        for file_ in files:
            filename = os.path.basename(file_.abs_src_path)
            file_ext = filename.split(os.extsep)[-1]

            if filename in self.filename_to_abs_path:
                if file_ext in ["md", "png", "jpg", "jpeg", "bmp", "gif"]:
                    LOG.warning(
                        "AutoLinksPlugin : Duplicate filename: '%s' exists at both '%s' and '%s'",
                        filename,
                        file_.abs_src_path,
                        self.filename_to_abs_path[filename],
                    )
                else:
                    LOG.debug(
                        "AutoLinksPlugin : Duplicate filename: '%s' exists at both '%s' and '%s'",
                        filename,
                        file_.abs_src_path,
                        self.filename_to_abs_path[filename],
                    )
                continue

            self.filename_to_abs_path[filename] = file_.abs_src_path

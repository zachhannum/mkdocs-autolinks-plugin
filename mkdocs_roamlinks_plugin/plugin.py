import re
import os
import logging
import urllib.parse

from mkdocs.plugins import BasePlugin
import mkdocs.utils

log = logging.getLogger(f"mkdocs.plugins.{__name__}")
log.addFilter(mkdocs.utils.warning_filter)

# For Regex, match groups are:
#       0: Whole markdown link e.g. [Alt-text](url)
#       1: Alt text
#       2: Full URL e.g. url + hash anchor
#       3: Filename e.g. filename.md
#       4: File extension e.g. .md, .png, etc.
#       5. hash anchor e.g. #my-sub-heading-link
AUTOLINK_RE = r'\[([^\]]+)\]\((([^)/]+\.(md|png|jpg))(#.*)*)\)'

# For Regex, match groups are:
#       0: Whole roamlike link e.g. [[filename#title|alias]]
#       1: Whole roamlike link e.g. filename#title|alias
#       2: filename
#       3: #title
#       4: |alias
ROAMLINK_RE = r'\[\[(([^\]#\|]*)(#[^\|\]]+)*(\|[^\]]*)*)\]\]'


class AutoLinkReplacer:
    def __init__(self, base_docs_url, page_url):
        self.base_docs_url = base_docs_url
        self.page_url = page_url

    def __call__(self, match):
        # Name of the markdown file
        filename = urllib.parse.unquote(match.group(3).strip())

        # Absolute URL of the linker
        abs_linker_url = os.path.dirname(
            os.path.join(self.base_docs_url, self.page_url))

        # Find directory URL to target link
        rel_link_url = ''
        # Walk through all files in docs directory to find a matching file
        for root, dirs, files in os.walk(self.base_docs_url):
            for name in files:
                # If we have a match, create the relative path from linker to the link
                if name == filename:
                    # Absolute path to the file we want to link to
                    abs_link_url = os.path.dirname(os.path.join(root, name))
                    # Constructing relative path from the linker to the link
                    rel_link_url = os.path.join(
                        os.path.relpath(abs_link_url, abs_linker_url),
                        filename)
        if rel_link_url == '':
            log.warning(f"AutoLinksPlugin unable to find {filename} in directory {self.base_docs_url}")
            return match.group(0)

        # Construct the return link by replacing the filename with the relative path to the file
        if (match.group(5) == None):
            link = match.group(0).replace(match.group(2), rel_link_url)
        else:
            link = match.group(0).replace(match.group(2),
                                          rel_link_url + match.group(5))
        return link


class RoamLinkReplacer:
    def __init__(self, base_docs_url, page_url):
        self.base_docs_url = base_docs_url
        self.page_url = page_url

    def simplify(self, filename):
        """ ignore - _ and space different, replace .md to '' so it will match .md file,
        if you want to link to png, make sure you filename contain suffix .png, same for other files
        but if you want to link to markdown, you don't need suffix .md """
        return re.sub(r"[\-_ ]", "", filename.lower()).replace(".md", "")

    def gfm_anchor(self, title):
        """Convert to gfw title / anchor 
        see: https://gist.github.com/asabaylus/3071099#gistcomment-1593627"""
        if title:
            title = title.strip().lower()
            title = re.sub(r'[^\w\u4e00-\u9fff\- ]', "", title)
            title = re.sub(r' +', "-", title)
            return title
        else:
            return ""

    def __call__(self, match):
        # Name of the markdown file
        whole_link = match.group(0)
        filename = match.group(2).strip() if match.group(2) else ""
        title = match.group(3).strip() if match.group(3) else ""
        format_title = self.gfm_anchor(title)
        alias = match.group(4).strip('|') if match.group(4) else ""

        # Absolute URL of the linker
        abs_linker_url = os.path.dirname(
            os.path.join(self.base_docs_url, self.page_url))

        # Find directory URL to target link
        rel_link_url = ''
        # Walk through all files in docs directory to find a matching file
        if filename:
            for root, dirs, files in os.walk(self.base_docs_url):
                for name in files:
                    # If we have a match, create the relative path from linker to the link
                    if self.simplify(name) == self.simplify(filename):
                        # Absolute path to the file we want to link to
                        abs_link_url = os.path.dirname(os.path.join(
                            root, name))
                        # Constructing relative path from the linker to the link
                        rel_link_url = os.path.join(
                                os.path.relpath(abs_link_url, abs_linker_url), name)
                        if title:
                            rel_link_url = rel_link_url + '#' + format_title
            if rel_link_url == '':
                log.warning(f"RoamLinksPlugin unable to find {filename} in directory {self.base_docs_url}")
                return whole_link
        else:
            rel_link_url = '#' + format_title

        # Construct the return link
        # Windows escapes "\" unintentionally, and it creates incorrect links, so need to replace with "/"
        rel_link_url = rel_link_url.replace("\\", "/")

        if filename:
            if alias:
                link = f'[{alias}]({rel_link_url})'
            else:
                link = f'[{filename+title}]({rel_link_url})'
        else:
            if alias:
                link = f'[{alias}]({rel_link_url})'
            else:
                link = f'[{title}]({rel_link_url})'

        return link


class RoamLinksPlugin(BasePlugin):
    def on_page_markdown(self,
                         markdown,
                         page,
                         config,
                         site_navigation=None,
                         **kwargs):

        # Getting the root location of markdown source files
        base_docs_url = config["docs_dir"]

        # Getting the page url that we are linking from
        page_url = page.file.src_path

        # Look for matches and replace
        markdown = re.sub(AUTOLINK_RE,
                          AutoLinkReplacer(base_docs_url, page_url), markdown)
        markdown = re.sub(ROAMLINK_RE,
                          RoamLinkReplacer(base_docs_url, page_url), markdown)

        return markdown

import re
import os
from mkdocs.plugins import BasePlugin

# For Regex, match groups are:
#       0: Whole markdown link e.g. [Alt-text](url)
#       1: Alt text
#       2: Full URL e.g. url + hash anchor
#       3: Filename e.g. filename.md
#       4: File extension e.g. .md, .png, etc.
#       5. hash anchor e.g. #my-sub-heading-link

AUTOLINK_RE = r'\[([^\]]+)\]\((([^)/]+\.(md|png|jpg))(#.*)*)\)'
# (?<!```\n)\[([^\]]+)\]\(([^)/]+\.md)\)
class AutoLinkReplacer:
    def __init__(self, base_docs_url, page_url):
        self.base_docs_url = base_docs_url
        self.page_url = page_url

    def __call__(self, match):
        # Name of the markdown file
        filename = match.group(3).strip()

        # Absolute URL of the linker
        abs_linker_url = os.path.dirname(os.path.join(self.base_docs_url, self.page_url))

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
                    rel_link_url = os.path.join(os.path.relpath(abs_link_url, abs_linker_url), filename)
        if rel_link_url == '':
            print('WARNING: AutoLinksPlugin unable to find ' + filename + ' in directory ' + self.base_docs_url)
            return match.group(0)

        # Construct the return link by replacing the filename with the relative path to the file
        if(match.group(5) == None):
            link = match.group(0).replace(match.group(2), rel_link_url)
        else:
            link = match.group(0).replace(match.group(2), rel_link_url + match.group(5))

        return link

class AutoLinksPlugin(BasePlugin):

    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):

        # Getting the root location of markdown source files
        base_docs_url = config["docs_dir"]

        # Getting the page url that we are linking from
        page_url = page.file.src_path

        # Look for matches and replace
        markdown = re.sub(AUTOLINK_RE, AutoLinkReplacer(base_docs_url, page_url), markdown)

        return markdown

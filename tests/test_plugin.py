import os
import tempfile
import pytest

from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs_roamlinks_plugin.plugin import RoamLinksPlugin


@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def config(temp_directory):
    return {"docs_dir": temp_directory}


@pytest.fixture
def site_navigation():
    return []


@pytest.fixture
def page(temp_directory):
    os.mkdir(os.path.join(temp_directory, "test"))
    file_path = os.path.join(temp_directory, "test", "test.md")
    with open(file_path, "w", encoding="utf8") as f:
        f.write("# Heading identifiers in HTML")
    with open(os.path.join(temp_directory, "demo (t).md"), "w", encoding="utf8") as f:
        f.write("# Demo Page")
    with open(os.path.join(temp_directory, "image.png"), "w", encoding="utf8") as f:
        f.write("# Image Page")
    with open(os.path.join(temp_directory, "image (1).png"), "w", encoding="utf8") as f:
        f.write("# Image Page")
    with open(os.path.join(temp_directory, "41m+ZoNoWqL._AC_UF894,1000_QL80_.jpg"), "w", encoding="utf8") as f:
        f.write("# Image Page")
    os.mkdir(os.path.join(temp_directory, "software"))
    with open(
        os.path.join(temp_directory, "software", "git_flow.md"), "w", encoding="utf8"
    ) as f:
        f.write("# Git Flow")

    return Page(
        title="Test Page",
        file=File(file_path, temp_directory, temp_directory, False),
        config={},
    )

@pytest.fixture
def converter(temp_directory, config, site_navigation, page):
    def c(markdown):
        plugin = RoamLinksPlugin()
        return plugin.on_page_markdown(markdown, page, config, site_navigation)

    return c

###############################################################################{}
## Text Links
###############################################################################{}

def test_converts_basic_link(converter):
    assert converter("[[Git Flow]]") == "[Git Flow](<../software/git_flow.md>)"

def test_converts_link_with_slash(converter):
    assert converter("[[software/Git Flow]]") == "[software/Git Flow](<../software/Git Flow.md>)"

def test_converts_link_with_anchor_only(converter):
    assert converter("[[#Heading identifiers]]") == "[#Heading identifiers](<#heading-identifiers>)"

def test_converts_link_with_anchor(converter):
    assert converter("[[Git Flow#Heading]]") == "[Git Flow#Heading](<../software/git_flow.md#heading>)"

def test_converts_link_with_parenthesis(converter):
    assert converter("[[demo (t)]]") == "[demo (t)](<../demo (t).md>)"

def test_converts_link_with_parenthesis_and_space(converter):
    assert converter("[demo (t)](<../demo%20(t).md>)") == "[demo (t)](<../demo%20(t).md>)"

def test_converts_link_with_spaces_in_text(converter):
    assert converter('[[Git Flow|Title With Spaces]]') == '[Title With Spaces](<../software/git_flow.md>)'

def test_converts_link_with_punctuation_in_text(converter):
    assert converter('[[Git Flow|Title, with. Punctuation!]]') == '[Title, with. Punctuation!](<../software/git_flow.md>)'

def test_converts_link_with_square_brackets_in_text(converter):
    assert converter('[[Git Flow|Title [with] square [brackets]]]') == '[Title [with] square [brackets]](<../software/git_flow.md>)'

def test_converts_link_with_single_quotes_in_text(converter):
    assert converter("[[Git Flow|Title 'with' single 'quotes']]") == "[Title 'with' single 'quotes'](<../software/git_flow.md>)"

def test_converts_link_with_double_quotes_in_text(converter):
    assert converter('[[Git Flow|Title "with" double "quotes"]]') == '[Title "with" double "quotes"](<../software/git_flow.md>)'

def test_converts_link_with_fragment_identifier(converter):
    assert converter('[[Git Flow#section|Title]]') == '[Title](<../software/git_flow.md#section>)'

###############################################################################{}
## Images
###############################################################################{}
def test_converts_basic_image_link(converter):
    assert converter("![[image.png]]") == '![image.png](<../image.png>)'

def test_converts_crazy_image_link(converter):
    assert converter("![[41m+ZoNoWqL._AC_UF894,1000_QL80_.jpg|Edimax EW-7811un 802.11n WiFi Adapter]]") == '![Edimax EW-7811un 802.11n WiFi Adapter](<../41m+ZoNoWqL._AC_UF894,1000_QL80_.jpg>)'

def test_converts_image_link_with_width(converter):
    assert converter("![[image.png|600]]") == '![image.png](<../image.png>){ width="600" }'

def test_converts_image_link_with_width_and_height(converter):
    assert converter("![[image.png|600x800]]") == '![image.png](<../image.png>){ width="600"; height="800" }'

def test_converts_image_link_with_title_and_width(converter):
    assert converter("![[image.png|Image|600]]") == '![Image](<../image.png>){ width="600" }'

def test_converts_image_link_with_parenthesis_title_and_width(converter):
    assert converter("![[image (1).png|Image|600]]") == '![Image](<../image (1).png>){ width="600" }'

def test_converts_image_link_with_parenthesis_title_width_and_height(converter):
    assert converter("![[image (1).png|Image|600x200]]") == '![Image](<../image (1).png>){ width="600"; height="200" }'

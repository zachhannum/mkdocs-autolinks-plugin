# MkDocs Roamlinks Plugin

An MkDocs plugin that simplifies relative linking between documents and convert roamlinks .

## Setup 

Install the plugin using pip:

`pip install mkdocs-roamlinks-plugin`

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  - roamlinks 
```

## Usage

To use this plugin, simply create a link that only contains the filename of file you wish to link to.

| origin                  | convert                             |
| ----------------------- | ----------------------------------- |
| `[Git Flow](git_flow.md)` | `[Git Flow](../software/git_flow.md)` |
| [[Git Flow]]            | `[Git Flow](../software/git_flow.md)` |
| ![[image.png]]           | `![image.png](../image/imag.png)`      |
[[#Heading identifiers]] | `[Heading identifiers in HTML](#heading-identifiers-in-html)`

## Known issues
roamlinks don't support ` [[Git Flow#Heading]]`

| origin                  | convert                             |
| ----------------------- | ----------------------------------- |
 [[Git Flow#Heading\| Alias]] | `[Alias](../software/git_flow.md#heading)` |

1. mkdocs heading have problem with Chinese, show `#_1`
2. somehow I format to `[Alias](../software/git_flow.md/#heading)` bug mkdocs won't change it to `https://xx/git_flow/#heading` , strip(".md")
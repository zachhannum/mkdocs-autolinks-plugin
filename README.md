# MkDocs Roamlinks Plugin

An MkDocs plugin that simplifies relative linking between documents and convert [[roamlinks]] for [vscode-foam](https://github.com/foambubble/foam) & [obsidian](https://obsidian.md) 

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
| `[[Git Flow]]`            | `[Git Flow](../software/git_flow.md)` |
| `[[software/Git Flow]]`   | `[software/Git Flow](../software/git_flow.md)` |
| `![[image.png]]`           | `![image.png](../image/imag.png)`      |
| `[[#Heading identifiers]]` | `[Heading identifiers in HTML](#heading-identifiers-in-html)`|
| `[[Git Flow#Heading]]`     |  `[Git Flow](../software/git_flow.md#heading)` |
| `![[image.png|Description|800x600]]` | `![Description](image.png){ width="600"; height="800" }` |


## TODO

- [ ] convert admonition, for example

[obsidian style admonition](https://help.obsidian.md/How+to/Use+callouts)
```
> [!info]
> something
```

to [mkdoc material style](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)
```
!!! note

    something
```
- [ ] `%% comment %%` to `<!-- comment -->`

# MkDocs Autolinks Plugin

An MkDocs plugin that simplifies relative linking between documents.

The Autolinks plugins allows you to link to pages and images within your MkDocs site without provided the entire relative path to the file in your document structure.

## Setup 

Install the plugin using pip:

`pip install mkdocs-autolinks-plugin`

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  - autolinks 
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].


## Usage

To use this plugin, simply create a link that only contains the filename of file you wish to link to.

For example, say you have a document structure like this:

```
docs/
├── guides/
│   ├── onboarding.md
│   └── syntax_guide.md
├── software/
│   ├── git_flow.md
│   └── code_reviews.md
└── images/
    ├── avatar.png
    └── example.jpg
```

Normally, if you want create a link to `git_flow.md` from inside `onboarding.md`, you would need to provide the relative path:

```markdown
# onboarding.md
[Git Flow](../software/git_flow.md)
```

This link is fragile; if someone decides to rearrange the site structure, all of these relative links break. Not to mention having to figure out the relative path.

With the Autolinks plugin, you simply need to provide the filename you wish to link to. The plugin will pre-process all of your markdown files and replace the filename with the correct relative path, given that the file exists in your document structure:

```markdown
# onboarding.md
[Git Flow](git_flow.md)
```

The Autolinks plugin also works with `jpg` and `png` files:

```markdown
# onboarding.md
![Avatar](avatar.png)
```

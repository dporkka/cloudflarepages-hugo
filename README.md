# Readme Template

This repository contains a Hugo-based documentation site template that's ready to deploy to Cloudflare Pages.

visit this example here https://timsnotes.pages.dev/

## Quick Start

1. Fork this repository, then clone your fork recursively:
   ```sh
   git clone --recurse-submodules https://github.com/YOUR-USER/cloudflarepages-hugo.git
   cd cloudflarepages-hugo
   ```
   For an existing checkout, run `git submodule update --init --recursive`.
2. Install **Hugo 0.170.0**. The Book theme is pinned to released version
   **v0.15.0** by the tracked Git submodule at
   `027be3349d20785efeb93f6773872a35497d7258`. This release uses plain CSS
   and requires neither Hugo Extended nor Dart Sass.
   Do not use `git submodule update --remote` in reproducible builds.
3. Preview locally with `hugo server`, or build with `hugo --minify`.
4. On Cloudflare Pages, connect your fork and set:
   - Build command: `git submodule update --init --recursive && hugo --minify`
   - Output directory: `public`
   - Environment variable: `HUGO_VERSION=0.170.0`
   - Environment variable: `HUGO_ENV=production`

Set `baseURL` in `hugo.toml` to your canonical HTTPS URL (with a trailing
slash) for production. The relative default is useful for local previews.

## Portable / offline build

Once the pinned submodule and Hugo binary are available locally,
build without fetching dependencies:

```sh
hugo --minify
python3 -m http.server 8080 --directory public
```

The generated folder can be copied to any static HTTP host. For a complete
source archive, include the checked-out `themes/book` files (a plain
`git archive` omits submodule contents). Keep the exact Hugo binary and
verify archived checksums. No Node.js installation is required.

## Validate the template

After initializing the pinned submodule, run the optional standard-library
regression check with Python 3:

```sh
HUGO_BIN=hugo python3 -m unittest discover -s tests -v
```

The test builds the same source at the domain root and a nested deployment
prefix, treats Hugo warnings as failures, and checks generated local links
and assets. Python is not needed for deployment.

## Site Structure

```
content/
├── _index.md          # Main landing page
└── docs/
    ├── topic1/
    │   ├── _index.md # Topic overview
    │   ├── subtopic1/
    │   │   └── _index.md
    │   └── subtopic2/
    │       └── _index.md
    └── [other topics]
```

## Creating Content

### File Format
Every markdown file should start with frontmatter:

```md
---
title: "Your Page Title"
description: "Brief description"
date: 2024-12-11
draft: false
---
```
* if draft: true is set, it will not publish publicly


### Markdown Examples

#### Basic Formatting
```md
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
~~Strikethrough~~

> This is a blockquote
```

#### Lists
```md
- Bullet point
- Another point
  - Nested point
  - Another nested point

1. Numbered list
2. Second item
   1. Nested numbered item
   2. Another nested item
```

#### Code
````md
```python
def hello_world():
    print("Hello, World!")
```
````

#### Links
```md
# Internal Links
- [Link to Topic 1](/docs/topic1/)
- [Link to Subtopic](../subtopic1)
- [Relative link to sibling page](./another-page)

# External Links
[OpenAI](https://openai.com)
```

#### Images
```md
![Alt text](/images/example.png)
```

#### Tables
```md
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```

### Link Structure Examples

1. From a topic page to its subtopics:
```md
- [Subtopic 1](subtopic1)
- [Subtopic 2](subtopic2)
```

2. From a subtopic back to its parent:
```md
[Back to Topic 1](..)
```

3. From any page to the home page:
```md
[Home](/)
```

4. Between sibling subtopics:
```md
[Next Subtopic](../subtopic2)
```

## Customization

### Site Configuration
Edit `hugo.toml` to change:
- Site title
- Base URL (currently using relative path)
- Language settings
- Theme options

### Adding New Topics
1. Create a new directory in `content/docs/`
2. Add an `_index.md` file
3. Add your content files
4. Push to GitHub - Cloudflare will automatically deploy changes

## Custom Hostname
Set `baseURL` to your canonical hostname before a production build.

## Troubleshooting

### Common Issues
1. Build fails: Check HUGO_VERSION in Cloudflare Pages settings
2. Missing content: Ensure frontmatter is properly formatted
3. Broken links: Check relative path structure

Need help? Open an issue on GitHub!

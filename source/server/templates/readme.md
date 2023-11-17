# Templates

## Components 

- Made of isolated html segements and jinja macros for single purpose. They can operate in isolation.

## Sections

- Building blocks for html pages made of html segment.

## Pages

- Jinja/HTML pages that extend `base.html`. Each page is independent of other pages and has its own context. 

## Icons

- `svg` HTML segments. Better to append svgs than having multiple request waterfalls to my server.
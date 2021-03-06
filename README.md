# Magic-Cardmarket-Spider

A scrapy-powered spider which parses all the 'single card' magic advertisement on https://www.cardmarket.com/.

## Prerequisites

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

The only package you need is scrapy. To install it, run the following command:

```bash
pip install scrapy
```

If your system (I assume it is UNIX) does not recognize the command "scrapy" add it to your path:

```bash
PATH="${PATH}:${HOME}/.local/bin"
```

## Run the project

Before executing anything, keep in mind that this execution may take days:

```bash
cd mkm

scrapy crawl mkm -o outputfile.csv
```

## Built With

* [Scrapy](https://scrapy.org/) - The industry standard for building spiders.

## Authors

* **Diego Dominguez**   <a href="https://twitter.com/DGlez1111" target="_blank">
    <img alt="Twitter: DGlez1111" src="https://img.shields.io/twitter/follow/DGlez1111.svg?style=social" />
  </a>

## MIT License

Copyright (c) 2020 Diego Domínguez González

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

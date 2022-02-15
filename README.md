# Magic-Cardmarket-Spider

A scrapy-powered spider that parses all the 'single card' magic card advertisements on CardMarket.

## Prerequisites

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

You will need to install some libs in order to run any spider. To install them, run the following command:

```bash
pip install -r requirements.txt
```

You also will need to install docker && docker-compose.

## Run the project

Before executing anything, keep in mind that this execution may take days:

```bash
docker-compose up -d

cd magic

scrapy crawl mkm
```

If your system (I assume it is UNIX) does not recognize the command "scrapy" add it to your path:

```bash
PATH="${PATH}:${HOME}/.local/bin"
```

## Built With

* [Scrapy](https://scrapy.org/)
* [Docker](https://www.docker.com/)
* [Privoxy](https://www.privoxy.org/)
* [Tor](https://www.torproject.org/)

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

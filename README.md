# WiproDigital Spider

## Task

Please write a simple web crawler in a language of your choice in a couple of
hours – please don’t spend much more than that.

The crawler should be limited to one domain. Given a starting URL – say
http://wiprodigital.com - it should visit all pages within the domain, but not
follow the links to external sites such as Google or Twitter.

The output should be a simple structured site map (this does not need to be a
traditional XML sitemap - just some sort of output to reflect what your crawler
has discovered), showing links to other pages under the same domain, links to
external URLs and links to static content such as images for each respective
page.

Please provide a README.md file that explains how to run / build your solution.
Also, detail anything further that you would like to achieve with more time.

Once done, please make your solution available on Github and forward the link.
Where possible please include your commit history to give visibility of your
thinking and progress.

## Running

This solution requires Python3 (https://www.python.org/) and Scrapy
(https://scrapy.org/). The easiest way is to run it is via a virtual
environment:

0. `git clone https://github.com/borancar/wipro_digital_spider.git`
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install scrapy`
4. `scrapy runspider spider.py -o out.json`

### Playing with data

Using jq (https://stedolan.github.io/jq/):
- Pretty-print data
  ```
  jq "." out.json 
  ```
- Find all urls crawled:
  ```
  jq ".[].url" out.json | sort | uniq
  ```
- Find all external links:
  ```
  jq ".[].external_links[]" out.json | sort | uniq
  ```

## Reasoning

When looking at the task of designing a crawler, one can initially start with
writing a recursive (whether DFS or BFS) search and HTML parser + some
selector. What typically happens afterwards is that same person realizes new
requirements are creeping in just to preserve functionality:
- the crawler is running too slow and needs to be parallelized
- the webserver has a limit on how many concurrent connections it will accept
  from the same IP before throttling
- (optional) the ability to have a cluster with different IPs to negate
  webserver throttling
The next step is spaghetti code where the engine of the crawler, the parsing,
the output generation are all mixed together so a refactor stage needs to
separate them.

For these reasons, I chose to leverage scrapy which abstracts away the core
engine of the crawler (the recursive traversal, throttling, ...) and provides
an architecturally clean pipelined solution that allows custom pipeline stages.
The trade-off here is simply having to learn a new framework.

## Next steps

- The crawler only looks at `<a>` and `<img>` elements, check whether
  anything else is of interest
- XML sitemap
- Understanding what navigation `#fragment` imply and re-adding them
- GUI that allows seeing a graph
- Measure connectivity, find strongly connected components to guide the
  UX designers of the website (e.g. refactoring them into a single page).

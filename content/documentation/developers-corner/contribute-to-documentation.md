+++
title = "Contribute to documentation"
weight = 10
+++

## Contribute to documentation 

Here we explain how to make change in the documentation and make it available online.

### General information

Our web [site repository](https://github.com/scgmlz/BornAgain-website) contains two branches.
`Master` branch contains markdown content of the site, `gh-pages` branch contains static html of the site.
[Hugo](https://gohugo.io/) static site generator is used to produce html content from markdown pages.

GitHub is configured to host content of `gh-pages` branch at [this address](https://scgmlz.github.io/BornAgain-website).

Users are modifying site content by providing pull requests to `master` branch. `Travis` continuous integration automatically generates
fresh html of the site and updates `gh-pages` branch.

To modify documentation follow these steps:

### Install Hugo

* Downloads latest hugo from [here](https://github.com/gohugoio/hugo/releases).
* Archive will contain single binary which you will have to put to your `$HOME/bin` directory, for example.

### Fork documentation repository

Make a fork of our [site repository](https://github.com/scgmlz/BornAgain-website) and clone your fork locally.

Please note, that repository contains submodule (external Hugo theme), so clone command should be

```
git clone --recurse-submodules https://github.com/<your-name>/BornAgain-website.git
```


### Run Hugo locally

Go to cloned repository and run `Hugo`.

```
$ cd <source>
$ hugo server -D
```

Open web-browser using address Hugo will tell you (most probably http://localhost:1313/BornAgain-website). 

### Modify the documentation

Modify one of documentation related markdown file. For example, to modify the page you are looking at right now, edit
```
<source>/content/documentation/developers-corner/contribute-to-documentation.md
```
`Hugo` will update web site within a fraction of a second. 


### Provide a pull request

When you are happy with the changes you've made, push changes to the `origin` and provide a pull request.

`Travis` will start the build to make sure that site is still in working state (no broken links found, etc). 
Depending on `Travis` mood and load, the build can be completed in less than a minute.

> Members of [scgmlz](https://github.com/scgmlz) have rights to merge their own pull requests.
> External users will have to wait a bit for a person with admin rights to approve.

After pull request merge, check site [online](https://scgmlz.github.io/BornAgain-website/).
It might take a few minutes before changes will be propagated to hosting service.

{{% alert theme="info" %}}
Because of browser cashing you might need to reload the page from scratch (e.g. push `reload` button while holding `shift` key).
See also [bypass your cache](https://en.wikipedia.org/wiki/Wikipedia:Bypass_your_cache).
{{% /alert %}}
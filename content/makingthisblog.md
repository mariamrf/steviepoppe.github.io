Title: Hello World - About This Blog
Category: technical
Tags: pelican, blog, github
Author: Stevie Poppe
Date: 2016-08-23
Status: published
Image: helloworld.jpg

[TOC]

<!-- PELICAN_START_SUMMARY -->

I had been thinking on starting a small, personal blog for a while now and was already in the progress of writing up a small stack of possible articles to post. A long summer-break permitted me to sit down and get started on the technicalities; a process a bit more complicated as initially expected but worth it in the long run. This blog serves not as a tutorial on making one with Pelican (I'll get to that *eventually*), but as a brief log on my reasoning and thought process during creation.

<!-- PELICAN_END_SUMMARY -->

# Blog-platform

## Deciding

Conceptually I tried to steer away from heavy content management systems such as **Drupal** and **WordPress**. While easy to work with (and taking quite a bit of technical work of your hands), a server-side database means too heavy a load for what's basically a small-scale personal blog, and several unnecessary security risks on top.[^1] The tinkerer in me opted for a DIY approach with full control over both content and design. As far as Static blog frameworks go there were several popular options, but since I'm more accustomed to the *Python* programming language I ended up choosing for **[Pelican](http://blog.getpelican.com/)** over more widespread options such as the *Ruby*-based **[Jekyll](http://jekyllrb.com/)**. An added value of managing my blogs client-side and delivering small sized static pages is the ease of finding an appropriate host (I host my pages on **[GitHub Pages](https://pages.github.com/)** while serving larger files through DropBox) as well as seamless integration with my *Markdown*-based writing work-flow.[^2]

## Set-up

The initial set-up is relatively simple, as installation and basic generation are done through command line, and content written in *Markdown*, *AsciiDoc* or *reStructuredText*[^3] gets served as stand-alone pages or articles. There's a wide choice of [existing templates](http://www.pelicanthemes.com/), but further customization requires some working knowledge on web-design as well as, preferably, on basic programming concepts (Pelican templates are created using the python-based **[Jinja2](http://jinja.pocoo.org/)**, allowing for template logic and inheritance). Needless to say, hosting on GitHub Pages requires rudementary knowledge of **Git**, but that's really not a skill learned in vain as the concept of version control applies well to writing papers and other documents too.

## Development

Getting acquainted with these tools can be time consuming. Luckily Pelican's [well documented](http://docs.getpelican.com/en/3.6.3/#), and there are plenty of tutorials out there, as well as hundreds of working examples hosted on GitHub available as reference (the backbone of my template is a heavily modified *[Plumage](https://github.com/kdeldycke/plumage)* theme). I prefer a minimalistic layout easy on the eye, and steered clear of unnecessary clutter, but with the advent of visual blogging[^4] I figured I'd integrate *some* graphical elements, such as article banners (that's the extent of it really, I'm not much of an artist), as visual content engages the reader more easily. One easily overlooked design problem is ensuring responsive web-pages for the ever increasing mobile internet traffic[^5], but with easy support for *[Sass](http://sass-lang.com/)*, or just using Twitter's **Bootstrap** framework, this comes pretty naturally. Finally, implementing additional features is pretty easy too. There's a wide range of existing [plugins](https://github.com/getpelican/pelican-plugins) for features like searching, minifying assets, table of contents and comments (using the third-party **[Disqus](https://disqus.com/)** blog hosting service).

## Hosting

GitHub has allowed free hosting for static personal or project-sites on GitHub Pages for a while now. This boils down to creating a new repository with your user-name and GitHub url (*steviepoppe.github.io*) and hosting your pages there. I created an additional source branch to host all my source-files, use [ghp-import](https://github.com/davisp/ghp-import) to place my output files in a separate branch, and force push that to the master branch on GH Pages.[^6]

    #!python
	pelican content -o output -s publishconf.py && ghp-import output && git push -f origin gh-pages:master

As of writing, GitHub's SSL certificate only covers *.github.io domains; there isn't any support yet for custom domains. Thus as final step after having set up my custom domain, and as an additional security layer, I use [CloudFare](https://www.cloudflare.com/) to secure part of the connection and enroll some further optimizations.

# Conclusion

While further customization requires *some* technical experience (or at least the proper mindset), I believe the base set-up is easy enough for anyone to learn and allows for more control over your own content and a smoother work-flow as you would have relying on big CMS systems. Any extra skills learned will definitely come in use as digital publishing, web-design and working with Git or other forms of version control become more and more basic skills anyone should possess. In retrospect, Jekyll appears to be an easier option for beginners with it's widespread usage, but both Jekyll and Pelican achieve the same thing, so this is personal choice really. I'll end up writing a full step-by-step beginner's guide on setting up Pelican and hosting on GitHub Pages eventually, but for now I'll post several decent tutorials below.

#Further reading

* <http://arunrocks.com/moving-blogs-to-pelican/>
* <http://cyrille.rossant.net/pelican-github/>
* <http://duncanlock.net/blog/2013/05/17/how-i-built-this-website-using-pelican-part-1-setup/>
* <http://guizishanren.com/guide-to-set-up-github-page-and-pelican/>

[^footnote]: Icelandic Sunset by Stevie Poppe (<https://flic.kr/p/M83mKT> - CC BY-SA 2.0)
[^1]: Burnett, Brett. 2015. “Why Did We Migrate from Drupal to Jekyll?” Text. The BHW Group. <https://thebhwgroup.com/blog/jekyll-drupal-wordpress>
[^2]: O’Nolan, John. 2015. “The Ultimate Guide to Writing & Publishing with Markdown”. Ghost. <https://blog.ghost.org/markdown/>
[^3]: All three are open, lightweight markup languages with a heavy focus on readability through separation of content and layout layers.
[^4]: Fanguy, Will. 2016. “The Amazing Evolution of Visual Storytelling: Blogging, Instagram, Snapchat, and the Future”. Business 2 Community. <http://www.business2community.com/trends-news/amazing-evolution-visual-storytelling-blogging-instagram-snapchat-future-01557833>
[^5]: '*the amount of mobile traffic now accounts for more than half of total internet traffic*' “Cisco Visual Networking Index: Global Mobile Data Traffic Forecast Update, 2015–2020 White Paper”. 2016. Cisco. <http://www.cisco.com/c/en/us/solutions/collateral/service-provider/visual-networking-index-vni/mobile-white-paper-c11-520862.html>
[^6]: I'm doing this manually through command line for now, but there's several automation options including using [Travis-CI](https://travis-ci.org/) for the more hardcore blogger.
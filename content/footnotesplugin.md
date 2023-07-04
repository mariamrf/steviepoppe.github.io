Title: Pelican Plugin: CSS-only footnote pop-up
Category: Technical
Tags: Pelican, Markdown, Python, Footnotes
Author: Stevie Poppe
Date: 2016-08-25
Status: published

<!-- PELICAN_BEGIN_SUMMARY -->

Footnotes are a classic staple in any writer's toolbox, allowing them to, in an unobtrusive way, cite sources or display additional information not directly related to the original argument. Nevertheless it is my impression that online footnotes, through the way they are often implemented imitating printed media footnotes, come over quite counterintuitive and force the reader to disrupt his reading flow,failing to make use of today's extensive web design possibilities.

As I royally use footnotes in my markdown writing work-flow[^1] I figured I'd get acquainted with the Pelican documentation a bit and write a small unobtrusive CSS pop-up plugin to display these on hover for those devices that support it.[^2]

<!-- PELICAN_END_SUMMARY -->

My solution is pretty rough and based on the way Python-Markdown parses markdown into HTML. As it's a quick 'n dirty workaround untested with other parsers, I have no intention to further maintain this code so feel free to use it however you'd like.

```python
    def content_object_init(instance):

        if instance._content is not None:
            content = instance._content
            soup = BeautifulSoup(content, 'html.parser')

            if 'sup' in content:
                footnotes = soup.find(class_="footnote").find_all('p')
                footnoteref = soup.find_all(class_="footnote-ref")

                for index, item in enumerate(footnotes):
                    footnoteref[index].parent['class'] = 'popup_footnote'
                    tag = soup.new_tag('span')
                    tag.append(BeautifulSoup(item.decode_contents(), 'html.parser'))
                    footnoteref[index].insert_after(tag)

            instance._content = soup.decode()

    def register():
        signals.content_object_init.connect(content_object_init)
```

For simplicity's sake I use the BeautifulSoup library to locate all footnote references and their respective footnotes. Then I loop through them and copy the contents of the footnote in a 'popup_footnote' span I append to the footnote reference container.

Styling is done in CSS. Below is my markup. I use `left: 50%;` `transform: translate(-50%, 0);` to center the absolute-positioned pop-up over the footnote reference.

``` css
	sup.popup_footnote span {   
	    text-align: justify;
	    z-index: 10;
	    display: none; 
	    padding: 5px;
	    line-height: 16px;
	    opacity: 0.9;
	    border-radius: 4px;
	    box-shadow: 5px 5px 8px #D4D4D4;
	    top: 10px;
	    left: 50%;
	    transform: translate(-50%, 0);
	    position: absolute; 
	    width: 250px;
	}

	sup.popup_footnote:hover span{
	    display: inline; 
	    color: #111;
	    border: 1px solid #eaeaea;
	    background-color: #fffcfc;
	  }
```

The downside to this CSS-only implementation (next to having double content in your markup) is that it fails to respond well to responsive design. Fixed-size pop-ups relative to the footnote pointer could result in a potential screen overflow. If this is an issue, the only alternative is using jquery and calculate the position of your reference relative to the window border and use this to calculate an ideal pop-up location. Of course if you're relying on the jquery library either way you might as well use that to copy the footnote on hover instead of above's solution. For such an example, I recommend [ignorethecode.net's solution](http://ignorethecode.net/blog/2010/04/20/footnotes/).

[^1]: The difficulty writing web-content with footnotes is distinguishing footnotes or direct links. I generally draw the line between source citation as footnote and useful information as direct link.
[^2]: Using `:active` to substitute the lack of proper hover on touch devices wouldn't be effective as these pop-ups display over anchors. A dirty solution would be to use media tags and keep `display:none` for mobile device widths, but with the blurring of lines between touch and mouse input devices lately this is not foolproof.
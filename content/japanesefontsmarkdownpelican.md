Title: Parsing Japanese Text in Markdown-Python for Stylizing and Semantic Purposes
Category: technical
Tags: python, pelican, markdown, Japanese, fonts
Author: Stevie Poppe
Date: 2016-09-06
Status: published

[TOC]

<!-- PELICAN_BEGIN_SUMMARY -->

Due to my studies I (will) often use Japanese in my blog. As I gave some thought to typography and readability, I found the default appearance of Japanese text to be in stark contrast with the rest of my design.[^1] To target specifically Japanese text, I wrote a small Markdown-Python extension for use in static blog generators as Jekyll and Pelican (or pretty much anything that utilizes Markdown-Python to parse Markdown in HTML) and embed such text in a span with the language attribute set to Japanese. The added, and probably more important bonus, aside from styling and semantic reasons, is that this method counters the negative effects of [Han unification](https://en.wikipedia.org/wiki/Han_unification) in so-called CJK-languages.

<!-- PELICAN_END_SUMMARY -->

# Download

I've added the extension on its [own repository](https://github.com/steviepoppe/lang_ja_span_markdown) on my GitHub for anyone interested, but as it serves its purpose for me as-is I have no further interest in maintaining it at the moment.[^2]

# Installation

Copy the `japanese.py` script into your python-markdown extension directory.

If you're using [Pelican](http://docs.getpelican.com/en/latest/) as static site generator, open your project's `pelicanconf.py` and add `'japanese'` to the `MD_EXTENSIONS` list:

``` python
    MD_EXTENSIONS = ['japanese']
```

# Usage

Using a simple regular expression `(\{\{)(.+?)(\}\})`, the extension treats double {} brackets as span tags with a `lang="ja"` attribute.

``` markdown
    {{読書クラブ}}
```

will output

``` html
    <span lang="ja">読書クラブ</span>
```

**Example 1** (fonts): just compare <span style='font-size: 135%;'>{{読書(どくしょ)クラブ}}</span> (custom) to <span style='font-size: 130%;'>読書(どくしょ)クラブ</span> (Meiryo) to <span style='font-size: 130%; font-family: "MS Gothic";'>読書(どくしょ)クラブ</span> (MS Gothic default).[^3]

**Example 2** (unihan): compare the Chinese to Japanese characters: <span style="font-size: 130%; font-family: 'Quicksand',sans-serif;" lang="zh">&#x9686;</span> (<span style='font-size: 135%;' lang="ja">&#x9686;</span>), <span style="font-size: 130%; font-family: 'Quicksand',sans-serif;" lang="zh">誤</span> (<span style='font-size: 135%;' lang="ja">誤</span>), <span style="font-size: 130%; font-family: 'Quicksand',sans-serif;" lang="zh">直</span> (<span style='font-size: 135%;' lang="ja">直</span>).[^4]

# Styling

Although it's a bit of a risk performance-wise, I'm quite a fan of Google's free web-fonts.[^5] Due the complexity of the Japanese character-set, development on these have been slow[^6], but [Google's Noto Font](https://en.wikipedia.org/wiki/Noto_fonts) is getting quite efficient and with the Japanese font set supporting near 7000 characters, it should pose no problem for most web-projects. Since it works better, typography-wise, with the rest of my fonts, I use this one over fonts as Meiryo that are more widespread across all platforms.

Using the CSS below, I ensure max compatibility by using Meiryo and others as fall-back if the page can't connect to Google's font API.

``` css
@import url(https://fonts.googleapis.com/earlyaccess/notosansjapanese.css);

    [lang="ja"] {
      font-family: "Noto Sans Japanese", "メイリオ","Meiryo","ヒラギノ角ゴ Pro W3",
      "Hiragino Kaku Gothic Pro","ＭＳ Ｐゴシック","MS PGothic",Sans-Serif;
      font-weight: 100;
      font-size: 95%;
    }
```

# Further reading

* <http://www.growingwiththeweb.com/2014/03/languages-and-chinese-characters-on-the-web.html>
* <http://nimbupani.com/declaring-languages-in-html-5.html>
* <https://design.studio-umi.jp/blog/google-web-font-japan>
* <http://kanjialive.com/2013/04/selecting-a-better-japanese-font-for-windows-web-browsers/>

[^1]: This is less so on mobile devices. Most Windows web browsers default to MS Gothic, lacking anti-aliasing found in newer fonts as Meiryo, and require some manual adjustments. For maximal compatibility, I prefer to do this in-site. If no further customization is necessary, just adding Meiryo as fall-back font in the page's font-family is sufficient, e.g. `font-family: Arial, Helvetica, Meiryo,sans-serif;`.
[^2]: A possible extension could be one where different regular expressions test for different languages and thus deliver different *lang* attributes. If I find the need for that on my own blog (eg. Korean), I'll update this.
[^3]: For *furigana* support I use a slightly edited version of an existing MD extension available at <https://github.com/djfun/furigana_markdown>.
[^4]: If a multilingual page uses only Japanese, it's sufficient to put a Japanese font as fall-back in the body's font-family. If occasionally Chinese or Korean characters are used as well, this approach, aside from semantic benefits, remains more recommended.
[^5]: I use [Quicksand](https://fonts.google.com/specimen/Quicksand) and [Poirot One](https://fonts.google.com/specimen/Poiret+One) for all my latin-based text on this page, for example.
[^6]: Adobe's competing, subscription-based Typekit apparently offers a wider range of Japanese web-fonts for anyone interested: <https://typekit.com/fonts?script=japanese>.
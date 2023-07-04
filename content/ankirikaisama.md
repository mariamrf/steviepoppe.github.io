Title: A <del>Quick</del> Guide on Using Anki 2: an efficient vocab mining set-up with Anki and Rikaisama
Category: Studies
Tags: Anki, Rikaisama, Tutorial, Japanese, Studying
Author: Stevie Poppe
Date: 2016-09-08
Status: published
Image: anki_header2.jpg
Keywords: Anki, Rikaisama, Rikaichan, Rikai, Tutorial, Japanese, Japan, Study, Animelon, Jnovelformatter, Visual novels

UPDATE 2018~: Rikaisama has been rendered obsolete since 2018 updates broke Firefox’ support of unsigned XUL-based add-ons. Nevertheless, this guide can still prove useful in two ways: further use of Rikaisama through XUL-supporting Firefox-derivatives such as Waterfox, Pale Moon and Basilisk, as well as the list of applications for Browser/Anki-integration listed in the second half of this guide. As I personally use Waterfox, I’ll refer to Waterfox as main option hereafter. Another option is to use Yomichan for Chrome, described [in this updated blog](https://steviepoppe.net/blog/2019/04/a-quick-guide-on-using-anki-5-an-efficient-vocab-mining-set-up-with-anki-and-rikaisama-yomichan/).

[TOC]

So you want to:

* <i class="icon-check"></i> read a Japanese novel without ending up crying yourself to sleep realizing you know *nothing*, Jon Snow?
* <i class="icon-check"></i> learn Japanese by watching anime, but like, for real?
* <i class="icon-check"></i> create beautiful Anki sets filled with handpicked vocabulary, hidden *furigana* reading-aids, AND crystal-clear audio pronunciations, all without spending days of mind-numbing copy-pasting?

Welcome to the lovely world of `Integrated Anki & Rikaisama`!

---

<!-- PELICAN_BEGIN_SUMMARY -->

The hove-over Japanese dictionary plug-in **Rikaichan** and its Chrome variant **Rikaikun** have already been widely established as incredibly helpful tools for reading Japanese online. Nevertheless, one major function remained missing still: a seamless integration with Anki for efficient vocabulary mining. A recent expansion of the original Rikaichan, aptly named **Rikaisama** (it's a *pun*!), adds several new features including communication with the Anki API, *Sanseido Web Dictionary*'s J-J dictionary definitions, access to *J-Pod101*'s audio-files,[^1] and more.[^2] Concretely, this means audio playback of tens of thousands of words and expressions as well as easy integration of new vocab into Anki. Despite these incredibly useful features, Rikaisama remains fairly  about. To counter that, this blog serves as a brief tutorial on setting up a Rikaisama/Anki environment as well as demonstrating some useful real-life use-cases.

<!-- PELICAN_END_SUMMARY -->

# Rikaisama

## Download

Like Rikaichan, Rikaisama is a <del>Firefox</del> Waterfox plugin, available for download on their [sourceforge download page](https://sourceforge.net/projects/rikaisama/files/) (free, of course). If you're an avid Chrome supporter, this one might be worth switching for.

{% img right {static}/images/anki/rikaisama.jpg rikaisama %}

After installation you’ll have two new buttons at your disposal, either already visible at the top-right of your menubar, or in <del>Firefox</del> Waterfox's toolbar.

The left one activates Rikaisama. I just leave it permanently open. The right one switches the Rikaisama lookupbar. I don’t use this one often so I hide it in the toolbox myself, but for now we’ll need it to access Rikaisama’s settings. Open the toolbar and click the right-most icon to open those (after we’re done, click the leftmost icon to deactivate the toolbar).

{% img border fcenter {static}/images/anki/rikaisamatool.png rikaisamatool %}

Rikaisama’s base settings are pretty self-explanatory, and I’ve left most of them to their default values. For our purpose, the Clipboard & Save and Anki tabs will be the most relevant.

## Set-up

[Rikaisama's homepage](http://rikaisama.sourceforge.net/) contains a crude, bare-bones set-up guide covering the basics of linking Rikaisama with Anki. It does however expect technical knowledge of it's readers, which I feel will averse some. I try to simplify things while still explaining *why* we're doing things, since it really is pretty easy to set-up. If you'd rather get straight to the point, just ignore the reasoning parts (or skip to [1.2.4. Usage](#usage) to download a pre-made Anki-set with matching note-type: all you'll have to do then is to change a few Rikaisama settings).

### Anki

First, Anki will need an additional add-on as well in order to allow real-time import. It's 'available' at Ankiweb's [plug-in page](https://ankiweb.net/shared/info/2512410601), although actual installation is done in-app. Open Anki on your desktop, go to **Tools** → **Add-ons** → **Browse & Install**, and copy-paste **2512410601** in the pop-up dialog.

Now, we'll create a new set to contain your Rikaisama-powered cards, a new note-type with fields corresponding to the info you'd like out of rikaisama, and finally a few card-types to test us on on visual recognition, on oral recognition, and on production.[^3] Start by creating a new set, e.g. `rikai-vocab`[^4]. On Windows, press <kbd>CTRL-SHIFT-N</kbd>, or click **Tools** → **Manage Note Types**, to enter the note-type management screen. Click **add**, then **ok** on the next screen, to create a new note type. Call it `Rikai` (do note my excellent graphical skills as seen in the screenshot below ( ͡° ͜ʖ ͡°) )!

{% img border fcenter {static}/images/anki/anki-notetypes-s.jpg anki-notetypes-s %}

Next, select the new Rikai note-type and click **Fields**. We'll rename the current front and backside as `Expression` and `Meaning`, and add two new Fields `Audio` and `Notes` (this one could be used for personal notes or example sentences). If you're interested in pitch accents, add a fifth field `Pitch`. Next, close this screen and click on **Cards**. We'll manage the different cards this note generates as well as it's make-up.

We'll start with some basic layout. Add the following lines to the bottom of the middle Shared Style screen. For optimal learning, we'll keep word readings in *kana* as *furigana* displayed on touch/hover. This way learners are less likely to use them as a crutch.

```css
ruby rt { visibility: hidden; }
ruby:hover rt { visibility: visible; }
```

Next, click the `+` button twice to create two more card-templates. Next, rename (by clicking **More** → **Rename**) templates **Card 1**, **Card 2** and **Card 3** respectively as `Recognition`, `Production`, and `Audio`.

Finally, let's wrap up our Anki set-up by creating the actual card's templates. Each card will question you on one field (the Japanese expression, the English translation and the Audio) and show the answer on the backside along with audio and any potential notes, if present. Your card's templates should look as follows:

**Recognition**

* **Front Template**

```python
{{furigana:Expression}}
```

* **Back Template**

```html
{{FrontSide}}

<hr id=answer>

{{Meaning}}
<br>
{{Audio}}

{{#Notes}}
<br><br>
<b>Notes:</b>
<br>{{furigana:Notes}}
{{/Notes}}
```

**Production**

* **Front Template**

```python
{{Meaning}}
```

* **Back Template**

```html
{{FrontSide}}

<hr id=answer>

{{furigana:Expression}}
<br>
{{Audio}}

{{#Notes}}
<br><br>
<b>Notes:</b>
<br>{{furigana:Notes}}
{{/Notes}}
```

**Audio**

* **Front Template**

```python
{{Audio}}
```

* **Back Template**

```html
{{FrontSide}}

<hr id=answer>

{{furigana:Expression}}
<br>
{{Meaning}}

{{#Notes}}
<br><br>
<b>Notes:</b>
<br>{{furigana:Notes}}
{{/Notes}}
```

---

If you added a fifth field **Pitch**, add `<br><br>{{Pitch}}` to the back templates of those cards.

### Mapping

Now we'll enter our Rikaisama settings on Firefox and ensure our newly created note-type's fields match the ones in Rikaisama's anki settings. You'll have to make some adjustments in both the **Anki** and **Clipboard & Save** tabs, as documented below:

---

**Anki tab**

* **Save format**: `$d[$r]$t$n$t[sound:$a]`

* **Field names**: `Expression Meaning Audio`

If you added the pitch field, this becomes:

* **Save format**: `$d[$r]$t$n$t[sound:$a]$t$p`

* **Field names**:`Expression Meaning Audio Pitch`

Make sure to mark the save audio check-box <i class="icon-check"></i>.

The **field names** field is pretty forward, it contains the field names of the note we just created in Anki. The **Save format** field however is a bit more complicated. It'll contain *tokens* or variables (similar to fields in your Anki note) available for each Japanese word hover-able through Rikaisama. Each field name must have both a corresponding token, marked by a dollar sign and a single letter (eg. `Expression` → `$d`) as well as a token for empty spaces in between. To get our *furigana*, the *kana* reading must be encapsulated next to our expression (eg. `$d[$r]`). The `$a` token contains just the MP3 filename. To get it to play in our cards, we require a correct format (e.g. `[sound:ちょうつがい - 蝶番.mp3]`), hence the `[sound:$a]`.

---

**Clipboard & Save tab**

Anki keeps all of its assets, like audio or images, in a specific folder. Thus, we'll have to adjust the path these audiofiles are saved in rikaisama's settings as well. On a clean Anki install on windows, this folder will probably be something like `C:\Users\your_name\Documents\Anki\anki_username\collection.media`. When located, use that folder's path for your **Saved Audio** path.

{% img border fcenter {static}/images/anki/anki-rikai-clip-s.jpg anki-rikai-clip-s %}

We'll also have to confirm our save format again in this tab. Just copy/paste the one you used in the other tab.

I personally tag all rikai-created ankicards as such, this isn't necessary but it might come of use in your Anki's browser one day.

---

### Dictionaries

A final step in case you haven't used Rikaichan before, is to install some dictionaries files, available at [Rikaichan's homepage](http://www.polarcloud.com/getrcx/). I personally use the **Japanese - Dutch**,[^5] **Japanese English** and **Japanese Names** dictionaries, and sort them in those order in Rikaisama's configuration.

{% img border fcenter {static}/images/anki/rikaisamadict.jpg rikaisamadict %}

### Usage

Now let's test our set-up!

For Rikaisama to recognize which Anki set and which notes to use, we'll have to open anki and enter our set every time we're on hunting spree. If you get a mismatch error, just click **add** and ensure that the selected type is `Rikai` by clicking on the current type and selecting the proper one (just click close again afterwards).

Hover over these two words. A rikai pop with definitions should appear.

{{理解(りかい)}} | {{暗記(あんき)}} (I'm not obsessed, I swear~)

Now, while still hovering over them, type <kbd>r</kbd> (the *Real-Time Import* key) to import these words into your set. Great! (Note that Rikaisama by default does not allow duplicates, so if you try to add an already added word, you'll get an error message.)

I've exported my own copy of this example and uploaded if you want to compare or save yourself the work of creating the note template manually:

* **Download**: [Example set Rikai <i class="icon-download-alt"></i>](https://www.dropbox.com/s/xnj67hqj3cubfn2/Rikai%20vocab.apkg?dl=0)

If there's one downside to this method, it's that an audio reference will be added to your cards regardless if there's a preexisting audio recording online. This is particularly the case with lesser known words or idioms: while reading Harry Potter I've added a few hundred of such cards. To remove these, just open Anki on your desktop computer and select **Tools** → **Control Media**. It will clear all the non-existent audio entries from your cards' Audio fields. Afterwards, click **Tools** → **Empty Cards** to remove all the empty oral-recognition cards.

# Appliances

## Internet

This one goes without saying as that's pretty much the prime objective of this tutorial. If you're a relatively new learner, NHK provides simplified news articles and videos at [NHK Easy News](http://www3.nhk.or.jp/news/easy/). I used these a lot near the end of my first year studying, and it's a neat way to stay up to date with what's going in Japan, or more generally in the world (frankly speaking in this time and age it's best to arm yourself with knowledge anyway).

## Novels

>{{「言い方がまちがってるわ。ウィン、ガー・デイアム　レヴィ・オーサ。『ガー』と長一くきれいに言わなくちゃ」}}[^6]

### JNovelFormatter

[JNovelFormatter](http://forum.koohii.com/post-113458.html) is a neat little tool by the developer of Rikaisama[^7] that converts Japanese literature in .txt format into clean parsed HTML files. Layout is fairly customizable, although I think the original settings are easy on the eye as-is (I like dark backgrounds when reading for hours at a time, makes me feel less like I'm gazing straight into a light-bulb). End of sentence dots get turned into book-markable anchors so you won't lose track of your progress.

{% img border fcenter {static}/images/anki/anki-jnovel.jpg anki-jnovel %}

I highly recommend this method! I've used this approach while reading *The Girl Who Leapt Through Time* ({{時(とき)をかける少女(しょうじょ)}}) during our {{読書(どくしょ)クラブ}}'s book-reading sessions and just last week, as a kind of summer project, worked my way through the first *Harry Potter* (a surprisingly high difficulty but I know the original by heart so that helped heaps context-wise).

As for resources, there's plenty to be found online. Light novels are commonly uploaded in text format and probably a good starting point for the more advanced learner.[^8] I've heard *Zero no Tsukaima* ({{ゼロの使魔(つかいま)}}) and *Kino no Tabi* ({{キノの旅(たび)}}) are relatively easy reads, for example.[^9]

### Aozora

[Aozora](http://www.aozora.gr.jp/), pretty much the Japanese Gutenberg project, freely hosts tons of public-domain books online.[^10] Check out Natsume Soseki's classic Botchan as [example](http://www.aozora.gr.jp/cards/000148/files/752_14964.html). Their literary standards are a bit higher as the typical light novel so it's quite an adjustment, but great for those who're looking for easy-to-find, legally obtainable literature.

## Anime

A really cool concept recently released is Animelon's multi-layer subtitled anime streaming web-app, akin to the [Erin's Challenge](https://www.erin.ne.jp/en/) video's (except with arguably way more interesting content: as of date there are over 60 series hosted, mostly all big names ranging from more recent hits as SAO and Attack on Titan to classics as Fullmetal Alchemist: Brotherhood and Clannad).

If I were to recommend one to start with, I might pick Clannad.[^11] The high-school setting means relatively easy and casual vocabulary (as opposed to, for example, SAO's highly technical and fantasy-related vocab you'll barely ever encounter in real life), while the voice-acting's pacing is calm enough to pick up as relative beginner, and devoid of difficult accents.

Check out their video demonstration below to see the various possibilities:

{% youtube meUmHCcjlcQ %}

What bothers me a bit is the legality of it all. They're currently keeping this site up as proof-of-concept in search of potential buyers but meanwhile they're hosting full series in HD quality "for educational purposes only".

## Gaming

This one's a bit tricky still. The new web-possibilities since the implementation of the latest HTML-standard, HTML5, have given rise to a broad range of games running natively in your browser without the need for additional clutter such as Adobe Flash. Visual novels, in particular, would be most suitable for our purpose considering the dense amount of words in each game. Unfortunately so far the online playable ones I've found were either already translated into English, or else of the early '90s *abandonware* *eroge* kind, so not what I was looking for (you'll easily find that online if that's your cup of tea).

Another option is to set up your gaming environment in such a way it enables you to use these features. There's an active community of technically capable Japanese learners at [Reddit](https://www.reddit.com/r/visualnovels/wiki/vnhooking) and [Koohii](http://forum.koohii.com/thread-10386.html) who came up with such a thing. I've yet to try this myself, and honestly, it's a bit bloated, but if you're dying to play visual novels and learn Japanese at the same time, this'll do the trick:

1. Get [Visual Novel Reader](http://sakuradite.com/wiki/en/vnr): it appears to be a mask to be run over an already installed visual novel, using OCR to capture Japanese text, parse it, and run it through some dictionaries ([Tutorial](http://sakuradite.com/wiki/en/VNR/Tutorial)).
2. Use the [Furigana Inserter](https://addons.mozilla.org/nl/firefox/addon/furigana-inserter/) Firefox Plug-in to automatically copy-paste dialog from your clipboard, obtained dynamically through OCR by above means, to an empty Firefox screen.

If you're running Firefox and your game side-by-side you'll be able to max up your visual novel ankisets in no time, just like this guy!

{% youtube 7djqr-RG26s %}

# Wait! There is more!

The main goal of this post was to introduce a less known, but highly useful, Anki functionality by linking Rikaisama's excellent[^12] pop-up dictionary with Anki's API, as well as show several possible appliances. If you've any further questions, feel free to check out the other articles in this series on Anki, or to leave a comment below.

* [A <del>Quick</del> Guide on Using Anki (effectively) (in an academic context)](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-effectively-in-an-academic-context/)
* [Using Anki's API to contextualize your vocab cards with example sentences](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-3-contextualize-your-vocab-cards-with-example-sentences/)
* [Making the switch: J-J definitions in your vocab cards](https://steviepoppe.net/blog/2016/10/a-quick-guide-on-using-anki-4-making-the-switch-j-j-definitions-in-your-vocab-cards/)

# Further reading

* [AwesomeTTS for Anki](https://ankiatts.appspot.com/): My approach uses JapanesePod101's vast audio library. Occasionally however I encounter words or expressions that have no native spoken audio recorded. If you want audio-completion, this open-source tool allows for text-to-speech in your Anki cards. I use this occasionally on full sentences or korean vocabulary, but the quality of the free TTS engines remains fairly primitive, so your mileage might vary.
* [Learn Japanese Through Videogames](http://www.nihongonobaka.com/learn-japanese-through-video-games/): speaking of videogames, you could also look up videogame scripts ({{セリフ集(しゅう)}}) and vocab-mine from those. This guy wrote a decent blog on that. The recent Phoenix Wright spin-off *Dai Gyakuten Saiban* (a series I'm particularly fond of) has yet to be confirmed to receive a western release, so I'll have to brush up my legal vocab this way before playing.

[^footnote]: Image taken from the 2012 Japanese animated film Wolf Children by Mamoru Hosoda, used under Fair Use doctrine.
[^1]: A popular online language course podcast. They have podcasts ranging from newbie (mostly English) to upper intermediate (100% Japanese). I used to use these in the beginning as the added scripts are quite helpful for raising listening skills. The male, English speaking is notoriously difficult to stand, however, and despite most content being free, they have some iffy marketing techniques. Regardless, they recorded a dictionary's worth of vocabulary in high quality audio for Jim Breen's dictionary, so that's hella cool. Read more: <http://blogs.japanesepod101.com/blog/2009/04/20/biggest-announcement-ever-edict-japanese-dictionary-now-with-audio-for-every-clip-must-hear>
[^2]: Other useful features include pitch order, updated frequency lists, and EPWING dictionary support if you're into that. The full list is on their homepage.
[^3]: I'll assume concepts like notes and types are somewhat clear to the reader. If not, I refer to that particular section of my previous Anki article [Creating your own cards… *Efficiently*!](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-effectively-in-an-academic-context/#creating-your-first-set-and-cards) for a more detailed guide on notes and setting up templates.
[^4]: I personally keep several sets containing *rikai-powered* cards. A set for each new book I read, sets for vocab related to my studies, and a set for whatever I come across online. I do this to keep my priorities in check: during exams I give less priority to keeping up to date with my books/misc vocab.
[^5]: Courtesy of Leuven University's very own Japanology department! More info on the Waran Jiten Japanese-Dutch dictionary at <http://japansnederlandswoordenboek.org/index.php/Hoofdpagina>
[^6]: The single most satisfying scene from the Japanese edition of the first Harry Potter novel.
[^7]: Actually, this guy made a lot of surprisingly helpful tools for learning Japanese, including the more popular *subs2srs* for creating Anki sets based on subtitles and video, and OCR Manga Reader, a manga reader with Rikaichan-like functionality using optical character recognition. Full list is at <http://rtkwiki.koohii.com/wiki/Community_Tools>
[^8]: I'll refrain from linking here as that's legally gray territory.
[^9]: Then again, Joyce's Ulysses is probably an easy read as well compared to the likes of Proust's In Search of Lost Time, so I'll come back to this statement when I've judged for myself.
[^10]: According to Wikipedia, they host over 10.000 works including both out-of-copyright works or those made freely available by the authors. Read more: <https://en.wikipedia.org/wiki/Aozora_Bunko>
[^11]: If you're watching Clannad: After Story afterwards, keep tissues at hand.
[^12]: Actually, while Rikaisama improves greatly upon Rikaichan, there's still some features I'd like to see implemented such as the ability to display sanseido-mode J-J as well as default J-E at the same time, or to select which definition to ankify. The developer set up a [to-do list](http://rikaisama.sourceforge.net/wishlist.html) of sorts, but as it's a one-man hobbyist project I'll expect these to be implemented rather slowly.
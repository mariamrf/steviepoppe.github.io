Title: A <del>Quick</del> Guide on Using Anki 4: Making the switch - J-J definitions in your vocab cards
Category: Studies
Tags: Anki, Tutorial, Japanese, Studying
Author: Stevie Poppe
Date: 2016-10-02
Status: published
Image: anki_header2.jpg
Keywords: Anki, Rikaisama, Tutorial, Japanese, Japan, Study

!!! Note "2021 Update"
    As of September 30, 2020, Sanseido [stopped](sanseido-publ.co.jp/sp/wbdct_close.html) their web dictionary service. This tutorial is thus rendered obsolete. [Kokugo Jiten Online](https://kokugo.jitenon.jp/) seems like a good alternative. I'll look into updating the Sanseido add-on to use the above instead.

[TOC]

<!-- PELICAN_BEGIN_SUMMARY -->

You've been studying Japanese for a while now and reached a level of Japanese adequate enough to understand (simple) texts. Drilling new vocabulary has become a daily routine so entangled in your lifestyle you barely notice anymore. If you were to describe your current level of proficiency, you'd proudly present yourself as an intermediate level learner. Sounds familiar? Let's take it a notch further by adding Japanese definitions[^1] to our Anki-sets and reduce our dependency on English definition crutches!

<!-- PELICAN_END_SUMMARY -->

If you've followed my [previous tutorial](#) on adding Japanese example sentences to your vocabulary cards, this tutorial will feel very similar: we'll install an Anki add-on, alter our card-layout to display the definitions in a fashionable manner, and finally bulk-edit our existing cards to actually add them. (This might be my first tutorial worthy of the header **quick**).

#Sanseido add-on

There are various online monolingual dictionaries for Japanese vocabulary. I personally like [Weblio](http://www.weblio.jp) and [Goo](http://dictionary.goo.ne.jp/), but for our Anki cards we'll use [Sanseido](http://www.sanseido.net/) - their definitions are usually more concise as the other dictionaries and tend to employ more comprehensible vocabulary. Luck has it someone has already written an anki add-on to serve our blog's purpose. The result of our work will look as follows:

{% img fborder fcenter {static}/images/anki/anki-gyakuten.jpg anki-gyakuten %}

## Download

The **Sanseido Definitions** add-on has a page on Ankiweb's [plug-in page](https://ankiweb.net/shared/info/1967553085), but as usual we'll install the plug-in using the Desktop Anki application. Go to **Tools** → **Add-ons** → **Browse & Install**, and copy-paste **1967553085** in the pop-up dialog. Restart the application to complete the installation.

##Set-up

The note-types of the vocabulary you want Japanese definitions for will need a new field to contain the definition. On the desktop Anki application, press <kbd>CTRL-SHIFT-N</kbd>, or click **Tools** → **Manage Note Types**, to enter the note-type management screen. Select the note-type of the cards you'd like to contain example sentences and click **fields**.

{% img fborder fcenter {static}/images/anki/anki-notetype-select.jpg anki-notetype-select %}

On the next screen, click **add** and call the field `Sanseido`. Now close this screen. On the previous note-type management screen, click **cards**. We'll edit our lay-out and display the new field in our cards.

## Anki Note Lay-out

**Lay-out**

Add the CSS code below to the shared style screen of your note's card-type template.

```css
.title {font-size:16px; color: #999999;}
```

**Templates**

Add the following code below the line displaying your vocabulary's translation/English definition (eg. `{{Meaning}}`) . You'll do this in **Expression** → **Back Template**, **Meaning** → **Front Template** and **Audio** → **Back Template**.

```html
<br/>{{#Sanseido}}
<br/><div id="japanese_meaning">
<span class= "title">Japanese:</span><br/>
<span id= "japanese" class="sanseido">
{{furigana:Sanseido}}<br/><br>
</span></div>
{{/Sanseido}}
```

---

##Bulk-edit

Open Anki's browser (by pressing <kbd>b</kbd> or clicking **Browse** from the main window). The left of this browser has an overview of all your different sets and tags. Select the deck or tag containing the cards you'd like to edit. Press <kbd>ctrl-a</kbd> to select all of those and click **Edit** → **Regenerate Sanseido Expression**. It will crawl the internet for each new definition so this might take quite a while.[^2]

{% img border fcenter {static}/images/anki/anki-browser2.jpg anki-browser2 %}

**Note**: the plug-in expects your vocabulary to be contained in a field called `Word`. If your field is called `Expression`, you'll have to edit this in the plug-in's python file on your Anki's add-on folder (e.g. `C:\Users\your_username\Documents\Anki\addons\sanseidoDefsForAnki.py`). Open it with your text-editor of choice (notepad is fine) and change `expressionField = 'Word'` to `expressionField = 'Expression'`.

**EDIT**: as of July 2017, Sanseido's domain changed from .net to .biz. As mentioned in the comments section, you'll have to manually edit **sanseidoDefsForAnki.py**, search for `sanseido.net` and replace it with `sanseido.biz` for it to work. Alternatively, replace the file with the one on my github repository linked below.

# Usage with Rikaisama / Real Time Import

As with my previous tutorial, a drawback to this plug-in is that it does not support vocabulary formatted to use *furigana*, and neither can Japanese definitions be added automatically on adding a new note through Rikaisama. We'll have to make some small adjustments for that.

I've added the edited files on a [new repository on my GitHub account](https://github.com/steviepoppe/anki_addon_edits/tree/master/jj_tutorial) so go ahead and replace the existing add-on files on your Anki's add-on folder on your computer (e.g. `C:\Users\your_username\Documents\Anki\addons`) with the ones on there. I've described all my edits below in case you'd prefer to do this manually. Feel free to skip this part if you're not technically inclined.

## Set-up

**sanseidoDefsForAnki.py**

We've set up our notes to show *furigana* on our vocabulary. This requires square brackets (eg. `気象庁[きしょうちょう]`). The Anki plug-in for Sanseido definitions however does not support this out of the box. For that reason, I've added a single line of code that uses a regular expression to only use the contents up to the first square bracket as expression.

```python
term = re.search(r'^[^\[]+',term).group(0)
```

If you'd like to edit this yourself, add the next line of code as first line in the `fetchDef` class - it should be around line 27 (`def fetchDef(term):`).

**Real-Time_Import_for_use_with_the_Rikaisama_Firefox_Extension.py**

This extension calls on Anki's API to create new notes. I haven't found a way to hook japanese_examples to outside note-creation, so instead I've edited the real_time_import plug-in itself to call japanese_examples at run-time.

First, we'll have to import that extension to be able to call it's methods. If you're doing this set-up manually, add the next line near the top, with the other includes (around line 30).

```python
from sanseidoDefsForAnki import *
```

Next, I've written a few lines in the `createNote` method to call sanseidoDefsForAnki's glossNote method at run-time and, if examples were found and our note-type has the correct destination field, add these to our newly created card. This should come before `dupOrEmpty = note.dupeOrEmpty()` around line 100.

```python
# Create sanseido definitions
try: glossNote( note )
except:
    showTooltip("Error, could not create sanseido definition.");
try: note.flush()
except:
    showTooltip("Error, could not create sanseido definition.");
```

## Contextualizing imported cards

If you've followed above steps, every time you add a new word online by pressing <kbd>r</kbd> (the *Real-Time Import* key) while hovering over something Japanese, it'll automatically contain a Sanseido dictionary definition as well.

Try it out on this article's "**Words of the Day**"!

    {{逆転(ぎゃくてん)}} | {{裁判(さいばん)}}

# Download Example Set

As usual, I've exported my own Anki copy of this tutorial and uploaded it in case you'd like to compare or save yourself the work of editing the note template yourself. It includes work from the previous two tutorials.

* **Download**: [Example set Sanseido <i class="icon-download-alt"></i>](https://www.dropbox.com/s/9wrpciaawfxeuo5/Rikai%20vocab_jj.apkg?dl=0)

# Wait! There is more!

The main goal of this post was to introduce another less known, yet highly useful Anki functionality for increasing your study efficiency, as well as hopefully create an attitude of self-reliability by pointing out various tools and possibilities. If there are any further questions, feel free to check out the other articles in this series on Anki or to leave a comment below.

* [ A <del>Quick</del> Guide on Using Anki (effectively) (in an academic context)](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-effectively-in-an-academic-context/)
* [Setting up a perfect vocab-mining environment with Anki and Rikaisama](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-2-an-efficient-vocab-mining-set-up-with-anki-and-rikaisama/)
* [Using Anki's API to contextualize your vocab cards with example sentences](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-3-contextualize-your-vocab-cards-with-example-sentences/)

[^footnote]: Image taken from the 2012 Japanese animated film Wolf Children by Mamoru Hosoda, used under Fair Use doctrine.
[^1]: Google `Anki JJ` and you'll come across dozens of posts describing the "*leap from the J-E to J-J dictionary*". It appears to be one of the more popular studying methods amongst self learners online, and is highly blogged about on such blogs as [Japaneselevelup.com](http://japaneselevelup.com/beating-the-anki-j-j-branches-1-earn-your-battle-scars/) or on the koohii.com forums.
[^2]: It takes a couple of seconds for one card. At time of writing, I had 20761 cards based on the Rikai note type; parsing these took about an hour and a half.
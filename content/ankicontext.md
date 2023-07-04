Title: A <del>Quick</del> Guide on Using Anki 3: contextualize your vocab cards with example sentences
Category: Studies
Tags: Anki, Tutorial, Japanese, Studying
Author: Stevie Poppe
Date: 2016-09-17
Status: published
Image: anki_header2.jpg
Keywords: Anki, Rikaisama, Tutorial, Japanese, Japan, Study, 10 000 sentences

[TOC]

So you've followed [my previous tutorial](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-2-an-efficient-vocab-mining-set-up-with-anki-and-rikaisama/) and set up this wonderful environment for creating vocabulary cards with audio and *furigana* based on all kinds of Japanese text you find online. Yet, while studying your new set, you feel this nagging feeling deep down inside... There's something missing, still... "*Hm, could it be...?*", you ponder quietly. **Yes**. You need `Japanese example sentences for providing context to your vocab cards`!

---

<!-- PELICAN_BEGIN_SUMMARY -->

One of the common pitfalls of learning Japanese vocabulary through Anki cards is memorizing them loose of context. Perhaps you've found yourself in a situation having no particular problems recalling vocabulary whilst reviewing your cards, but less so when confronted with real-life situations. If that sounds familiar, one way to counter this common problem would be to install an additional Anki add-on, and bring our vocab cards to a next level by adding Japanese example sentences and their translations. This blog offers an easy step-by-step tutorial on setting this up. Additionally, for those who've followed my previous tutorial, I add some extra code to combine the example sentence functions with the instant-import features of the Firefox plug-in Rikaisama.

<!-- PELICAN_END_SUMMARY -->

# Plug-in

We'll use an existing Anki add-on called **Japanese Example Sentences** to add Japanese sentences taken from [Tatoeba.org](https://tatoeba.org/eng/), a "collaborative, open, free and even addictive" community on producing example sentences. The result of our work will look as follows:

{% img fborder fcenter {static}/images/anki/anki-contextcard.jpg anki-contextcard %}

## Download

The Japanese Example Sentences add-on has a page on Ankiweb's [plug-in page](https://ankiweb.net/shared/info/2413435972), but as usual we'll install the plug-in using the Desktop Anki application. Go to **Tools** → **Add-ons** → **Browse & Install**, and copy-paste **2413435972** in the pop-up dialog. Restart the application to complete the installation.

**Edit**: as user *nwt* mentioned in the comments, this example-set is fairly outdated. Follow [the instructions](https://ankiweb.net/shared/info/2413435972) left in the plug-in's comment section to update to the most recent set.

If you want a test Anki deck to work with, I've uploaded an example set, the result of my previous Anki tutorial, containing the necessary notetype and two test-notes for download: [Example set Rikai <i class="icon-download-alt"></i>](https://www.dropbox.com/s/xnj67hqj3cubfn2/Rikai%20vocab.apkg?dl=0).

##Set-up

The note-types of the vocabulary you want sentences for will need a new field to contain these. On the desktop Anki application, press <kbd>CTRL-SHIFT-N</kbd>, or click **Tools** → **Manage Note Types**, to enter the note-type management screen. Select the note-type of the cards you'd like to contain example sentences and click **fields**.

{% img border fcenter {static}/images/anki/anki-notetype-select.jpg anki-notetype-select %}

On the next screen, click **add** and call the field `Examples`. Now close this screen. On the previous note-type management screen, click **cards**. We'll edit our lay-out and add the sentences in our actual cards.

## Anki Note Lay-out

Add the code to the bottom of the middle lay-out screen. It'll display the example sentences to the left of your cards.

```css
.examples {font-size:75%; text-align: left;}
.title {font-size:16px; color: #999999;}
```

* **Back Template**

Add the following HTML code at the bottom of your different cards' back templates. As pointed out in the comments, `lang="ja"` serves to render characters correctly, rather than in simplified Chinese due Han unification.

```html
{{#Examples}}
<br/>
<div class="examples" lang="ja">
<span class= "title">Sentences:</span><br/>
{{furigana:Examples}}
</div>
{{/Examples}}
```

{% img fborder fcenter {static}/images/anki/anki-notetype-back.jpg anki-notetype-back %}

When done, close both this and the previous screen. Let's try this plug-in out now!

#Usage

## Contextualizing existing cards

We'll start by adding example sentences to our existing cards (of the note type we've just edited). Press ++b++ or click on "Browse" to open Anki's Card Browser. The left of this browser has an overview of all your different sets and tags. Select the deck or tag containing the cards you'd like to edit. Press ++ctrl+a++ to select all of those and click **Edit** → **Bulk-add examples**. Most, if not all, should contain sexy new example sentences by now.

{% img fborder fcenter {static}/images/anki/anki-browser.jpg anki-browser %}

## Contextualizing new cards

While creating a new card of a note-type that contains the **Examples** field, the add-on will automatically fill in that field as soon as you've entered a Japanese expression in the **Expression** field. No further set-up is required for this.

# Usage with Rikaisama / Real Time Import

A drawback to this plug-in is that it does not support vocab expressions using *furigana*, and neither can example sentences be added automatically on adding a new note through Rikaisama. I've you've read my [previous blogpost](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-2-an-efficient-vocab-mining-set-up-with-anki-and-rikaisama/), you'll probably want to to follow these next steps as well.

I've made some adjustments to both the Anki Real-Time Import add-on and the Japanese_Examples add-on. I've added the edited files on a [new repository on my github](https://github.com/steviepoppe/anki_addon_edits/tree/master/context_tutorial) so go ahead and replace the existing add-on files on your Anki's add-on folder on your computer (e.g. `C:\Users\your_username\Documents\Anki\addons`) with the ones on there.

I've described all my edits below in case you'd prefer to do this manually. Feel free to skip this part if you're not technically inclined.

## Set-up

**japanese_examples.py**

We've set up our notes to show *furigana* on our vocabulary. This requires square brackets (e.g. `気象庁[きしょうちょう]`). The anki plug-in for Japanese example sentences however does not support this out of the box. For that reason, I've added a regular expression to only use the contents up to the first square bracket as expression.

```python
searched = re.search(r'^[^\[]+',expression)
if searched:
    expression = searched.group(0)
```

If you'd like to edit this yourself, add that piece of code to the `find_examples` class right after it defined `examples` as a list. it should be around line 139 (`def find_examples(expression, maxitems):` `examples = []`).

**Real-Time_Import_for_use_with_the_Rikaisama_Firefox_Extension.py**

This extension calls on Anki's API to create new notes. I haven't found a way to hook Japanese_examples to external note-creation, so instead I've edited the *real_time_import* plug-in itself to call japanese_examples at run-time.

First, we'll have to import the japanese_examples extension to be able to call its methods. If you're doing this set-up manually, add the line below near the top, along with the other includes (around line 30).

```python
from japanese_examples import *
```

Next, I've written a few lines in the `createNote` method to call Japanese-examples' find method at run-time and, if examples were found and our note-type has the correct destination field, add these to our newly created card. This should come before `dupOrEmpty = note.dupeOrEmpty()` around line 100.

```python
# for use with japanese examples
examples = find_examples_multiple(note, MAX_PERMANENT)

# if field is empty and examples exist
if examples and not n[DEST_FIELD]:
    note[DEST_FIELD] = examples
```

Finally, I've edited the mark-up of the example sentences themselves to hide the English translations unless hovered above (or on press on smart phones). Locate the `examples.append` call in the `find_examples` method. You'll want to replace it (I commented it out) with the line below. It'll be around line 174.

```python
examples.append("<div id='eng_test'>%s<span id='eng_sentence'>%s</span></div>" % tuple(example.split('\t')))
```

In the `find_examples_multiple` method (around line 214), replace the current `return` with the following line. We want only one break between example sentences.

```python
return "<br>".join(examples)
```

---

**Important!** For this to work, you'll need to make an edit to your note template's layout. As usual enter the note-type management screen by pressing ++ctrl+shift+n++, or click **Tools** → **Manage Note Types**. Select the notetype of the cards you'd like to contain example sentences and click **fields**. From there, select the `Rikai` note, click **cards** and add the following CSS code to the bottom of the shared lay-out screen in the middle.

```css
#eng_sentence { display: none; }
#eng_test:hover #eng_sentence{ display: inherit; color: #eb4c42;}
```

#New Usage

## Contextualizing existing cards

If you've set up Rikaisama to include *'rikai'* as tag on new cards, this should be a breeze. Open Anki's browser (by clicking **Browse** or pressing ++b++), select the *rikai* tag in the left column, and press ++ctrl+a++ to select all your cards. Next, click **Edit** → **Bulk-add examples**.

## Contextualizing imported cards

If you've followed above steps, every time you add a new word online by pressing ++r++ (the *Real-Time Import* key) while hovering over something Japanese, it'll automatically contain example sentences as well.

Try it out on our new "**Words of the Day**"™!

>{{文脈(ぶんみゃく)}} | {{語彙(ごい)}}

# Download Example Set

As usual, I've exported my own copy of this tutorial and uploaded it in case you'd like to compare or save yourself the work of editing the note template yourself.

* **Download**: [Example set Sentences <i class="icon-download-alt"></i>](https://www.dropbox.com/s/2lq0d7cn2rqywih/Rikai%20vocab_context.apkg?dl=0)

# Wait! There is more!

The main goal of this post was to introduce another less known, but highly useful, Anki functionality on increasing your study efficiency, as well as hopefully create an attitude of self-reliability by reaching out various tools and possibilities. If you've any further questions, feel free to check out the other articles in this series on Anki, or to leave a comment below.

* [ A <del>Quick</del> Guide on Using Anki (effectively) (in an academic context)](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-effectively-in-an-academic-context/)
* [Setting up a perfect vocab-mining environment with Anki and Rikaisama](https://steviepoppe.net/blog/2016/09/a-quick-guide-on-using-anki-2-an-efficient-vocab-mining-set-up-with-anki-and-rikaisama/)
* [Making the switch: J-J definitions in your vocab cards](https://steviepoppe.net/blog/2016/10/a-quick-guide-on-using-anki-4-making-the-switch-j-j-definitions-in-your-vocab-cards/)

# Further reading

* [The 10 000 Sentences Method](http://learnanylanguage.wikia.com/wiki/10000_Sentences): one of the more popular online self-study methods seem to be the complete Japanese immersion ([All Japanese All The Time](http://learnanylanguage.wikia.com/wiki/AJATT)) method and its 10 000 sentences style of learning: increasing the feel of a language by assimilating and internalizing 10 000 different sentences. To be honest, the arbitrary number of sentences and clickbaitfish descriptions make it pretty gimmicky ("*Learn Japanese in just 18 months*!"[^1]), but its popularity should give some validity on the importance of example sentences in your vocab-learning.

[^footnote]: Image taken from the 2012 Japanese animated film Wolf Children by Mamoru Hosoda, used under Fair Use doctrine.
[^1]: I've read enough blogs on learning Japanese or language acquisition to come up with my own gimmicky clickbait articles as "*Use these methods to watch your Japanese learning abilities soar*" or "*Break the Plateau: 10 easy tips to Master Japanese*" and cash in on ads or selling e-books, but honestly I'm just some guy on the internet learning Japanese and occasionally blogging about cool, potentially useful features. Maybe if I actually sticked on studying instead of needlessly browsing the internet I could've actually made such claims, but no... It's stronger as myself...
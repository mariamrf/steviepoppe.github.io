Title: A <del>Quick</del> Guide to Data-mining & (Textual) Analysis of (Japanese) Twitter Part 2: Basic Metrics & Graphs
Category: Studies
Tags: Big Data, Digital Humanities, Japanese, Python, Tutorial,Twitter
Author: Stevie Poppe
Date: 2020-05-15
Status: published
Image: anki_header2.jpg
Keywords: Big Data, Digital Humanities, Japanese, Python, Tutorial,  Twitter, Japanese, Japan, Study
Slug: a-quick-guide-to-data-mining-textual-analysis-of-japanese-twitter-part-2

*This short series of blogs chronicles the bare-bones required to conduct a basic form of social media analysis on corpora of (Japanese) Tweets. It is primarily intended for **undergraduate and graduate students** whose topics of research include contemporary Japan or its online vox populi, and want to strengthen their existing research (such as an undergraduate thesis or term paper) with a social media-based quantitative angle.*

[TOC]

<!-- PELICAN_BEGIN_SUMMARY -->

The purpose of this second blog is two-fold: 1) to introduce the reader to some possibilities in regards to basic social media analysis (applicable almost immediately upon having [finished the previous guide](https://steviepoppe.net/blog/2020/04/a-quick-guide-to-data-mining-textual-analysis-of-japanese-twitter/)), and 2) to touch upon a crucial, yet sometimes ignored aspect of social media analysis: the legal and ethical caveats regarding privacy and informed content when researching user-generated content on social media.

By using a concrete, real-world example, we will thus:

* <i class="icon-check"></i> Think about how we might integrate Twitter analysis into our project,
* <i class="icon-check"></i> Use the Python scripting language to further process our dataset to our needs and obtain relevant metrics,
* <i class="icon-check"></i> Use spreadsheet software such as Openlibre or Excel to produce pivot tables and graphs,
* <i class="icon-check"></i> Reflect on the ethical and legal ramifications of working with social media data in academic research.

<!-- PELICAN_END_SUMMARY -->

# Context

I assisted several third-year BA students working on a group essay covering aspects of the COVID-19 virus and marital issues within a larger framework of hegemonic masculinity, femininity and gender hegemony in Japan. Their choice of incorporating an element of social network analysis was not ungrounded. Correlating to increased remote work measures taken in Japan as a COVID-19 precaution, several hashtags concerning marital issues began to trend on Japanese Twitter starting Mid-April 2020 and saw further acceleration after being promptly picked up on by several news outlets and tabloids both within- and outside of Japan (such as the Japanese hashtag #*coronadivorce*, #*koronarikon* #コロナ{{離婚(りこん)}}).

One of my research interests concerns the many ways the internet, as a cultural artifact, augments or subverts our personal reality. Of interest to this project, then, was how the explosion in usage of the above hashtags reifies in Japan a situation that is undoubtedly being felt worldwide among many (married) couples during the pandemic. Concretely we had several questions: how does Twitter (and general social media usage) fit within the lives of struggling couples trying to cope with the uncertainty of the Corona crisis and its amplification of internal relational struggles? Does the usage of those hashtags reveal any attempts on Twitter to interconnect with one another, form communities and to share advice or frustrations? If so; can we pinpoint particular group dynamics? Might we find a steady increase of Twitter users empowered enough to engage in discourse with each other, or is its usage mostly limited to a form of semi-public, anonymous diaries kept by a small, stable group of users venting frustration? Moreover, what are the common topics of these posts? Can they be further divided in larger categories of frustration (e.g. relating to parents-in-law, housework, finances, children, etc)? Finally, what can this, in a greater socio-cultural context, tell us about gender roles and marriage expectations in Japan?

Those are the kind of questions for which quantitative analysis of social media datasets might inductively help to lead the researcher to new theories, or instead strengthen one’s existing hypotheses. Having completed the previous tutorial and given a bit more work outlined below, this blog post introduces the reader to some very basic metrics and graphs that could already assist us in shedding some light on the above questions.

---

# Preliminary analysis

## Datasource

For the purpose of both this article and the project highlighted above, one specific hashtag tying into the discourse of marital stress on Twitter was taken as the target of our analysis: #husbandstress (*dan’na sutoresu*, #{{旦那(だんな)}}ストレス), using the archaic master / husband (dan’na, {{旦那(だんな)}}) to refer to one’s husband.

The dataset was obtained using our historical search script with the `#!python lang='ja'` option enabled (limiting tweets to the Japanese language) on the above hashtag; ran for the first time on 8 May, 2020 (right after an extended golden week), with subsequent runs on 15 May, 2020, 22 May, 2020 and 29 May, 2020 (with the `since_id` argument set to the ID of the last tweet in each preceding set). The first set includes 886 tweets and retweets from the period between Thu Apr 30 05:55:28 UTC and Fri May 08 14:25:30 UTC.[^1] The second set includes 1178 (re)tweets tweeted between Fri May 08 15:21:46 UTC and Fri May 15 01:04:47 UTC. The third set includes 857 (re)tweets between Fri May 22 15:34:06 UTC and Fri May 15 01:55:21 UTC. The fourth and final set includes 686 (re)tweets posted between Fri May 22 16:51:16 and Fri May 29 13:54:15 UTC.

Note
    It should again be noted that even in the case of a query that has relatively low usage, such as the one used here, the Twitter search API does not guarantee completeness and the results are thus indicators of trends among the engaging audience, rather than exhaustive resources. As stated on [developer.twitter.com](https://developer.twitter.com/en/docs/tweets/search/overview/standard): “The Twitter Search API searches against a sampling of recent Tweets published in the past 7 days. […] the standard search API is focused on relevance and not completeness. This means that some Tweets and users may be missing from search results.”

## Processing & Cleaning

In order to built a clean dataset in CSV format, used to produce a variety of graphs, this blog provides a slightly edited variant of the parsing script from the previous tutorial. Some of the significant changes to the previous script are as follows:

* An option to exclude retweets, or to include more meta-information when opting to keep them
* The addition of `user_mention` information (i.e. other Twitter accounts tagged with @)
* An option to choose the CSV output filename
* An option to **localize time** to the suspected timezone
* An option to calculate the total amount of retweets in our dataset and save tweets predating our calculations that were nevertheless retweeted since
* An option to check for double entries
* Performance & scalability: able to handle millions of rows and files taking up several gigabytes of disk space.

## Pre-processing

Our edited script (also available for download on [GitHub](https://github.com/steviepoppe/python_twitter_api_examples)) thus look as follows:

### Python script

```python
import json
import tweepy
import sys
import csv
import os
import pandas as pd
import ijson
from pytz import timezone
from pathlib import Path
from datetime import date, datetime

def parse_tweets(sys_args):

    file_name = sys_args[1]
    time_zone = sys_args[2] if len(sys_args) > 2 else "utc"
    keep_rt = sys_args[3] if len(sys_args) > 3 else "True"
    save_file_name = sys_args[4] if len(sys_args) > 4 else ('%s_parsed' % file_name)
    add_totals = sys_args[5] if len(sys_args) > 5 else "False"
    check_duplicates = sys_args[6] if len(sys_args) > 6 else "False"
    count_tweets = 0
    exists = os.path.isfile('./results/%s.csv' % save_file_name)

    tweet_list = list()

    with open("./results/%s.json" % file_name, mode='r', encoding="utf-8") as tweet_data:
        tweets = ijson.items(tweet_data, 'objects.item')
        for tweet in tweets:
            entities = tweet["entities"]
            user = tweet["user"]
            hashtags = ()
            user_mentions = ()

            if 'user_mentions' in entities:
                user_mentions = (user_mention["screen_name"] for user_mention in entities["user_mentions"])

            tweet_row = {}
            tweet_row["tweet_id"] = tweet["id"]
            tweet_row["text"] = ""
            tweet_row["hashtags"] = ""
            tweet_row["user_mentions"] = ','.join(user_mentions)
            tweet_row["created_at"] = localize_utc_object(tweet["created_at"],time_zone)

            is_retweet = ("retweeted_status" in tweet)
            if keep_rt == "True":
                tweet_row["is_retweet"] = is_retweet
                tweet_row["retweet_id"] = 0
                tweet_row["retweet_created_at"] = None

            if keep_rt == "True" and is_retweet == True:
                retweet = tweet["retweeted_status"]
                re_entities = retweet["entities"]
                tweet_row["retweet_id"] = retweet["id"]
                tweet_row["retweet_created_at"] = localize_utc_object(retweet["created_at"],time_zone)

                tweet_row["text"] = "RT @" + retweet["user"]["screen_name"] 
                + ": " + (retweet["extended_tweet"]["full_text"] if "extended_tweet" in retweet
                    else retweet["full_text"] if "full_text" in retweet else retweet["text"])

                if 'hashtags' in re_entities:
                    hashtags = (hashtag["text"] for hashtag in re_entities["hashtags"])
                if len(re_entities['user_mentions']) > 0:
                    re_user_mentions = (re_user_mention["screen_name"] 
                        for re_user_mention in re_entities["user_mentions"] if 
                        re_user_mention["screen_name"] not in user_mentions)
                    re_user_mentions = ','.join(re_user_mentions)
                    tweet_row["user_mentions"] += ("," + re_user_mentions)
            else:
                tweet_row["text"] = (tweet["extended_tweet"]["full_text"] if "extended_tweet" in tweet 
                    else tweet["full_text"] if "full_text" in tweet else tweet["text"])

                if 'hashtags' in entities:
                    hashtags = (hashtag["text"] for hashtag in entities["hashtags"])

            tweet_row["hashtags"] = ','.join(hashtags)
            tweet_row["text"] = tweet_row["text"].strip()

            tweet_row["user_screen_name"] = user["screen_name"]
            tweet_row["user_description"] = user["description"]
            tweet_row["user_following_count"] = user["friends_count"]
            tweet_row["user_followers_count"] = user["followers_count"]
            tweet_row["user_total_tweets"] = user["statuses_count"]
            tweet_row["user_created_at"] = 
            localize_utc_object(user["created_at"],time_zone)
            tweet_row["retweet_count_listed"] = tweet["retweet_count"]
            tweet_row["retweet_count_dataset"] = 0

            count_tweets += 1
            tweet_list.append(tweet_row)

    #these are memory intensive, do some garbage collecting
    del tweets
    del tweet_data
    tweet_json = pd.DataFrame(tweet_list)

    with open('./results/%s.csv' % save_file_name, mode='a', encoding="utf-8",newline='') as file:
        tweet_json.to_csv(file, header=(not exists), index = False)

    del tweet_json
    del file

    if check_duplicates == "True":
        remove_duplicate_rows(save_file_name)

    print("Finished processing %s tweets. Saved to ./results/%s.csv" % (count_tweets, save_file_name))

    if add_totals == "True":
        get_retweet_count(save_file_name)

#note, changing the timestring to match the location based on an estimation (by language filters for ex.) is sloppy:
#-> what about Japanese tweets posted abroad? Difficult to detect since utc_offset is no longer supported by Twitter
#https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
def localize_utc_object(time_string, time_zone):
    date_object =  datetime.strptime(time_string, '%a %b %d %H:%M:%S %z %Y')
    if time_zone != "utc":
        date_object = date_object.astimezone(tz=timezone(time_zone)) #for example Asia/Tokyo
    return date_object.isoformat()

# Only way to find duplicates in CSV files that are too large too load in one time is to iterate by chunks
#collecting doubles in the first iteration and removing them in the second one
def remove_duplicate_rows(save_fn):
    double_ids = []
    chunksize = 100000
    count = 0
    header = True

    for chunk in pd.read_csv('./results/%s.csv' % save_fn, chunksize=chunksize, iterator=True):
        double_ids.extend(chunk['tweet_id'].tolist())

    #Get list of double tweet_id
    seen = set()
    seen2 = []
    seen_add = seen.add
    seen2_add = seen2.append
    for tweet in double_ids:
        if tweet in seen:
            seen2_add(tweet)
        else:
            seen_add(tweet)
    del seen

    os.rename("./results/%s.csv" % save_fn,"./results/%s_temp.csv" % save_fn)
    for chunk in pd.read_csv('./results/%s_temp.csv' % save_fn
        , chunksize=chunksize, iterator=True):
        for index, tweet in chunk.iterrows():
            if tweet["tweet_id"] in seen2:
                chunk.drop(index, inplace=True)
                count += 1
                seen2.remove(tweet["tweet_id"])
                print('Tweet ID: %s dropped from CSV.' % tweet["tweet_id"])
        chunk.to_csv('./results/%s.csv' % save_fn, encoding="utf-8",header=header, index = False, mode='a')
        header = False

    print('%d duplicate row(s) removed.' % count)
    os.remove("./results/%s_temp.csv" % save_fn)

def get_retweet_count(file_name):

    chunksize = 100000
    header = True
    line_count = 0
    Path("./results/metrics_%s/" % file_name).mkdir(parents=True, exist_ok=True)

    os.rename("./results/%s.csv" % file_name,"./results/%s_temp.csv" % file_name)

    df = pd.read_csv('./results/%s_temp.csv' % file_name, usecols = ["retweet_id"])
    retweets = df['retweet_id'].value_counts().to_dict()
    if 0 in retweets:
        del retweets[0]

    print("%s unique retweets found. Processing..." % len(retweets))
    for chunk in pd.read_csv('./results/%s_temp.csv' % file_name, chunksize=chunksize, iterator=True):
        for index, tweet in chunk.iterrows():
            if tweet["tweet_id"] in retweets:
                chunk.at[index,'retweet_count_dataset'] = retweets[tweet["tweet_id"]]
                del retweets[tweet["tweet_id"]]
        chunk.to_csv('./results/%s.csv' % file_name, encoding="utf-8",header=header, index = False, mode='a')
        header = False

    os.remove("./results/%s_temp.csv" % file_name)

    print("%s retweets not in data set. Processing..." % len(retweets))

    with open('./results/metrics_%s/%s_old_retweets.csv' % (file_name, file_name), mode='w'
        , encoding="utf-8",newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["tweet_id","text", "hashtags", "user_screen_name",
            "user_mentions", "created_at", "retweet_count", "url"])

        for chunk in pd.read_csv('./results/%s.csv' % file_name
            , usecols = ["tweet_id","text", "hashtags","user_mentions", "retweet_created_at", "retweet_id"]
            , chunksize=chunksize, iterator=True):
            for index, tweet in chunk.iterrows():
                if tweet["retweet_id"] in retweets:
                    if pd.isna(tweet["user_mentions"]):
                        user_mentions = re.findall(
                            r'((?<=^|(?<=[^a-zA-Z0-9-\.]))(?<=@)[a-zA-Z0-9\/_]+(?=[^a-zA-Z0-9-_\.]))'
                            ,tweet["text"])
                    else:
                        user_mentions = tweet["user_mentions"].split(",")
                    screenname = user_mentions[0]
                    f_text = "RT @%s: " % screenname
                    ## There's a rare flaw in the Twitter API that doesn't return the user mention of the og tweeter
                    ## In such cases, use a regular expression
                    f_mentions = ",".join(user_mentions[1:]) if len(user_mentions[1:]) > 0 else None
                    hashtags = None if pd.isna(tweet["hashtags"]) 
                    else tweet["hashtags"]
                    url = "https://twitter.com/%s/status/%s" % (screenname, str(tweet["retweet_id"]))
                    writer.writerow([tweet["retweet_id"]
                        ,tweet["text"].replace(f_text,''), hashtags,
                    screenname, f_mentions, tweet["retweet_created_at"], retweets[tweet["retweet_id"]], url])
                    del retweets[tweet["retweet_id"]]
                    line_count += 1

    print("Finished calculating total tweets. Processed %s old retweets." % line_count)

if __name__ == '__main__':
    parse_tweets(sys.argv)
```

!!! Note
    The script above requires three new external libraries that need to be imported in our script (see **lines 6 - 8**): **[Pytz](https://pypi.org/project/pytz/)** (used for date manipulation), **[ijson](https://pypi.org/project/ijson/)** (used for reading large JSON files in chunks) and **[Pandas](https://pandas.pydata.org/)** (a very powerful data manipulation and analysis library). Before doing so, first install them with the command prompt using **pip** (`pip install pytz`, `pip install ijson` and `pip install pandas`).

### Technical notes

Some technical notes about the above script:

* Twitter adheres to the Coordinated Universal Time (UTC) time standard for date & time information of objects such as tweets and user accounts. If we have strong reason to believe that the tweets in our dataset were tweeted within the same timezone, and if we intend to use that data for our work, we may localize the timezone of all tweets (and/or the Twitter accounts tweeting those) in our dataset (see **lines 8, 15, 41, 53, 78** and **107-111**). In regards to our current dataset, which is fairly limited in size, it is fair to assume that with the possibility of some negligible exceptions, the vast majority (if not all) of those tweets were created within the Japanese timezone.

!!! Note
    Taking into account any daylight saving time adjustments, Pytz uses the UTC offsets of the desired `timezone` for its localization. The time_zone information we’re passing to the above `localize_utc_object` function should adhere to the [TZ database names](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) of the desired country (e.g. **Asia/Tokyo**).

* By adjusting the `mode` argument of the `open` function to `a` (append), rather than `w` (write, which would overwrite any existing files), our script can append the results from a second JSON dataset to an existing CSV file. Furthermore, to ensure that we append results to the same output file every time we want to update our dataset over time, the script now takes an argument to define the filename of the CSV file our results will be written to (see **lines 17** and **90**).
* If we decide to include retweets in our set (useful for meta information on those who retweet content), we could calculate the amount of times tweets have been retweeted based on the amount of retweets of that tweet in our dataset. Using a temporary helper CSV file, the original CSV is then rewritten to include this information.[^2] Moreover, if our dataset contains retweets of original tweets that predate the earliest tweet data we possess, this script further generates a list of those original tweets (e.g. **/metrics/#旦那ストレス_old_retweets.csv**), including information such as tweet ID, text, hashtags, user name of the original tweeter, time of creation, amount of retweets and a direct URL to that tweet (see **lines 16, 49-68, 101-102** and **150-199**).
* When working with JSON data files compiled over a larger period of time, it is not unlikely duplications of tweets might have entered our dataset. In order to remove possible duplicate tweets, a helper function iterates through all rows of a CSV file, keeping track of the rows with a unique ID, and rewrites the output file based on those unique values (see **lines 19, 96-97** and **115-148**).[^3]
* Both scripts on this page use the Pandas data manipulation library to read CSV files in chunks, which slightly impacts speed but drastically reduces memory consumption by iterating over an arbitrary amount of rows at a time (see **lines 6, 89, 91, 159-160, 165-171** and **182-199**).

The script above thus takes several new optional arguments when run in command line. In order, they are:

* The timezone to localize Tweets by (defaults to `'utc'`)
* A boolean to decide whether or not to include retweets (defaults to `True`)
* The name of the output file (defaults to the name of the JSON file with **’_parsed’** attached to it)
* A boolean to decide whether or not to calculate retweets for unique tweets (defaults to `True`)
* A boolean to decide whether to check for doubles in CSV based on the tweet ID (defaults to `True`)

!!! Note
    The command in our command prompt (after first navigating to the correct folder using the change directory command `cd`) will therefore resemble something akin to: `python python_parse_tweet_ver2.py search_tweets_#旦那ストレス_20200515_030826 Asia/Tokyo True #旦那ストレス True True`. That command runs the above python script (**python_parse_tweet_ver2.py**) on a raw JSON file **search_tweets_#旦那ストレス_20200515_030826.json**, localizes the Tweets to Japanese Standard Time (JST), includes retweets, outputs to a CSV file called **#旦那ストレス.csv**, calculates the amount of times tweets have been retweeted since they were tweeted, and finally, checks for any duplicates in the CSV file.

## Metrics & Graphs

### Calculating Metrics with Python

Based on our existing CSV we can now start calculating various metrics and produce graphs with our spreadsheet software of choice. As-is, there is plenty we could do already solely by importing the ‘master CSV’ file generated earlier and using pivot tables and graphs. This blog post, however, provides another script with a variety of helper methods to calculate and export some of the most prevalently used metrics in separate CSV files. This part will therefore, again, briefly elaborate on that python script, before proceeding to demonstrate the kind of visuals that can be extracted from the generated data and how it might fit into one’s research project. The script below thus contains four general helper functions:[^4]

!!! Note
    Similar to before, the script below (available on [GitHub](https://github.com/steviepoppe/python_twitter_api_examples)) should be saved in the folder we have used thus far to store the rest of our script files in (e.g. '**C:/python_examples**' → ‘**python_metrics.py’**).

    The next script take one argument: the name of the input CSV file generated with the script above. The commands used to execute our script could thus respectively look like: `python python_metrics.py #旦那ストレス` (output CSV files are stored in a new folder named after the input, e.g. ‘**/metrics_#旦那ストレス**/’).

* **User data**: generates a list of all unique users in our dataset, including 1) calculated fields such as the amount of tweets and retweets each user has contributed to our dataset or how many times their tweets were retweeted, and 2) general information such user name, description, account creation date, following/follower count and the total amount of tweets (taken at the time of the most recent contribution to our dataset).
* **Hashtag frequency**: generates a list of each unique hashtag, the amount of times it appeared in (re)tweets and the amount of (re)tweeters having used that hashtag.
* **Date frequency**: generates, for each day in our dataset, the amount of tweets, retweets, unique tweeters, retweeters and overlap between tweeters | retweeters in our dataset.
* **Time frequency**: generates the same as above, filtered by hour.

Essentially, this script iterates through each tweet in our input CSV file, storing the required information in python ‘dictionaries’. Upon finishing, it again iterates through each of those python dictionaries, writing the content to helper CSV files containing metrics for each of the four functions defined above.

```python
import json
import sys
import csv
from datetime import date, datetime
import time
from pathlib import Path
import pandas as pd

def parse_tweets(sys_args):

    file_name = sys_args[1]
    keep_rt = sys_args[2] if len(sys_args) > 2 else "True"
    chunksize = 100000
    hashtags = {}
    date_set = {}
    time_set = {}
    user_set = {}
    line_count = 0

    Path("./results/metrics_%s/" % file_name).mkdir(parents=True, exist_ok=True)

    for chunk in pd.read_csv('./results/%s.csv' % file_name, encoding="utf-8", chunksize=chunksize, iterator=True):
        for index, tweet in chunk.iterrows():
            line_count += 1
            is_retweet = 1 if tweet["is_retweet"] == True else 0
            hashtag_metrics(tweet, hashtags, is_retweet)
            date_metrics(tweet, date_set, is_retweet)
            time_metrics(tweet, time_set, is_retweet)
            user_metrics(tweet, user_set, is_retweet, keep_rt)
        print('Processed %s lines.' % line_count)

    print('Processed total of %s lines.' % line_count)
    save_hashtag_metrics(hashtags, file_name)
    save_date_metrics(date_set, file_name)
    save_time_metrics(time_set, file_name)
    save_user_metrics(user_set, file_name)

def hashtag_metrics(tweet, hashtags, is_retweet):
    if not pd.isna(tweet["hashtags"]):
        c_hashtags = tweet["hashtags"].replace(",,",",").split(",")
        for hashtag in c_hashtags:                      
            if hashtag != '':
                if hashtag in hashtags:
                    hashtags[hashtag][is_retweet] = hashtags[hashtag][is_retweet] + 1
                else:
                    retweet_status = [0,0,0]
                    retweet_status[is_retweet] = 1
                    retweet_status[not is_retweet] = 0
                    retweet_status[2] = [0,0]
                    retweet_status[2][0] = []
                    retweet_status[2][1] = []
                    hashtags[hashtag] = retweet_status
                hashtags[hashtag][2][is_retweet].append(tweet["user_screen_name"])

def date_metrics(tweet, date_set, is_retweet):
    tweet_created_date = datetime.fromisoformat(tweet["created_at"]).strftime("%m/%d/%Y")
    if not tweet_created_date in date_set:
        retweet_status = [0,0,0]
        retweet_status[is_retweet] = 1
        retweet_status[not is_retweet] = 0
        date_set[tweet_created_date] = retweet_status
        retweet_status[2] = [0,0]
        retweet_status[2][0] = []
        retweet_status[2][1] = []
    else:
        date_set[tweet_created_date][is_retweet] += 1
    date_set[tweet_created_date][2][is_retweet].append(tweet["user_screen_name"])

def time_metrics(tweet, time_set, is_retweet):
    tweet_created_time = datetime.fromisoformat(tweet["created_at"]).strftime("%H") #change to %I %p for AM/PM

    if not tweet_created_time in time_set:
        retweet_status = [0,0,0]
        retweet_status[is_retweet] = 1
        retweet_status[not is_retweet] = 0
        time_set[tweet_created_time] = retweet_status
        retweet_status[2] = [0,0]
        retweet_status[2][0] = []
        retweet_status[2][1] = []
    else:
        time_set[tweet_created_time][is_retweet] += 1
    time_set[tweet_created_time][2][is_retweet].append(tweet["user_screen_name"])

def user_metrics(tweet, user_set, is_retweet, keep_rt):
    if ("retweeted_status" in tweet) == False or keep_rt == "True":
        user = {}
        if tweet["user_screen_name"] not in user_set:
            user["screen_name"] = tweet["user_screen_name"]
            user["description"] = tweet["user_description"]
            user["following_count"] = tweet["user_following_count"]
            user["followers_count"] = tweet["user_followers_count"]
            user["total_tweets"] = tweet["user_total_tweets"]
            user["created_at"] = tweet["user_created_at"]
            user["total_in_data_set"] = [0,0]
            user["total_in_data_set"][is_retweet] = 1
            ## Note, if full retweet count is preferred, replace "retweet_count_dataset" with "retweet_count_listed"
            if "retweet_count_dataset" in tweet:
                user["total_times_retweeted_set"] = int(tweet["retweet_count_dataset"])
            user_set[tweet["user_screen_name"]] = user

        else:           
            user_set[tweet["user_screen_name"]]["total_in_data_set"][is_retweet] += 1
            if "retweet_count_dataset" in tweet:
                user_set[tweet["user_screen_name"]]["total_times_retweeted_set"] += int(tweet["retweet_count_dataset"])
            if tweet["user_following_count"] > user_set[tweet["user_screen_name"]]["following_count"]:
                user_set[tweet["user_screen_name"]]["following_count"] 
            if tweet["user_followers_count"] > user_set[tweet["user_screen_name"]]["followers_count"]:
                user_set[tweet["user_screen_name"]]["followers_count"] 
            if tweet["user_total_tweets"] > user_set[tweet["user_screen_name"]]["total_tweets"]:
                user_set[tweet["user_screen_name"]]["total_tweets"]

        #if tweet["user_screen_name"] not in unique_users[is_retweet]:
        #   unique_users[is_retweet].append(tweet["user_screen_name"])

def save_hashtag_metrics(hashtags, file_name):
    with open('./results/metrics_%s/%s_hashtags.csv' % (file_name, file_name), 
        mode='w', encoding="utf-8",newline='') as file_hashtags:
        writer_hashtags = csv.writer(file_hashtags)
        writer_hashtags.writerow(["hashtag","total_normal", "total_retweet", 
            "total","unique_tweeters", "re_unique_tweeters", "re_unique_tweeters_filtered", "total"])

        for hashtag, value in hashtags.items():
            normal = set(value[2][0])
            retweet = set(value[2][1])
            unique = [x for x in retweet if x not in normal]
            writer_hashtags.writerow([hashtag, value[0], value[1], value[0] + value[1], str(len(normal)), 
                str(len(retweet)), str(len(unique)), str(len(normal) + len(unique))])
    print("Finished. Saved to ./results/metrics_%s/%s_hashtags.csv" % (file_name, file_name))

def save_date_metrics(date_set, file_name):
    with open('./results/metrics_%s/%s_date.csv' % (file_name, file_name), 
        mode='w', encoding="utf-8",newline='') as file_date:
        writer_date = csv.writer(file_date)
        writer_date.writerow(["date","total_normal", "total_retweet", "total_tweets","unique_normal_tweeters",
            "unique_retweeters_exist", "unique_retweeters_filtered", "unique_retweeters_total", 
            "total_tweeters"])

        for date, value in date_set.items():
            #unique_users[is_retweet]

            normal = set(value[2][0])
            retweet = set(value[2][1])
            unique = [x for x in retweet if x not in normal]
            writer_date.writerow([date, value[0], value[1], value[0] + value[1], 
                str(len(normal)), str(len(retweet) - len(unique)), str(len(unique)), str(len(retweet)), 
                str(len(normal) + len(unique))])

    print("Finished. Saved to ./results/metrics_%s/%s_date.csv" % (file_name, file_name))

def save_time_metrics(time_set, file_name):
    with open('./results/metrics_%s/%s_time.csv' % (file_name, file_name), 
        mode='w', encoding="utf-8",newline='') as file_time:
        writer_time = csv.writer(file_time)
        writer_time.writerow(["time","total_normal", "total_retweet", "total_tweets","unique_tweeters", 
            "re_unique_tweeters", "re_unique_tweeters_filtered", "total_tweeters"])

        for hour, value in time_set.items():
            normal = set(value[2][0])
            retweet = set(value[2][1])
            unique = [x for x in retweet if x not in normal]
            writer_time.writerow([hour, value[0], value[1], value[0] + value[1], 
                str(len(normal)), str(len(retweet)), str(len(unique)), str(len(normal) + len(retweet))])
    print("Finished. Saved to ./results/metrics_%s/%s_time.csv" % (file_name, file_name))

def save_user_metrics(user_set, file_name):
    with open('./results/metrics_%s/%s_users.csv' % (file_name, file_name), 
        mode='w', encoding="utf-8",newline='') as file_users:
        writer_users = csv.writer(file_users)


        if "total_times_retweeted_set" in list(user_set.values())[0]:
            writer_users.writerow(["screen_name", "total_posted_normal","total_posted_retweets","total_posted", 
                "user_description","user_following_count", "user_followers_count", "user_total_tweets", 
                "total_times_retweeted_set","user_created_at"])
            with open('./results/metrics_%s/%s_old_retweets.csv' % (file_name, file_name), 
                mode='r', encoding="utf-8") as old_retweets:
                csv_reader = csv.DictReader(old_retweets)
                for tweet in csv_reader:
                    if tweet["user_screen_name"] in user_set:
                        user_set[tweet["user_screen_name"]]["total_times_retweeted_set"] += int(tweet["retweet_count"])
        else:
            writer_users.writerow(["screen_name", "total_posted_normal","total_posted_retweets","total_posted", 
                "user_description","user_following_count", "user_followers_count", "user_total_tweets","user_created_at"])

        for a in user_set:
            user = user_set[a]
            if "total_times_retweeted_set" not in user:
                writer_users.writerow([user["screen_name"],user["total_in_data_set"][0],user["total_in_data_set"][1], 
                    (user["total_in_data_set"][0] + user["total_in_data_set"][1]), user["description"],
                    user["following_count"],user["followers_count"],user["total_tweets"],user["created_at"]])
            else:
                writer_users.writerow([user["screen_name"],user["total_in_data_set"][0],user["total_in_data_set"][1], 
                    (user["total_in_data_set"][0] + user["total_in_data_set"][1]), user["description"],
                    user["following_count"],user["followers_count"],user["total_tweets"],
                    user["total_times_retweeted_set"],user["created_at"]])

    print("Finished. Saved to ./results/metrics_%s/%s_users.csv" % (file_name, file_name))

if __name__ == '__main__':
    #pass in the target filename without "json" as argument in command prompt.
    parse_tweets(sys.argv)
```

### Spreadsheet Graphs

This section contains some graphs we might create upon importing the metric CSV files, generated with the script above, into a spreadsheet application.[^5]

!!! Note
    The content of the Tweets and the description of the users remain as-is, including newlines, URLs, hashtags and emojis. Older versions of MS Excel, in particular, might have trouble correctly importing CSVs because of that. If using an older version of Excel is a must and importing the CSV results in faulty data, the best option would be to use OpenRefine to export the CSV as a valid Excel file (make sure that UTF-8 is selected for character encoding and that the radio button indicating columns are separated by commas is checked). Moreover, ensure that the Tweet ID columns are set to text rather than int64, in order to prevent Excel from cutting of digits in its conversion.

#### Date & time frequency

The time-series graphs below represent changes over time and were made after importing the date frequency and time frequency CSV files in Excel 2019. Both **Figure 2** (a line chart measuring all occurrences over time) and **figure 3** (a stacked area chart showcasing the total amount of tweets of a daily timespan split in original tweets and retweets) reveal a strong peak in retweets on the 13 <sup>th</sup> of May. This spike obscures the visual effectiveness of the rest our graphs. A solution is thus to split the count of Tweets and retweets over two different horizontal axes (**figure 4**), or use a 100% stacked bar graph to view the relation between the total tweets and retweets (**figure 5**).

!!! Note
    Data for the first and last day in our set (respectively 04/30/2020 and 05/29/2020) contains data only up to a certain point of that day and has thus been left out of the following graphs.

<div class="slider" style="margin: auto; text-align: center;">
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/day_graph_analysis_total_users_axis.png" style="margin: auto; max-width: 95% !important;margin-bottom: 10px;width: 883px; height: auto; max-width: 100%;"/><span><strong>Figure 1:</strong> Amount of daily active Twitter users (re)tweeting #旦那ストレス</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/day_graph_analysis_total.png" style="margin: auto; max-width: 95% !important;margin-bottom: 10px;width: 884px; height: auto; max-width: 100%;"/><span><strong>Figure 2:</strong> Total combined tweets containing #旦那ストレス</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/day_graph_analysis_total_split.png" style="margin: auto; max-width: 95%!important;margin-bottom: 10px;width: 885px; height: auto; max-width: 100%;"/><span><strong>Figure 3:</strong> Total tweets &amp; retweets Containing #旦那ストレス</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/day_graph_analysis_total_split_axis.png" style="margin: auto; max-width: 95% !important;margin-bottom: 10px;width: 883px; height: auto; max-width: 100%;"/><span><strong>Figure 4:</strong> Total tweets &amp; retweets Containing #旦那ストレス</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/day_graph_analysis_stacked_100.png" style="margin: auto; max-width: 95% !important;margin-bottom: 10px;width: 883px; height: auto; max-width: 100%;"/><span><strong>Figure 5:</strong> Tweet/retweet division of combined total containing #旦那ストレス per day</span></div>
</div>

In regards to the question of a public sphere and interconnected discourse forming around this hashtag, we might be interested in knowing how many of those retweeters are actually actively writing similar Tweets themselves (and thus engaging with others connected by the hashtag) as well. In that case, we could use a mixed graph with stacked bars for visualizing retweeters in two groups (the right axis) and a line measure for the count original tweeters on the left (**figure 1**). One immediate takeaway is that only a very small number of retweeters have actually tweeted similar content themselves, suggesting that there might not be much engagement among active tweeters (and thus unlikely to develop into a public or community developed through this hashtag).[^6] From a glance it is furthermore clear that the amount of active tweeters practically doubled during the first couple of days of the extended holiday (golden week) in Japan, with gradual ups and down in activity since. The same goes for retweet activity, with a clear exception present around the period of May 13 (more on that below).

Using the spreadsheet table overview of our full CSV data as well as spreadsheet pivot functionality helps bring clarity to this trend deviation. The deviation concerns several tweets of one particularly active user with thousands of followers, but with a nevertheless low amount of posts actually being retweeted or replied to. Although the most prominent Tweet (which accuses the husband of intending to hoard the cash handouts each household member would receive in light of the Corona virus) was made prior to the first Tweet in our set, it didn’t get picked up on until late May 12 (with an increase in pace after being retweeted by a prominent Twitter influencer with over 80.000 followers). Subsequent retweets more or less lasted until the early night of May 14.

Moreover, the follower count of that Twitter user increased fifteen fold between the first and last raw JSON data files we obtained including that user’s Tweets. It should also be noted that although having frequently used both the husband stress and related hashtag *#husbanddeathnote* (*dan’na desunōto*, #{{旦那(だんな)}}デスノート) before, the user has since such an increase in attention refrained from using them at all.

The renewed peak in (original) Tweets and (unique) tweeters shortly after the initial retweet peak of May 13 suggests a brief reinvigorating effect after a period of stagnation. Nevertheless, it is recommended to conduct a closer content analysis (using quantitative and qualitative methods) of the Tweet content to deduce whether those Tweets are indeed signaling an increase in users utilizing the medium to discuss dissatisfaction in regards to their spouses, or are instead meta-conversations on the existence of those hashtags (as is so often the case with viral hashtags).

<div class="slider" style="margin: auto; text-align: center;">
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/time_graph_analysis_tweets.png" style="margin: auto; max-width: 95% !important;margin-bottom: 10px;width: 882px; height: auto; max-width: 100%;"/><span><strong>Figure 6:</strong> Total hourly (re)tweets containing #旦那ストレス</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/time_graph_analysis_tweeters.png" style="margin: auto; max-width: 95%!important;margin-bottom: 10px;width: 880px; height: auto; max-width: 100%;"/><span><strong>Figure 7:</strong> Total hourly (re)tweeters engaging with #旦那ストレス</span></div>
</div>

Finally, while spreading the tweeting (**figure 6**) or tweeter (**figure 7**) rate on an hourly basis might have its benefits for specific use cases, it does not yield particularly surprising results when applied to our dataset. While it is not much of a stretch to assume that the vast majority of tweets in our dataset are posted by mothers[^7] with a particular rigid daily schedule, it is reasonable to believe that the peaks in activity in the late evening, as well as right before and after lunch are common among unrelated Twitter users as well.

#### Hashtag frequency

These next graphs are based on the top ten hashtags sorted by frequency of appearance (excluding, of course, the hashtag we have used as the query to collect our data). With the exception of **figure 10** (which counts based on the total amount of unique Twitter users rather than total tweets) as demonstration of marginally different results, all are sorted by total combined (re)tweets. **Figure 8** is an English translation of **Figure 9**, and **Figure 11** juxtaposes the amount of tweeters and retweeters with the total amount of tweets and retweets per hashtag. It should be noted that these statistics are based on the individual occurrence of each hashtag and thus does not keep in mind the overlap of multiple such hashtags in one particular tweet (some tweets consisted of nothing more than several hashtags and an annexed image).

The majority of the hashtags are idle complaints targeting the spouse with various levels of playfulness. The highest ranking hashtag, *#husbanddeathnote* (*dan’na desunōto*, #{{旦那(だんな)}}デスノート), for example, refers to a popular 2000’s manga, anime and live action series (Death Note) and in particular to its eponymous notebook, which results in the death of every person whose name is penned down. The concept has since been juxtaposed with various demographics as an expression of anger or frustration. A google search suggests that this hashtag predates our targeted hashtag #{{旦那(だんな)}}ストレス, with media attention dating all the way back to around 2017. Furthermore, the top result links to an anonymous bulletin board **danna-shine.com** (a transliteration of #{{旦那死(だんなし)}}ね, *husband, die!*). A brief visit to that website reveals that it is, perhaps unsurprisingly, intended for posting anonymous complaints,[^8] claims to have over 180.000 monthly users and makes a visual reference to Twitter and that specific death note hashtag in its banner.[^9]

<div class="slider" style="margin: auto; text-align: center;">
<div><img  class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/hashtags_freq_eng.png" style="margin: auto; max-width: 95%!important; margin-bottom: 10px;width: 1005px; height: auto; max-width: 100%;"/><span><strong>Figure 8:</strong> Top 10 used hashtags sorted by combined total (re)tweets containing #旦那ストレス (English translation)</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/hashtags_freq_total.png" style="margin: auto; max-width: 95%!important;margin-bottom: 10px;width: 1012px; height: auto; max-width: 100%;"/><span><strong>Figure 9:</strong> Top 10 used hashtags sorted by combined total (re)tweets containing #旦那ストレス</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/hashtags_freq_tweets.png" style="margin: auto; max-width: 95% !important;margin-bottom: 10px;width: 1011px; height: auto; max-width: 100%;"/><span><strong>Figure 10:</strong> Top 10 used hashtags sorted by original tweets containing #旦那ストレス</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/hashtags_freq_tweet_tweeters.png" style="margin: auto; max-width: 95% !important;margin-bottom: 10px;width: 874px; height: auto; max-width: 100%;"/><span><strong>Figure 11:</strong> Top 10 used hashtags original tweets containing #旦那ストレス</span></div>
</div>

Other noteworthy hashtags are “*#coronadivorce*” (*Korona rikon*, #コロナ{{離婚(りこん)}}), “*#emotionallyabusivehusband*” (*morahara otto*, モラハラ{{夫(おっと)}}) and “#mother-in-lawstress” (*gibo sutoresu*, #{{義母(ぎぼ)}}ストレス). The first, of course, refers to the greater discourse in which we situate this study, although actual references to the threat of divorce appear to be relatively low in our sample. The second refers to *morahara* (モラハラ, an abbreviation of the pseudo-Anglican Japanese term moral harassment), indicating a sociological concept of emotional and psychological abusive behavior through means of gas-lighting and humiliation. The last hashtag, “*#mother-in-law stress*”, then, is exceptional in that it is not just the only hashtag in our top ten not explicitly connected to the spouse, it is also the only one that has a disproportionate amount of retweets and retweeters.[^10]

#### User Data

Based on the generated user data CSV, we might use pivot functionality to build graphs visualizing the relation between things such as date of user registration and tweets.

**Figure 13**, for example, visualizes users, with at least one actively tweeted message containing #{{旦那(だんな)}}ストレス, in a *pie of pie* chart on a yearly basis, demonstrating that 41% of such users were created in 2020. **Figure 15** further divides the period of 2018 to May 2020 by month, illustrating again that there is indeed a fairly consistent monthly increase since late 2019 in registered accounts utilizing Twitter to display marital problems.

Based on those graphs, we can thus conclude that the majority of the Twitter users actively posting tweets containing this hashtag registered their account on Twitter extremely recently, most likely as a second, private account (often referred to as ura’aka, #{{裏垢(うらあか)}}) created specifically for this purpose. In comparison then, **figure 14** suggest that there is less of a psychological barrier for Twitter users to retweet such content on existing accounts; a retweet might insinuate sympathy towards the original tweeter and/or personal engagement with the topic at hand, but enough distance remains to not be used negatively towards those retweeters. The fact that the green line (representing the total amount of Twitter users in our dataset) is almost consistent with the combine value of the stacked bars (total tweet & retweet posters) further demonstrates that there is a very low tendency for users to both actively tweet content with this hashtag and simultaneously retweet the content of others.

Taking a different angle to demonstrate the same thing, **Figure 12** displays the amount of (re)tweets posted on a yearly basis both separate and as running total. Again, this graph suggest that there is not anything particularly outstanding concerning the registration date for users retweeting such content, while simultaneously showing that the most actively tweeting accounts have all been created very recently.

<div class="slider" style="margin: auto; text-align: center;">
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/users_year_tweets.png" style="margin: auto; max-width: 95%!important; margin-bottom: 10px;width: 952px; height: auto; max-width: 100%;"/><span><strong>Figure 12:</strong> (Cumulative) totals of (re)tweets containing #旦那ストレス spread over date of account creation by year</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/users_year_creation.png" style="margin: auto; max-width: 95%!important; margin-bottom: 10px;width: 723px; height: auto; max-width: 100%;"/><span><strong>Figure 13:</strong> Year of creation of Twitter users in our dataset having posted more than one post containing #旦那ストレス</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/users_year_combined.png" style="margin: auto; max-width: 95%!important; margin-bottom: 10px;width: 722px; height: auto; max-width: 100%;"/><span><strong>Figure 14:</strong> Twitter users engaging with #旦那ストレス, sorted by account year of creation</span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/users_year_creation_months.png" style="margin: auto; max-width: 95%!important; margin-bottom: 10px;width: 881px; height: auto; max-width: 100%;"/><span><strong>Figure 15:</strong> Registered accounts with active #旦那ストレス usage per month (2018 - 2020) </span></div>
<div><img class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/users_sorted_original.png" style="margin: auto; max-width: 95%!important; margin-bottom: 10px;width: 883px; height: auto; max-width: 100%;"/><span><strong>Figure 16:</strong> Twitter users sorted by amount of original tweets containing #旦那ストレス </span></div>
<div><img  class="fborder" alt="Twitter" src="https://steviepoppe.net/images/twitter/users_sorted.png" style="margin: auto; max-width: 95%!important; margin-bottom: 10px;width: 886px; height: auto; max-width: 100%;"/><span><strong>Figure 16:</strong> Twitter users posting original tweets containing #旦那ストレス, sorted by followers and following count </span></div>
</div>

Finally, the two ugliest graph on this blog (**figure 16** and **figure 17**) reveal more about the level of engagement of Twitter users actively posting themselves, as well as the possible reach and/or attempts to interconnect with others based on the amount of followers and ‘friends’ (i.e. their following count). About half of those users have tweeted content with the #{{旦那(だんな)}}ストレス hashtag on a repeated basis within the timespan of our dataset and are thus likely to have a particular strong investment in the topic. It is not unlikely that there are those, among the other half of those users, who have no personal investment but rather feel some curiosity towards the actual hashtag and the discourse it itself represents.

One such Twitter account, for example, has over 300.000 followers. By sorting the users table by followers, this was revealed to be the public account of Shinya Arino, a famous Japanese comedian who might have possibly come into contact after a particular tweet mentioned earlier went relatively viral on the 13th of May. By cross-referencing our full CSV table with this name, the content and date of creation of Shinya’s tweet was easily revealed: 「このハッシュタグは　#{{勉強(べんきょう)}}になる #{{旦那(だんな)}}ストレス」 (Kono hasshu tagu wa benkyō ni naru, Eng. “This hashtag is illuminating”), posted on 18 May, 2020. It is difficult to gouge what impact this ‘endorsement’ by a public media figure has or if it was perhaps intended mockingly, but at the very least **figure 4** reveals a stark drop rather than rise in accounts tweeting such messages right after his tweet.

---

# Automation: Bringing Everything Together

In a research project that requires the collection of Twitter data over a long period of time, it is understandably a drag to manually update the preprocessed data (and its derisive metrics in CSV format) through various separate scripts run from the command line each time new data is to be collected. One method of simplifying those steps is to use a batch script[^11] that automatizes several or even all of the acts we have been doing manually. Upon saving and running the following script, for example, it will iterate through all the unprocessed JSON files with a filename matching the name of the batch file (e.g. **#旦那ストレス.bat** → all JSON files containing **#旦那ストレス**) and run them through **python_parse_tweet_ver2.py** with predefined options such as setting the timezone to “Asia/Tokyo” (keeping the total calculation and check for doubles until the final JSON has been processed). Finally, this batch script will run the preprocessed CSV file through the parsing metric script we have outlined in this article.

```bash
@echo off

:: Necessary for Unicode support
chcp 65001 >NUL

cd /d C:\python\

set safe_csv=%~n0
set time_zone=Asia/Tokyo
set include_retweets="True"
set add_totals="True"
set double_check="True"
set query=%~n0
set since_id="None"

:: Count total amount of files
for /f %%A in ('dir /A:-D /B .\results\*%query%*.json ^| find /v /c ""') do set total=%%A

:: Necessary to count in loop
setlocal enabledelayedexpansion
set count=0

for %%a in (results/*%query%*.json) do (
    :: Create CSV of all relevant query JSON
    echo "Pre-processing: %%a"
    set /a count += 1
    IF !count!==%total% (
            py python_parse_tweet_ver2.py %%~na %time_zone% %include_retweets% %safe_csv% %add_totals% %double_check%
    ) else (
    py python_parse_tweet_ver2.py %%~na %time_zone% %include_retweets% %safe_csv%
    )
)
endlocal

:: Create metrics CSV files
echo "Calculating metrics..."
py python_metrics.py %safe_csv%

PAUSE
```

This script could be further edited to begin by first datamining new JSON data with any of the API scripts provided earlier, potentially using the Windows Registry to keep track op the `since_id` variable. If desired, we might also schedule this script to run periodically using the Windows schedule manager (e.g. to run the Search API script and its preprocessing and parsing scripts on a weekly basis, or even on a daily basis if daily updated statistics on account information, such as follower and following count, is preferred).

If we are using spreadsheet software that maintains a connection with the CSV data sources for its tables and graphs, updating our graphs to reflect those changes is a matter of pressing a single update button (such as the Data → Refresh All button in MS Excel 2019).

---

# Legal and Ethical Caveats

Having glanced over both the above tutorial and the provided graphs or data, the reader might have (with one exception) noticed a lack of direct references to concrete Tweets or users. Japanese Tweet content has either been translated to English without supplying any identification, or visualized through calculated metrics. Moreover, this series does not provide access to the original JSON files or to the preprocessed CSV files. This is done deliberately both according to Twitter API’s terms of service (which prohibits sharing raw, unprocessed Tweet data) and, from an ethical standpoint, to protect the identity of its users (regardless of the public accessibility of those users’ Tweets and the levels of anonymity their accounts provide). One jarring exception this article made is the explicit reference to Shinya Arino, a public figure who is using Twitter with the explicit purpose of reaching a large public. Verbatim quoting his tweet, then, was done purposefully to illustrate the ethical line one must thread when revealing personal information of social media users.

Traditionally, informed consent, anonymity and confidentiality are crucial elements of research involving public opinion of private individuals. For over a decade, social media platforms has been providing (budding) researchers the opportunity to engage with an unprecedented amount of data representing public opinion, creating somewhat of a gray zone within academic research concerning the above elements. From a legal perspective, Twitter’s Privacy Policy does indeed inform its users that all public data could be used for the purpose of academic research. Yet, as Fiesler and Proferes (2018)[^12] rightly point out, social media users are often not aware of the extent their content on those platforms can be used. Instead, Fiesler and Proferes highlight several prominent examples of scandals or public outrage in regards to publications that have used such data, even if they did not break any legal boundaries.

One could argue that this ethical boundary is highly individual. Data on platforms such as Twitter is explicitly open, more so when containing hashtags whose prime function is to reach a wider audience.[^13] Moreover, websites such as Buzzfeed have financially thrived on using tweets from private individuals for comical effect. In an era of meme-dominated pop culture, it is furthermore extremely common to find memefied tweets spreading across other media platforms.

Especially in light of the recent Cambridge Analytica scandal, however, utter care must be taken that no risks befalls any individual whose social media content is part of one’s research data; especially when dealing with sensitive topics such as the one highlighted in this article. Generating quantitative data that does not pinpoint individual content (such as the statistics provided in this article, and text analytics such as frequency tables, sentiment analysis, etc) is but one specific part of social media-based research, and often goes hand in hand with qualitative readings of certain content. What if I published a paper on this topic that would later be cited by a major Japanese news outlet? If I had referenced a particular tweet by a user who had afterwards revealed personal information, could it not potentially endanger that Twitter user? This is of course highly unlikely, but nevertheless not impossible and something that should be kept in mind when taking a research angle dealing with such data.

Although Woodfield (2017, ch.4)[^14] refers to a research project that took a similar stance as I did concerning the masking of individual user names and paraphrasing rather than quoting tweet content, Woodfield has also referred to another research project in which researchers retrospectively searched informed content of each Twitter account whose tweet content they would individually use in their publications. This might seem excessive, and on a purely legal basis not even required, but even in the case of a graduate thesis rather than a PhD thesis or academic publication, it is at the very least not unwise to contact the board of ethics of one’s university for clarity on how to best deal with data obtained from social media from an ethical point of view.

---

# Wait! There is more!

Some of the graph examples and analyses in this article might appear overly excessive, especially when keeping in mind the limited scope of the highly specific hashtag analyzed.[^15] Nevertheless, it is my hope that those graphs served some purpose in illustrating how social network analysis and the methods outlined in this article might fit in research topics covering contemporary issues and public opinion expressed online.

Throughout the next entries in our blog series, we will dive further into actual textual analysis of Japanese corpora. In the third blog, we will look into the Japanese computational linguistics tool KH Coder, the morphological parser MeCab and its extensions, as well as the various options they offer us in our quantitative text analysis. The fourth blog will expand on the script provided in this article, including options for animating changes over an arbitrary timespan.

* [A <del>Quick</del> Guide to Data-mining & (Textual) Analysis of (Japanese) Twitter Part 1: Twitter Data Collection](https://steviepoppe.net/blog/2020/04/a-quick-guide-to-data-mining-textual-analysis-of-japanese-twitter/)
* [A <del>Quick</del> Guide to Data-mining & (Textual) Analysis of (Japanese) Twitter Part 3: Natural Language Processing With MeCab, Neologd and KH Coder](https://steviepoppe.net/blog/2020/06/a-quick-guide-to-data-mining-textual-analysis-of-japanese-twitter-part-3/)
* [A <del>Quick</del> Guide to Data-mining & (Textual) Analysis of (Japanese) Twitter Part 4: Natural Language Processing With MeCab, Neologd and NLTK](https://steviepoppe.net/blog/2020/07/a-quick-guide-to-data-mining-textual-analysis-of-japanese-twitter-part-4/)
* [A <del>Quick</del> Guide to Data-mining & (Textual) Analysis of (Japanese) Twitter Part 5: Advanced Metrics & Graphs](#)

*On a final note, it is my aim to write tutorials like these in such a way that they provide enough detail and (technical) information on the applied methodology to be useful in extended contexts, while still being accessible to less IT-savvy students. If anything is unclear, however, please do not hesitate to leave questions in the comment section below. <i class="icon-hand-down"></i>*

[^footnote]: Still image from the 2012 Japanese animated film Wolf Children by Mamoru Hosoda, used under a Fair Use doctrine.

[^1]: The Coordinated Universal Time (UTC) time standard; a universal standard [similar](https://www.timeanddate.com/time/gmt-utc-time.html) to the Greenwich Mean Time (GMT) timezone.
[^2]: Although the original JSON tweet objects contain a `retweet_count` variable, this contains all the retweets of that post from its conception up to the point we first acquired it in our dataset. This is not sufficient for long term data mining projects. Unfortunately it’s quite taxing to calculate replies the same way, and the Twitter `reply_count` variable is only available to Premium and Enterprise Twitter API services.
[^3]: It’s important to check on tweet ID doubles rather than on unique rows because secondary data such as follower and following count of the user might have changed by the time we have obtained new data with some duplications. In other words, even if the Tweet itself is a duplication, the row in our CSV file wouldn’t be counted as such.
[^4]: While functional and rigidly tested through various use-cases, this script is far from optimized and not very *pythonic*. I will rewrite this in due time, using in particular the python package **pandas**.
[^5]: It should be noted that some of the data we calculate by means of python could fairly easily have been derived from the base, preprocessed CSV file using pivot tables. About half of the data couldn’t, however, and centralizing everything in one script was a deliberate choice.
[^6]: Another option to gouge this is by viewing overlap of followers and followings of the most active users (network analysis) over a certain timespan, which is what we will be doing in a next blog entry.
[^7]: A glance over the description of all tweeters seems to suggest so (with language and emojis indicating one’s social identity as a mother or raising children), and could be further confirmed by textual analysis.
[^8]: Or to be exact, death wishes. 💀 The slogan furthermore refers to the corona virus, demanding the spouse to get infected as fast as possible.
[^9]: Indicating the limited nature of analyzing only one particular social media platform, since various platforms might perform together to form unique eco-systems on which discourse can thrive.
[^10]: The social problem of toxic relations with parents-in-law was furthermore the topic of the bestseller 2016 novel The House on the Slope (*Saka no Tochū no Ie*, 『坂の途中の家』) by Mitsuyo Kakuta, and its 2019 live action adaption. Both reinvigorated public interest in contemporary marital issues in Japan and concluded with the possible importance of social media towards empowering women stuck in toxic marriages.
[^11]: Short for computerized batch processing.
[^12]: **Fiesler, Casey, and Nicholas Proferes**. 2018. ‘“Participant” Perceptions of Twitter Research Ethics’. Social Media + Society 4 (1): 2056305118763366. <https://doi.org/10.1177/2056305118763366>.
[^13]: Even though its usage might often be for aesthetic or comic purposes.
[^14]: **Woodfield, Kandy**. 2017. The Ethics of Online Research. Emerald Group Publishing.
[^15]: Not withstanding the greater social relevance of the topic that encompasses this hashtag, either.


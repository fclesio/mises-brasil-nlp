#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import spacy
import string
import time
from bs4 import BeautifulSoup
import multiprocessing as mp
import numpy as np
import pandas as pd
from unicodedata import normalize

# PT-BR Corpora
nlp = spacy.load("pt_core_news_sm")

# Define default stopwords list
stoplist = spacy.lang.pt.stop_words.STOP_WORDS

# Define default punctuation list
punctuations = string.punctuation


def get_page_to_df(page_url: str):
    """
    Fetch data from the URL and stores in a dataframe

    Args:
        page_url (str): String that had the article URL

    Return:
        df_essay_complete (Pandas DF): Dataframe with the
        article text and information about the authors

    """
    res = requests.get(page_url)

    df_essay_complete = pd.DataFrame(
        columns=["title", "text", "author", "dow", "date", "url"]
    )

    if str(res) != "<Response [500]>":
        html_page = res.content
        soup = BeautifulSoup(html_page, "html.parser")

        for a in soup.find_all("a"):
            del a["href"]

        essay = []
        text_full = []

        get_essay_entire_text = soup.find(class_="text-justify mis-text")
        get_essay_paragraph_text = get_essay_entire_text.find_all("p")

        try:
            for paragraph_text in get_essay_paragraph_text:
                text = paragraph_text.contents[0]
                text = str(text)

                if text[:4] != "<img":
                    essay.append(text)
                    text_full = ", ".join([str(x) for x in essay])

            text_full = str(text_full)
            text_full = text_full.replace("<b>", "")
            text_full = text_full.replace("</b>", "")
            text_full = text_full.replace("<p>", "")
            text_full = text_full.replace("</p>", "")
            text_full = text_full.replace("<a>", "")
            text_full = text_full.replace("</a>", "")
            text_full = text_full.replace("<br/>", "")

            get_essay_name = soup.find(class_="mis-title1 mis-fg-almostblack")
            get_essay_name = str(get_essay_name.contents[0])

            get_essay_author = soup.find(class_="no-link mis-fg-alpha mis-author-name")
            get_essay_author = get_essay_author.contents[0]

            get_essay_date = soup.find(
                class_="mis-fg-lightgray mis-text mis-article-date"
            )
            get_essay_date = str(get_essay_date.contents[0])

            get_essay_section_name = soup.find(class_="mis-fg-alpha mis-section-name")
            for section_name in get_essay_section_name.find(class_="no-link"):
                get_essay_section_name = section_name

            essay_strip = []

            essay_strip.append(
                (
                    str(get_essay_name),
                    str(text_full),
                    str(get_essay_author),
                    str(get_essay_date.split(",")[0]),
                    str(get_essay_date.split(",")[1]),
                    str(page_url),
                )
            )

            df_essay_complete = pd.DataFrame(essay_strip)
            df_essay_complete.columns = [
                "title",
                "text",
                "author",
                "dow",
                "date",
                "url",
            ]
        except:
            for paragraph_text in get_essay_paragraph_text:
                text = paragraph_text
                text = str(text)

                if text[:4] != "<img":
                    essay.append(text)
                    text_full = ", ".join([str(x) for x in essay])

            text_full = str(text_full)
            text_full = text_full.replace('<[^<]+?>', '')
            text_full = text_full.replace("<b>", "")
            text_full = text_full.replace("</b>", "")
            text_full = text_full.replace("<p>", "")
            text_full = text_full.replace("</p>", "")
            text_full = text_full.replace("<a>", "")
            text_full = text_full.replace("</a>", "")
            text_full = text_full.replace("<br/>", "")

            get_essay_name = soup.find(class_="mis-title1 mis-fg-almostblack")
            get_essay_name = str(get_essay_name.contents[0])

            get_essay_author = soup.find(class_="no-link mis-fg-alpha mis-author-name")
            get_essay_author = get_essay_author.contents[0]

            get_essay_date = soup.find(
                class_="mis-fg-lightgray mis-text mis-article-date"
            )
            get_essay_date = str(get_essay_date.contents[0])

            get_essay_section_name = soup.find(class_="mis-fg-alpha mis-section-name")
            for section_name in get_essay_section_name.find(class_="no-link"):
                get_essay_section_name = section_name

            essay_strip = []

            essay_strip.append(
                (
                    str(get_essay_name),
                    str(text_full),
                    str(get_essay_author),
                    str(get_essay_date.split(",")[0]),
                    str(get_essay_date.split(",")[1]),
                    str(page_url),
                )
            )

            df_essay_complete = pd.DataFrame(essay_strip)
            df_essay_complete.columns = [
                "title",
                "text",
                "author",
                "dow",
                "date",
                "url",
            ]

    return df_essay_complete


# Fetch all URLs in a sequential way and get the articles
all_url = []

for i in range(1, 6000):
    page_url = f"https://mises.org.br/Article.aspx?id={i}"
    all_url.append(page_url)

# DF object that will store the data
df_extracted_essays = pd.DataFrame()


def main(df):
    """
    Main function with Multiprocessing to fetch all data

    Args:
        df (Pandas Dataframe): Dataframe that will receive
        the data inside the multiprocessing wrapper

    Return:
        df (Pandas Dataframe): Dataframe with the
        article text

    """
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(get_page_to_df, all_url)
    df = df.append(result)

    return df


# Time tracking
start_time = time.time()

# Call the main wrapper with multiprocessing
df_extracted_essays = main(df_extracted_essays)

elapsed_time = time.time() - start_time
fetching_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
print(f"Fetching Time: {fetching_time}")
print(f"Articles fetched: {df_extracted_essays.shape[ 0 ]}")

# Data Preprocessing
df_extracted_essays["title"] = [
    x.replace("\r\n", " ") for x in df_extracted_essays["title"]
]
df_extracted_essays["text"] = [
    x.replace("\r\n", " ") for x in df_extracted_essays["text"]
]
df_extracted_essays["text"] = [
    x.replace("<i>", "") for x in df_extracted_essays["text"]
]
df_extracted_essays["text"] = [
    x.replace("</i>", "") for x in df_extracted_essays["text"]
]
df_extracted_essays["text"] = [
    x.replace("\xa0", "") for x in df_extracted_essays["text"]
]

# Generate the date columns for parsing
df_extracted_essays["date_transform"] = (
    df_extracted_essays["date"].str.split(" ").values
)

# Strip columns
df_dates = pd.DataFrame(df_extracted_essays["date_transform"].values.tolist())
df_dates.columns = ["spare", "day", "month", "year"]
del df_dates["spare"]

# Parse days, months and years
conditions = [
    (df_dates["month"] == "jan"),
    (df_dates["month"] == "fev"),
    (df_dates["month"] == "mar"),
    (df_dates["month"] == "jul"),
    (df_dates["month"] == "abr"),
    (df_dates["month"] == "0aio"),
    (df_dates["month"] == "set"),
    (df_dates["month"] == "jun"),
    (df_dates["month"] == "out"),
    (df_dates["month"] == "nov"),
    (df_dates["month"] == "ago"),
    (df_dates["month"] == "dez"),
]

choices = [1, 2, 3, 7, 4, 5, 9, 6, 10, 11, 8, 12]

df_dates["mes"] = np.select(conditions, choices, default="null")

df_dates["date"] = pd.to_datetime(
    df_dates["year"] + "-" + df_dates["mes"] + "-" + df_dates["day"]
)

df_dates["month"] = df_dates["mes"]
df_dates["date"] = pd.to_datetime(df_dates["date"])

# Remove unnecessary columns
del df_dates["day"]
del df_dates["year"]
del df_dates["month"]
del df_dates["mes"]
del df_extracted_essays["dow"]
del df_extracted_essays["date"]

# Concatenate the dates
df_extracted_essays.reset_index(drop=True, inplace=True)
df_dates.reset_index(drop=True, inplace=True)
df_extracted_essays = pd.concat([df_extracted_essays, df_dates], axis=1)

df_extracted_essays["full_text"] = (
    df_extracted_essays["title"].str.lower()
    + " "
    + df_extracted_essays["text"].str.lower()
)


def remove_img_tags(data):
    """Remove some trash strings in the text"""
    p = re.compile(r"<img.*?/>")
    return p.sub("", str(data))


df_extracted_essays["text_processed"] = df_extracted_essays["full_text"].apply(
    remove_img_tags
)

special_by_space = re.compile('[/(){}\[\]"\|@,;]')


def clean_text(text):
    """ Remove some HTML chars from the text"""
    text = str(text)
    text = text.lower()  # lowercase text
    text = text.replace('<p align="justify">', "")
    text = text.replace("<u>", "")
    text = text.replace("</u>", "")
    text = text.replace(" u ", "")
    text = text.replace("justify", "")
    text = text.replace("align", "")
    text = text.replace("N. do T.:", "")
    text = text.replace('<div itemprop="articleBody">', "")
    text = text.replace('<div class="plain" id="parent-fieldname-text">', "")
    text = text.replace('<p style="text-align: justify;">', "")
    text = text.replace("<br/>", "")
    text = text.replace("</div>", "")
    text = text.replace("\n", "")
    text = text.replace(" < p>", "")
    text = text.replace(".< p>", " ")
    text = text.replace(".", " ")
    text = text.replace('<div itemprop="articlebody">', "")
    text = text.replace("<", "")
    text = text.replace(">", "")
    text = text.replace("style=/", "")
    text = text.replace("br/", "")
    text = text.replace("div/", "")
    text = text.replace("div", "")
    text = text.replace("/p", "")
    text = text.replace("...", "")
    text = text.replace("text-align", "")
    text = special_by_space.sub(" ", text)
    text = " ".join(word for word in text.split() if word not in stoplist)
    return text


df_extracted_essays["text_processed"] = df_extracted_essays["text_processed"].apply(
    clean_text
)

df_extracted_essays["text_processed"] = df_extracted_essays[
    "text_processed"
].str.replace("[^\w\s]", "")

# Remove the least 1000 words
freq = pd.Series(
    " ".join(df_extracted_essays["text_processed"]).split()
).value_counts()[-1000:]

freq = list(freq.index)
df_extracted_essays["text_processed"] = df_extracted_essays["text_processed"].apply(
    lambda x: " ".join(x for x in x.split() if x not in freq)
)

# Remove top 200 words and remove the non necessary ones (was cherry picked)
freq = [
    "a",
    "o",
    "e",
    "há",
    "the",
    "name",
    "1",
    "of",
    "p",
    "2",
    "align",
    "and",
    "title",
    "3",
    "5",
    "to",
    "span",
    "4",
    "in",
    "r",
]

df_extracted_essays["text_processed"] = df_extracted_essays["text_processed"].apply(
    lambda x: " ".join(x for x in x.split() if x not in freq)
)

del df_extracted_essays["full_text"]


def remove_punctuation(text):
    """
     This function remove the replacement_patterns from input string.

     Parameters
     ----------
     text : String
         Input string to the function.

     Returns
     -------
     text : String
         Output string after replacement.
     """
    rem = string.punctuation
    pattern = r"[{}]".format(rem)
    text = re.sub(r"[-()\"#/@;:&<>{}`+=~|.!?,[\]©_*]", " ", text)
    text = text.replace(pattern, "")
    return text


df_extracted_essays["text_processed"] = df_extracted_essays["text_processed"].apply(
    remove_punctuation
)


del df_extracted_essays["title"]
del df_extracted_essays["text"]

# Special thanks for the user Humberto Diogenes from Python List (answer from Aug 11, 2008)
# Link: http://python.6.x6.nabble.com/O-jeito-mais-rapido-de-remover-acentos-de-uma-string-td2041508.html


def replace_ptbr_char_by_word(word):
    word = str(word)
    word = normalize("NFKD", word).encode("ASCII", "ignore").decode("ASCII")
    return word


def remove_pt_br_char_by_text(text):
    text = str(text)
    text = " ".join(
        replace_ptbr_char_by_word(word) for word in text.split() if word not in stoplist
    )
    return text


df_extracted_essays["text_processed"] = df_extracted_essays["text_processed"].apply(
    remove_pt_br_char_by_text
)

html_trash_list = [
    "000",
    "0000ff",
    "008000",
    "0cm",
    "0pt",
    "100",
    "10pt",
    "1pt",
    "36pt",
    "5pt",
    "75pt",
    "7pt",
    "arial",
    "blockquote",
    "border",
    "bordercolor",
    "borderstyle",
    "borderwidth",
    "c5cusers5cuser5cappdata5clocal5ctemp...",
    "cellpadding",
    "cellspacing",
    "center",
    "class",
    "color",
    "colorblack",
    "ff0000",
    "file",
    "font",
    "fontfamily",
    "fontsize",
    "fontstyle",
    "fontweight",
    "height",
    "height",
    "href",
    "lang",
    "link",
    "medium",
    "mozusetextcolor",
    "msobodytext",
    "msonormal",
    "msonormal",
    "none",
    "nowrap",
    "op",
    "padding",
    "parte1",
    "parte2",
    "parte3",
    "parte4",
    "parte5",
    "parte6",
    "rgb",
    "right",
    "roman",
    "strong",
    "strongdia",
    "strongop",
    "strongspan",
    "style",
    "sup",
    "supsup",
    "t",
    "table",
    "tbody",
    "tbodytrtd",
    "td",
    "tdblockquote",
    "textindent",
    "tr",
    "trilhoesop",
    "trtr",
    "verdana",
    "width",
    "windowtext",
    "xml",
    "xmlnamespace",
    "st1place",
    "st1city",
    "spanspan",
    "text",
    "tdblockquote",
]


df_extracted_essays["text_processed"] = df_extracted_essays["text_processed"].apply(
    lambda x: " ".join(x for x in x.split() if x not in html_trash_list)
)

# Save checkpoint and pre-process date
df_extracted_essays.to_csv("df_extracted_essays.csv", index=False)

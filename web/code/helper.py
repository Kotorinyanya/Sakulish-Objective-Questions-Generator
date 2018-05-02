import time
import html
from datetime import datetime as dt


def timestamp():
    """
    Get Unix timestamp in int type.
    :return: timestamp
    """
    return int(time.time())


def datetime(time_stamp):
    """
    Get date string with Unix timestamp.
    :param time_stamp:
    :return: date string
    """
    return dt.fromtimestamp(
        int(time_stamp)
    ).strftime('%Y-%m-%d %H:%M:%S')


def counter(start=1, step=1):
    """
    Return a counter, each access it will increase [step].
    :param start: start number
    :param step: increment each call
    :return:
    """
    def real_counter():
        nonlocal start
        now_count = start
        start += step
        return now_count
    return real_counter


def text_to_html(text):
    """
    Convert a text to html.
    :param text: a text
    :return: text in html format
    """
    paragraphs = html.escape(text).split("\n")
    paragraphs = map(lambda x: x.strip(), paragraphs)
    paragraphs = map(lambda x: "<p>" + x + "</p>", paragraphs)
    return "\n".join(paragraphs)


def paginate(this_page, page_count, url_prefix, show_page_count=5):
    """
    Get page links.
    :param this_page: current page
    :param page_count: number of all pages
    :param url_prefix: page link prefix
    :param show_page_count: maximum pages in the list
    :return: generated links
    """
    pages = {
        "current": this_page,
        "previous": url_prefix + str(this_page - 1) if this_page > 1 else None,
        "next": url_prefix + str(this_page + 1) if this_page < page_count else None,
        "links": list()
    }
    # Calculate start page & end page.
    start_page = this_page - show_page_count // 2
    if start_page < 1:
        start_page = 1
    end_page = start_page + show_page_count
    if end_page - 1 > page_count:
        end_page = page_count + 1
    if end_page - start_page < show_page_count and start_page > 1:
        if end_page - show_page_count > 0:
            start_page = end_page - show_page_count
        else:
            start_page = 1
    # Generate links.
    for i in range(start_page, end_page):
        pages["links"].append({"page": i, "link": url_prefix + str(i)})
    return pages

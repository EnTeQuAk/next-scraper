from collections import defaultdict

from lxml import html

HTML_VERSION_CHOICES = {
    "unknown": "Unknown",
    "html5": "HTML 5",
    "html4-strict": "HTML 4.01 Strict",
    "html4-transitional": "HTML 4.01 Transitional",
    "html4-frameset": "HTML 4.01 Frameset",
    "xhtml10-strict": "XHTML 1.0 Strict",
    "xhtml10-transitional": "XHTML 1.0 Transitional",
    "xhtml10-frameset": "XHTML 1.0 Frameset",
    "xhtml-11": "XHTML 1.1",
}

# Mapping of root_name, public id and system url
HTML_DOCTYPE_MAPPING = {
    "html5": ("html", None, None),
    "html4-strict": (
        "html",
        "-//W3C//DTD HTML 4.01//EN",
        "http://www.w3.org/TR/html4/strict.dtd",
    ),
    "html4-transitional": (
        "html",
        "-//W3C//DTD HTML 4.01 Transitional//EN",
        "http://www.w3.org/TR/html4/loose.dtd",
    ),
    "html4-frameset": (
        "html",
        "-//W3C//DTD HTML 4.01 Frameset//EN",
        "http://www.w3.org/TR/html4/frameset.dtd",
    ),
    "xhtml10-strict": (
        "html",
        "-//W3C//DTD XHTML 1.0 Strict//EN",
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd",
    ),
    "xhtml10-transitional": (
        "html",
        "-//W3C//DTD XHTML 1.0 Transitional//EN",
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd",
    ),
    "xhtml10-frameset": (
        "html",
        "-//W3C//DTD XHTML 1.0 Frameset//EN",
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd",
    ),
    "xhtml11": (
        "html",
        "-//W3C//DTD XHTML 1.1//EN",
        "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd",
    ),
}


REVERSE_DOCTYPE_MAPPING = {value: key for key, value in HTML_DOCTYPE_MAPPING.items()}


def get_html_version_from_tree(tree):
    """Get the doctype of a page.

    Per spec a doctype is required -
    https://html.spec.whatwg.org/multipage/syntax.html#the-doctype
    but some pages don't properly set it.

    LXML defaults to html4 transitional if none exists which should be fine.
    """
    info = tree.getroottree().docinfo
    return REVERSE_DOCTYPE_MAPPING.get(
        (info.root_name, info.public_id, info.system_url), "unknown"
    )


def _form_score(form):
    score = 0
    # In case of user/pass or user/pass/remember-me
    if len(form.inputs.keys()) in (2, 3):
        score += 10

    typecount = defaultdict(int)
    for x in form.inputs:
        type_ = x.type if isinstance(x, html.InputElement) else "other"
        typecount[type_] += 1

    if typecount["text"] > 1:
        score += 10
    if not typecount["text"]:
        score -= 10

    if typecount["password"] == 1:
        score += 10
    if not typecount["password"]:
        score -= 10

    if typecount["checkbox"] > 1:
        score -= 10
    if typecount["radio"]:
        score -= 10

    return score


def pick_possible_login_form(forms):
    """Return the form most likely to be a login form

    Shamelessly stolen from Scrapy.
    """
    sorted_forms = sorted(forms, key=_form_score, reverse=True)
    if sorted_forms:
        return sorted_forms[0]
    return None

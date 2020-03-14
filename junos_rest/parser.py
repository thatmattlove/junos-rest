"""Parsing functions for JunOS XML/HTTP responses."""

# Third Party Imports
import xmltodict
from boltons.iterutils import remap

# Project Imports
from junos_rest.constants import RESULTS

_NAMESPACES = {
    "http://xml.juniper.net/xnm/1.1/xnm:error": "error",
    "http://xml.juniper.net/xnm/1.1/xnm:token": "token",
    "http://xml.juniper.net/xnm/1.1/xnm:message": "message",
    "@http://xml.juniper.net/junos/*/junos:style": "style",
    "http://xml.juniper.net/xnm/1.1/xnm:line-number": "line-number",
    "http://xml.juniper.net/xnm/1.1/xnm:column": "column",
    "http://xml.juniper.net/xnm/1.1/xnm:statement": "statement",
    "http://xml.juniper.net/xnm/1.1/xnm:edit-path": "edit-path",
    "http://xml.juniper.net/xnm/1.1/xnm:source-daemon": "source-daemon",
}

_DELETE_KEYS = ("@xmlns",)


def _fix_keys(path, key, value):
    """Replace XML namespace keys with human-readable keys.

    Also deletes unneeded keys. Used by remap function to iterate
    through a dictionary, is run per-key.
    """
    if key in _NAMESPACES:
        return _NAMESPACES[key], value
    elif key in _DELETE_KEYS:
        return False
    return key, value


def _remap_visit(path, key, value):
    """Process input dictionary.

    Iterate through one level of child dictionaries, and one level of
    list children.
    """
    if isinstance(value, dict):
        fixed_value = remap(value, visit=_fix_keys)
    elif isinstance(value, list):
        fixed_value = []
        for item in value:
            if isinstance(item, dict):
                fixed_item = remap(item, visit=_fix_keys)
            else:
                fixed_item = item
            fixed_value.append(fixed_item)

    if key in _NAMESPACES:
        fixed_key = _NAMESPACES[key]
        fixed_value = value

    elif key in _DELETE_KEYS:
        return False
    else:
        fixed_key = key
        fixed_value = value

    return fixed_key, fixed_value


async def parse_xml(xml):
    """Parse raw XML string to dict.

    Arguments:
        xml {str} -- Raw XML

    Returns:
        {dict} -- XML as parsed dict
    """
    parsed = xmltodict.parse(xml, dict_constructor=dict, process_namespaces=True)
    mapped = remap(parsed, visit=_remap_visit)

    return mapped


async def parse_results(response):
    """Parse raw HTTP response object for success/failure messages.

    Arguments:
        response {object} -- Raw httpx response object

    Returns:
        {dict} -- Constructed results dict
    """
    parsed = await parse_xml(xml=RESULTS.format(results=response.content))
    status = response.status_code
    result = parsed.get("results")

    if "error" in result or "error" in result.get("commit-results", {}):
        error = result.get("error") or result["commit-results"].get("error")

        if error is not None:
            details, messages = error
            output = {"status": "fail", "data": messages["message"], "detail": details}
        else:
            output = {
                "status": "fail",
                "data": "An unknown error occured",
                "detail": [],
            }

    elif (
        status == 200
        and result["commit-results"]["routing-engine"]["commit-success"] is None
    ):
        output = {"status": "success", "data": None}

    elif status and not response.text:
        output = {"status": "success", "data": None}

    elif status in range(400, 600):
        output = {"status": "error", "message": response.text}

    return output

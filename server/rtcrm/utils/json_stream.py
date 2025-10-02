import json
import logging
logger = logging.getLogger(__name__)

def yield_json_objects(incr_text: str):
    """
    Incrementally scan for top-level JSON objects in a stream of text.
    Yields parsed dicts as soon as each full {...} completes.
    """
    depth = 0
    start = None
    for i, ch in enumerate(incr_text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                frag = incr_text[start : i + 1]
                try:
                    yield json.loads(frag)
                except Exception as e:
                    logger.debug("JSON fragment not ready: %s", e)
                start = None

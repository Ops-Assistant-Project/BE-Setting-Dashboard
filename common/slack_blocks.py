from typing import List

def get_mrkdwn_block(text: str, block_id: str = None) -> dict:
    block = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": text}
    }
    if block_id:
        block["block_id"] = block_id
    return block

def get_divider_block(block_id: str = None) -> dict:
    block = {"type": "divider"}
    if block_id:
        block["block_id"] = block_id
    return block

def get_header_block(text: str, block_id: str = None) -> dict:
    block = {
        "type": "header",
        "text": {"type": "plain_text", "text": text, "emoji": True}
    }
    if block_id:
        block["block_id"] = block_id
    return block

def get_context_block(elements: List[dict], block_id: str = None) -> dict:
    block = {"type": "context", "elements": elements}
    if block_id:
        block["block_id"] = block_id
    return block

import copy
import json
from .utils import JSON_INDENT

class Conversation:
    def __init__(self, llm_client, system_prompt):
        self.llm_client = llm_client
        self.messages = [ {"role": "system", "content": system_prompt} ]

    def _messages(self):
        messages = []
        attachments_str = ""
        for msg in self.messages:
            if attachments_str and msg['role'] != 'tool':
                messages.append({"role": "user", "content": "SYSTEM NOTICE: Here is the current content:\n"+attachments_str})
                attachments_str = ""
            for k,v in msg.get("attachments",{}).items():
                if v is None:
                    _attachments_str = f"[Attachment: {k}]\n\n"
                    if not _attachments_str in attachments_str:
                        attachments_str += _attachments_str
                else:
                    if type(v) in (dict, list):
                        v = json.dumps(v, indent=JSON_INDENT)
                    attachments_str += (f"-------- BEGIN {k} --------\n"
                                        f"{v}\n"
                                        f"-------- END {k} ----------\n\n")
            if msg['role'] == 'user':
                messages.append({
                    k: attachments_str + v if k == "content" else v
                    for k, v in msg.items() if not k == "attachments"
                })
                attachments_str = ""
            else:
                messages.append({k: v for k,v in msg.items() if not k == "attachments"})
        if attachments_str:
            messages.append({"role": "user", "content": "SYSTEM NOTICE: Here is the current content:\n"+attachments_str})
        return messages

    def _append_message(self, message, attachments=None):
        if attachments is None:
            attachments = {}
        # Invalidate previous attachments with the same key if the content has changed
        _attachments = {}
        for k, v in attachments.items():
            exists, modified = False, False
            for m in self.messages:
                if k in (a := m.get("attachments",{})):
                    exists = True
                    if a[k] != v:
                        a[k] = None
                        modified = True
            if not exists or modified:
                _attachments[k] = copy.deepcopy(v)
        if _attachments:
            message["attachments"] = _attachments
        self.messages.append(message)

    def llm(self, tools=None):
        resp_msg = self.llm_client.call(self._messages(), tools)
        self.messages.append(resp_msg)
        return resp_msg

    def usermsg(self, content, attachments={}, **kwargs):
        content = content if type(content) is str else json.dumps(content)
        message = {"role": 'user', "content": content, **kwargs}
        self._append_message(message, attachments)

    def toolmsg(self, content, attachments={}, **kwargs):
        content = content if type(content) is str else json.dumps(content)
        message = {"role": 'tool', "content": content, **kwargs}
        self._append_message(message, attachments)

#  Copyright 2020 DASIUSP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from typing import Optional

from google.cloud.exceptions import NotFound
from google.cloud import firestore

db = firestore.Client()


def has_agenda(chat_id: int) -> bool:
    return current_agenda(chat_id) is not None


def add_to_agenda(chat_id: int, text: str) -> None:
    curr_agenda = current_agenda(chat_id)
    curr_agenda.append(text)
    db.collection('agendas').document(str(chat_id)).set({
        'current_agenda': curr_agenda
    })


def has_item(chat_id: int, text: str) -> bool:
    curr_agenda = current_agenda(chat_id)
    return text in curr_agenda


def remove_from_agenda(chat_id: int, text: str) -> None:
    curr_agenda = current_agenda(chat_id)
    curr_agenda.remove(text)
    db.collection('agendas').document(str(chat_id)).update({
        'current_agenda': curr_agenda
    })


def current_agenda(chat_id: int):
    doc_ref = db.collection('agendas').document(str(chat_id))
    try:
        doc = doc_ref.get().to_dict()
        if doc is None:
            return None
        return doc.get('current_agenda')
    except NotFound:
        return None


def initialize_agenda(chat_id: int) -> None:
    db.collection('agendas').document(str(chat_id)).set({
        'current_agenda': []
    })


def finalize_agenda(chat_id: int) -> None:
    db.collection('agendas').document(str(chat_id)).delete()

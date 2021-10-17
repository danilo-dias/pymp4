#!/usr/bin/env python
"""
   Copyright 2016-2019 beardypig
   Copyright 2017-2019 truedread

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import logging

from pymp4.exceptions import BoxNotFound

log = logging.getLogger(__name__)


class BoxUtil:
    @classmethod
    def first(cls, box, type_):
        if hasattr(box.box_body, "children"):
            for sbox in box.box_body.children:
                try:
                    return cls.first(sbox, type_)
                except BoxNotFound:
                    # ignore the except when the box is not found in sub-boxes
                    pass
        elif box.type == type_:
            return box

        raise BoxNotFound(f"could not find box of type: {type_}")

    @classmethod
    def index(cls, box, type_):
        if hasattr(box.box_body, "children"):
            for i, box in enumerate(box.box_body.children):
                if box.type == type_:
                    return i

    @classmethod
    def find(cls, box, type_):
        if box.type == type_:
            yield box
        elif hasattr(box.box_body, "children"):
            for sbox in box.box_body.children:
                for fbox in cls.find(sbox, type_):
                    yield fbox

    @classmethod
    def find_extended(cls, box, extended_type_):
        if hasattr(box.box_body, "extended_type") and box.box_body.extended_type == extended_type_:
            yield box
        elif hasattr(box.box_body, "children"):
            for sbox in box.box_body.children:
                for fbox in cls.find_extended(sbox, extended_type_):
                    yield fbox

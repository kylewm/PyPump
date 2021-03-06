##
# Copyright (C) 2013 Jessica T. (Tsyesika) <xray7224@googlemail.com>
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version. 
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
##

from pypump.models import (PumpObject, Postable, Likeable, Shareable, 
                           Commentable, Deleteable, Mapper)

class Note(PumpObject, Postable, Likeable, Shareable, Commentable, Deleteable):

    object_type = 'note'
    _ignore_attr = ["summary",]
    _mapping = {}
    
    @property
    def ENDPOINT(self):
        return "/api/user/{username}/feed".format(
            username=self._pump.client.nickname
            )

    id = None
    url = None
    display_name = None
    content = None
    published = None # When this was published
    updated = None # last time this was updated
    deleted = None # has the note been deleted
    liked = None
    author = None

    def __init__(self, content=None, id=None, published=None, updated=None, 
                 deleted=False, liked=None, author=None, display_name=None, url=None,
                 *args, **kwargs):

        super(Note, self).__init__(*args, **kwargs)

        self.id = id
        self.url = url
        self.display_name = display_name
        self.content = content
        self.published = published
        self.updated = updated
        self.deleted = deleted
        self.liked = liked
        self.author = author

    def serialize(self):
        """ Converts the post to JSON """
        data = super(Note, self).serialize()
        data.update({
            "verb":"post",
            "object":{
                "objectType":self.object_type,
                "content":self.content,
            }
        })
        if self.display_name:
            data["object"]["displayName"] = self.display_name

        return data

    def __repr__(self):
        return "<{type} by {webfinger}>".format(
            type=self.object_type.capitalize(),
            webfinger=getattr(self.author, 'webfinger', 'unknown')
        )

    def __unicode__(self):
        return u"{type} by {webfinger}".format(
            type=self.object_type,
            webfinger=getattr(self.author, 'webfinger', 'unknown')
        )

    def unserialize(self, data):
        """ Goes from JSON -> Note object """
        Mapper(pypump=self._pump).parse_map(self, data=data)
        self.add_links(data)
        return self

from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from operun.media import MediaMessageFactory as _

class IMedia(Interface):
    """Media"""

    title = schema.TextLine(title=_(u"Title"),
                                    required = True)
    
    description = schema.Text(title=_(u"Description"),
                                    description=_(u"Plain Description of the Body Text"))
    
    text = schema.Text(title=_(u"Body Text"),
                                    required = False)
    
    link = schema.Text(title=_(u"Link"),
                                    description=_(u"Please enter the URL to a file or YouTube video."),
                                    required = False)
    
    file = schema.Text(title=_(u"File"),
                                    description=_(u"Upload a audio or video file."),
                                    required = False)    
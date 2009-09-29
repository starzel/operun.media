from zope.interface import implements

try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.atapi import *

from Products.Archetypes.atapi import DisplayList

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.newsitem import ATNewsItem, ATNewsItemSchema

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.validation import V_REQUIRED

from operun.media.interfaces import IMedia
from operun.media.config import PROJECTNAME

from operun.media import MediaMessageFactory as _

SELECTION = DisplayList((
    ('', 'Keine Vorgabe'),
    ('internal', 'Hochgeladene Datei'),
    ('external', 'Verlinkte Datei'),
    ))


schema = Schema((

    StringField('link',
        searchable = False,
        required = False,
        languageIndependent = True,
        storage = AnnotationStorage(),
        widget = StringWidget(label = _(u"Link"),
                              description = _(u"Please enter the URL to a file or YouTube video."),
                              ),     
        ),
        

    FileField('file',
        searchable = False,
        required = False,
        languageIndependent = True,
        storage = AnnotationStorage(),
        validators = (('isNonEmptyFile', V_REQUIRED), ('checkFileMaxSize', V_REQUIRED)),
        widget = FileWidget(label = _(u"File"),
                            description = _(u"Upload a audio or video file."),
                            ),
        ),
        
    StringField('selection',
        searchable = False,
        storage = AnnotationStorage(),
        vocabulary = SELECTION,
        widget = SelectionWidget(label=_(u"Select source"),
                            description=_(u"Please select what to display."),
                            ),     
        ),
        
    ),
)

MediaSchema = ATNewsItemSchema.copy() + schema.copy()

MediaSchema['title'].storage = AnnotationStorage()
MediaSchema['description'].storage = AnnotationStorage()
MediaSchema['text'].storage = AnnotationStorage()

MediaSchema['image'].widget.description = _(u'label_image_field', default = u'Will be shown in the folder listing, and as screenshot. Image will be scaled to a sensible size.')
MediaSchema['imageCaption'].widget.visible = {"edit": "invisible", "view": "invisible"}
MediaSchema['image'].schemata = 'Media'
MediaSchema['imageCaption'].schemata = 'Media'
MediaSchema['link'].schemata = 'Media'
MediaSchema['file'].schemata = 'Media'
MediaSchema['selection'].schemata = 'Media'

finalizeATCTSchema(MediaSchema, folderish=False, moveDiscussion=False)

class Media(ATNewsItem):
    """Media
    """

    implements(IMedia)

    portal_type = "Media"
    _at_rename_after_creation = True

    schema = MediaSchema
    
    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    text = ATFieldProperty('text')
    link = ATFieldProperty('link')
    file = ATFieldProperty('file')
    

    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)
    
    def __bobo_traverse__(self, REQUEST, name):
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                return image
        if name.startswith('file'):
            field = self.getField('file')
            file = None
            file = field.download(self)
            if file is not None:
                return file
        return super(Media, self).__bobo_traverse__(REQUEST, name)

    def getFileName(self):
        """Returns the file name needed by flowplayer"""
        
        field = self.getField('file')
        filename = field.getFilename(self)
        return filename
    
    def isFile(self):
        """Check if there is a File"""

        #size = self.getField('file').get_size(self)
        size = '1'
        if size:
            return True
        return None
        
registerType(Media, PROJECTNAME)
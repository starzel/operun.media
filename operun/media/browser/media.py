from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize
from operun.media.interfaces import IMedia


class MediaView(BrowserView):

    template = ViewPageTemplateFile('media.pt')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.success = True
        self.link = self.context.getLink()
        self.selection = self.context.getSelection()
        
    def __call__(self):
        context = aq_inner(self.context)
        return self.template()
    
    def isYouTube(self):
        """Check if there is a youtube url and external source is selected to play"""
        if 'youtube' in self.link.split('.'):
            return True
        return None
    
    def isMediaPlayer(self):
        """Check if there is a file uploaded and internal source is selected to play"""
        if self.context.isFile():
            return True
        return None
    
    def getPlayer(self):
        """Return wich player to display"""
        
        if self.isYouTube() and self.isMediaPlayer():
            if self.selection:
                return self.selection
            else:
                return 'external'
        if not self.isYouTube():
            return 'internal'
        if not self.isMediaPlayer():
            return 'external'
    
    def getYouTubeLink(self):
        """Returns the URL used by the embed code by YouTube"""
        return self.link.replace('watch?v=', 'v/')
from zope.interface import alsoProvides, implements, invariant, Invalid
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from collective.behavior.localanalytics import MessageFactory as _


class ILocalAnalytics(form.Schema):
    """
       Marker/Form interface for Local Analytics Settings
    """

    # -*- Your Zope schema definitions here ... -*-
    analytics_type = schema.Choice(
        title=_(u"Analytics Type"),
        description=_(u"Select the type of local analytics to utilise."),
        vocabulary='collective.behavior.localanalytics.vocabularies.analytics',
        required=True
    )

    analytics_id = schema.TextLine(
        title=_(u"Analytics Identifier"),
        description=_(u"Enter your unique identifier associated with your relevant analytics profile."),
        required=False
    )

    @invariant
    def analyticsSettingsProvided(context):
        if context.analytics_type and not context.analytics_id:
            raise Invalid(_("You must specify a unique analytics identifier."))


alsoProvides(ILocalAnalytics,IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)

class LocalAnalytics(object):
    """
       Adapter for Local Analytics Settings
    """
    implements(ILocalAnalytics)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-


import cgi
from zope.interface import implements
from zope.component import getUtility
from zope.viewlet.interfaces import IViewlet

from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces._content import ISiteRoot
from Products.CMFPlone.utils import safe_unicode

from collective.behavior.localanalytics.analytics import IAnalytics
from collective.behavior.localanalytics.behavior import ILocalAnalytics


class AnalyticsViewlet(BrowserView):
    implements(IViewlet)

from plone.app.layout.analytics.view import AnalyticsViewlet


class LocalAnalyticsViewlet(AnalyticsViewlet):

    def render(self):
        """render the webstats snippet"""
        context = self.context

        while context is not None:
            if ILocalAnalytics.providedBy(context):
                break
            if ISiteRoot.providedBy(context):
                context = None
                break
            context = aq_parent(context)

        snippet = ''
        if context and context.analytics_type:
            analytics = getUtility(IAnalytics,
                                   name=context.analytics_type)
            if analytics:
                snippet = safe_unicode(
                    analytics().tag(id=cgi.escape(context.analytics_id,
                                                  quote=True)))

        return snippet

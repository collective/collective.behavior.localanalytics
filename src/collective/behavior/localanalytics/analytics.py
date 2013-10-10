from zope.interface import Interface, implements, Attribute
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtilitiesFor

from collective.behavior.localanalytics import MessageFactory as _


class IAnalytics(Interface):
    """ Interface for analytics tags and configuration.
    """
    identifier = Attribute('Internal identifier')
    title = Attribute('Public facing title')

    def tag(**data):
        """ Returns generated HTML snippet to be rendered.

        Ensure any tags being generated using incoming data correctly
        quote parameters using ``"`` (quotation marks). Not using this
        quoting will likely introduce an XSS issue, allowing arbitrary
        JS or HTML injection by users.
        """

class GoogleAnalyticsClassic(object):
    implements(IAnalytics)
    identifier = 'google_analytics_classic'
    title = 'Google Analytics (Classic)'
    _tag = """<script>var _gaq=[['_setAccount',"%(id)s"],['_trackPageview']];(function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];g.src='//www.google-analytics.com/ga.js';s.parentNode.insertBefore(g,s)}(document,'script'))</script>"""

    def tag(self, **data):
        return self._tag % data

class GoogleAnalyticsUniversal(object):
    implements(IAnalytics)
    identifier = 'google_analytics_universal'
    title = 'Google Analytics (Universal)'
    _tag = """<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');ga('create', "%(id)s");ga('send', 'pageview');</script>"""

    def tag(self, **data):
        return self._tag % data


def getAnalytics(context):
    """ Query registry for all registered analytics options.
    """
    terms = [SimpleTerm(name, name, analytics.title)
             for name, analytics in getUtilitiesFor(IAnalytics)]
    terms.insert(0, (SimpleTerm('', '', _(u'None'))))
    return SimpleVocabulary(terms)

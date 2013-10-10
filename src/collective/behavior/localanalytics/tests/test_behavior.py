import unittest2 as unittest
from plone.testing import z2
from plone.dexterity.fti import DexterityFTI

from collective.behavior.localanalytics.behavior import ILocalAnalytics
from collective.behavior.localanalytics.browser.view \
        import LocalAnalyticsViewlet
from collective.behavior.localanalytics.testing import \
    LOCALANALYTICS_INTEGRATION_TESTING


class TestBehavior(unittest.TestCase):

    layer = LOCALANALYTICS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer.get('app').plone
        self.request = self.layer.get('request')

        #Create a dummy Dexterity container to work with
        fti = DexterityFTI('Container')
        self.portal.portal_types._setObject('Container', fti)
        fti.klass = 'plone.dexterity.content.Container'
        fti.behaviors = ('collective.behavior.localanalytics.behavior.ILocalAnalytics',)
        fti.allowed_content_types = ('Folder',)

        z2.login(self.portal['acl_users'], 'manager')

        #Default configuration for container
        id = self.portal.invokeFactory('Container', 'container')
        self.container = self.portal[id]
        self.container.analytics_type = \
                'collective.behavior.localanalytics.GoogleAnalyticsUniversal'
        self.container.analytics_id = 'UA-12345-XX'

    def test_container(self):
        self.assertEqual(self.container.id, 'container')

    def test_interface(self):
        self.assertTrue(ILocalAnalytics.providedBy(self.container))

    def test_vocabulary(self):
        from collective.behavior.localanalytics.analytics import getAnalytics
        vocabulary = getAnalytics(self.portal)
        self.assertTrue(len(vocabulary) >= 3)
        self.assertEqual(vocabulary._terms[0].title, u'None')

    def test_viewlet_rendering(self):
        self.container.analytics_id = '<script>alert("xss");</script>'
        viewlet = LocalAnalyticsViewlet(self.container,
                                        self.request,
                                        None,
                                        None)
        snippet = viewlet.render()
        self.assertNotIn('alert("xss")', snippet)
        self.assertIn('"&lt;script&gt;alert(&quot;xss&quot;);&lt;/script&gt;"',
                      snippet)

    def test_viewlet_rendering_security(self):
        viewlet = LocalAnalyticsViewlet(self.container,
                                        self.request,
                                        None,
                                        None)
        snippet = viewlet.render()


    def test_viewlet_rendering_empty(self):
        self.portal.invokeFactory('Folder', 'subfolder')
        for context in (self.portal, self.portal['subfolder']):
            viewlet = LocalAnalyticsViewlet(context,
                                            self.request,
                                            None,
                                            None)
            self.assertEqual(viewlet.render(), '')


    def test_viewlet_subcontent(self):
        self.container.invokeFactory('Folder', 'subfolder')
        subfolder = self.container['subfolder']
        subfolder.invokeFactory('Folder', 'subsubfolder')
        subsubfolder = subfolder['subsubfolder']

        #All nested contexts should inherit same settings
        for context in (subfolder, subsubfolder):
            viewlet = LocalAnalyticsViewlet(context,
                                            self.request,
                                            None,
                                            None)
            snippet = viewlet.render()
            for value in (self.container.analytics_id,
                          '<script',
                          '</script>'):
                self.assertIn(value, snippet)


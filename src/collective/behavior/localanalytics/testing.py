from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class LocalAnalyticsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.dexterity
        xmlconfig.file(
            'configure.zcml',
            plone.app.dexterity,
            context=configurationContext
        )
        import collective.behavior.localanalytics
        xmlconfig.file(
            'configure.zcml',
            collective.behavior.localanalytics,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        self['portal'] = portal
        roles = ('Member', 'Manager')
        portal.portal_membership.addMember('manager', 'secret', roles, [])
        roles = ('Member', 'Contributor')
        portal.portal_membership.addMember('contributor', 'secret', roles, [])


LOCALANALYTICS_FIXTURE = LocalAnalyticsLayer()
LOCALANALYTICS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LOCALANALYTICS_FIXTURE,),
    name="LocalAnalyticsLayer:Integration"
)

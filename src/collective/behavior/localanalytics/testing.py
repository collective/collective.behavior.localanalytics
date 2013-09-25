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


LOCALANALYTICS_FIXTURE = LocalAnalyticsLayer()
LOCALANALYTICS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LOCALANALYTICS_FIXTURE,),
    name="LocalAnalyticsLayer:Integration"
)
LOCALANALYTICS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LOCALANALYTICS_FIXTURE, z2.ZSERVER_FIXTURE),
    name="LocalAnalyticsLayer:Functional"
)

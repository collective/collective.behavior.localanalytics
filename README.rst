.. contents::

Introduction
============

.. image:: https://travis-ci.org/collective/collective.behavior.localanalytics.png?branch=master
    :target: https://travis-ci.org/collective/collective.behavior.localanalytics

This package provides a local analytics behaviour for Dexterity-based content
types within Plone.  By associating the ``Local Analytics`` behaviour with
a given context, and configuring the settings on that context accordingly,
an analytics snippet (typically a ``<script>`` tag for page tracking)
will be rendered onto the page.  

The same analytics snippet will be applied to that context and all children.
The only exception to this is where multiple objects in the hierarchy have this
behaviour applied -- in that case, the *closest* parent to the current object
will take precedence.

Why?
----

This behaviour exists for several reasons:

* By default, Plone's support for web analytics is one configuration per site.
  Having a behaviour means allowing one configuration per area (or content
  object).
* To provide optimised preset analytics profiles (Google Analytics is the only
  built-in at present)
* Do so whilst guarding against abitrary script injection by regular users

Adding other analytics providers
--------------------------------

This behaviour is mostly extendable in its current state.  Adding a new
analytics provider is a cause of creating and registering a class or object
conforming to the ``collective.behavior.localanalytics.IAnalytics`` interface
and it will automatically be available.

Future
------

* Allow arbitrary parameters to be passed to analytics providers for tag
  generation.
  
  At present, only a basic textual ID paramter is supported.  In future, since
  other analytics providers will/may more information than just an 
  ``id`` attribute to generate a HTML snippet for rendering. 

Associated Projects
-------------------

`collective.spaces <https://pypi.python.org/pypi/collective.spaces>`_
    collective.spaces is a simple way of creating mini-sites within the Plone
    CMS, with each mini-site based on a fully-customisable template.


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# this is the full version name
# changing it will change version when uploading to pip and in the documentation
GSAPIFullVersion = u'1.0.3'


def getGSAPIFullVersion():
    """Helper to get full version name."""
    return GSAPIFullVersion


def getGSAPIShortVersion():
    """Helper to get only first two elements of full version name."""
    return u'.'.join(GSAPIFullVersion.split('.')[:2])
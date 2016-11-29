from GSBaseDescriptor import *


class GSDescriptorDensity(GSBaseDescriptor):

    def __init__(self, ignoredTags=["silence"], includedTags=[]):
        GSBaseDescriptor.__init__(self)
        self.ignoredTags = ignoredTags
        self.includedTags = includedTags

    def getDescriptorForPattern(self, pattern):
        density = 0
        _checkedPattern = pattern.getPatternWithoutTags(self.ignoredTags)
        if self.includedTags:
            _checkedPattern = _checkedPattern.getPatternWithTags(self.includedTags, copy=False)

        for e in _checkedPattern.events:
                density += e.duration
        return density

from GSBaseDescriptor import *


class GSDescriptorDensity(GSBaseDescriptor):

    def __init__(self, ignoredTags=None, includedTags=None):
        GSBaseDescriptor.__init__(self)
        self.ignoredTags = ignoredTags or ["silence"]
        self.includedTags = includedTags

    def getDescriptorForPattern(self, pattern):
        density = 0
        _checkedPattern = pattern.getPatternWithoutTags(self.ignoredTags)
        if self.includedTags:
            _checkedPattern = _checkedPattern.getPatternWithTags(self.includedTags, makeCopy=False)

        for e in _checkedPattern.events:
                density += e.duration
        return density

from GSBaseDescriptor import *


class GSDescriptorNumberOfTags(GSBaseDescriptor):

    def __init__(self, ignoredTags=None, includedTags=None):
        GSBaseDescriptor.__init__(self)
        self.ignoredTags = ignoredTags or ["silence"]
        self.includedTags = includedTags

    def getDescriptorForPattern(self, pattern):
        density = 0
        _checkedPattern = pattern.getPatternWithoutTags(self.ignoredTags)
        if self.includedTags:
            _checkedPattern = _checkedPattern.getPatternWithTags(self.includedTags, makeCopy=False)

        return len(_checkedPattern.getAllTags())

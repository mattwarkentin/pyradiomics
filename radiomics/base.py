class RadiomicsFeaturesBase(object):
  def __init__(self, inputImage, inputMask):
    '''
    Initialization

    inputImage and inputMask are SimpleITK images. The motivation for using
    SimpleITK images as input is to keep the possibility of reusing the
    optimized feature calculators implemented in SimpleITK in the future.
    '''
    self.inputImage = inputImage
    self.inputMask = inputMask

    # all features are disabled by default
    self.disableAllFeatures()

    self.featureNames = self.getFeatureNames()

  def setBinWidth(self, binWidth):
    self.binWidth = binWidth
    
  def setResampledPixelSpacing(self, resampledPixelSpacing, interpolator=sitk.sitkBSpline):
    self.resampledPixelSpacing = resampledPixelSpacing
    self.interpolator = interpolator

  def setPadDistance(self, padDistance):
    self.padDistance = padDistance

  def setPadFillValue(self, padFillValue):
    self.padFillValue = padFillValue

  def enableFeatureByName(self, featureName, enable=True):
    if not featureName in self.featureNames:
      raise LookupError('Feature not found: '+featureName)
    self.enabledFeatures[featureName] = enable

  def enableAllFeatures(self):
    for featureName in self.featureNames:
      self.enableFeatureByName(featureName, True)

  def disableAllFeatures(self):
    self.enabledFeatures = {}
    self.featureValues = {}

  def getFeatureNames(self):
    allMembers = dir(self)
    allFeatureNames = [f[3:-12] for f in allMembers if f.endswith('FeatureValue') and f.startswith('get')]
    return allFeatureNames

  def calculateFeatures(self):
    for feature in self.enabledFeatures.keys():
      call = 'self.get'+feature+'FeatureValue()'
      self.featureValues[feature] = eval(call)

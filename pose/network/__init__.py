from pose_estimate.network.detector import Detector
from pose_estimate.network.refiner import VolumeRefiner
from pose_estimate.network.selector import ViewpointSelector

name2network={
    'refiner': VolumeRefiner,
    'detector': Detector,
    'selector': ViewpointSelector,
}
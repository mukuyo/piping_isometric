from pose.network.detector import Detector
from pose.network.refiner import VolumeRefiner
from pose.network.selector import ViewpointSelector

name2network={
    'refiner': VolumeRefiner,
    'detector': Detector,
    'selector': ViewpointSelector,
}
__all__ = ['cspace','robotcspace','robotplanning']
import motionplanning
import cspace
import robotcspace
import robotplanning
import atexit
atexit.register(motionplanning.destroy)
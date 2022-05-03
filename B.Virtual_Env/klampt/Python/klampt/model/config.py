"""A uniform interface for getting/setting configurations of arbitrary objects.
A configuration is a flattened list of floats describing the physical pose of
an object. 

Supported objects include world entities, mathematical objects, 
and IK goals.  You can also set a configuration of a set of objects, or a
world, in which case the configuration is the concatenation of the
configurations of each object.

Supported objects include:

- WorldModel
- RobotModel
- RigidObjectModel
- point
- rotation
- rigid transform
- coordinates module objects
- IKObjective 
- lists containing multiple objects (including nested lists)

Notably, used in the :meth:`klampt.vis.visualization.setItemConfig`, 
:meth:`klampt.vis.visualization.getItemConfig`, and
:meth:`klampt.vis.visualization.animate` methods.  Also used in Cartesian
interpolation in the :mod:`cartesian_trajectory` module.

Module summary
==============

API
----

.. autosummary::
    get_config
    set_config
    get_config_names
    num_config_params
    distance
    interpolate

Helpers 
-------

.. autosummary::
    is_compound
    components
    component_names

"""

from ..robotsim import WorldModel,RobotModel,RobotModelLink,RigidObjectModel,IKObjective
from ..math import vectorops,so3,se3
from . import coordinates
import warnings
from .typing import Config
from typing import Union,List

def is_compound(item) -> bool:
    if isinstance(item,WorldModel):
        return True
    elif isinstance(item,coordinates.Group):
        return True
    elif hasattr(item,'__iter__'):
        if all(isinstance(v,(bool,int,float,str)) for v in item):
            return False
        return True
    return False

def components(item):
    """For compound items returns a list of all component sub-items.
    For non-compound items, returns a singular item."""
    if isinstance(item,WorldModel):
        res = [item.robot(i) for i in range(item.numRobots())]
        res += [item.rigidObject(i) for i in range(item.numRigidObjects())]
        return res
    elif isinstance(item,coordinates.Group):
        res = list(item.frames.values())
        res += list(item.points.values())
        res += list(item.directions.values())
        res += [components(g) for g in item.subgroups.values()]
        return res
    elif hasattr(item,'__iter__'):
        if all(isinstance(v,(bool,int,float,str)) for v in item):
            return [item]
        return sum([components(v) for v in item],[])
    return [item]

def component_names(item) -> Union[str,List[str]]:
    """For compound items returns a list of names of all component sub-items.
    For non-compound items, returns a singular name."""
    if isinstance(item,WorldModel):
        res = [item.robot(i).getName() for i in range(item.numRobots())]
        res += [item.rigidObject(i).getName() for i in range(item.numRigidObjects())]
        return res
    elif isinstance(item,coordinates.Group):
        res = list(item.frames.keys())
        res += list(item.points.keys())
        res += list(item.directions.keys())
        res += [component_names(g) for g in item.subgroups.keys()]
        return res
    elif hasattr(item,'__iter__'):
        if all(isinstance(v,(bool,int,float,str)) for v in item):
            return ''
        return sum(['['+str(i)+']'+component_names(v) for i,v in enumerate(item)],[])
    if hasattr(item,'getName'):
        return [item.getName()]
    if hasattr(item,'name'):
        return [item.name]
    return ['']

def num_config_params(item) -> int:
    """Returns the number of free parameters in the flattened version of the configuration
    of the given item. Nearly all Klamp't objects are recognized, including RobotModel's,
    RigidObjectModel's, WorldModel's, IKObjectives, and all variable types in the
    coordinates module.
    """
    if hasattr(item,'getConfig'):
        return len(item.getConfig())
    elif isinstance(item,RigidObjectModel) or isinstance(item,coordinates.Frame):
        return 12
    elif isinstance(item,coordinates.Point) or isinstance(item,coordinates.Direction):
        return 3
    elif isinstance(item,IKObjective):
        if item.numPosDims() == 3 and item.numRotDims() == 3:
            return 12
        start = 0
        if item.numPosDims() == 3:
            start = 6
        elif item.numPosDims() == 2:
            #linear constraint
            start = 9
        elif item.numPosDims() == 1:
            #planar constraint
            start = 7
        if item.numRotDims() == 3:
            return 9+start
        elif item.numRotDims() == 2:
            return 6+start
        return start
    elif is_compound(item):
        return sum(num_config_params(v) for v in components(item))
    elif hasattr(item,'__iter__'):
        return len(item)
    return 0

def get_config(item) -> Config:
    """Returns a flattened version of the configuration of the given item.
    Nearly all Klamp't objects are recognized, including RobotModel's,
    RigidObjectModel's, WorldModel's, IKObjectives, and all variable types in the
    coordinates module.

    TODO: ContactPoint
    """
    if hasattr(item,'getConfig'):
        return item.getConfig()
    elif isinstance(item,RigidObjectModel):
        R,t = item.getTransform()
        return R+t
    elif isinstance(item,coordinates.Point):
        return item.localCoordinates()
    elif isinstance(item,coordinates.Direction):
        return item.localCoordinates()
    elif isinstance(item,coordinates.Frame):
        R,t = item.relativeCoordinates()
        return R+t
    elif isinstance(item,IKObjective):
        x = []
        if item.numPosDims() == 3 and item.numRotDims() == 3:
            #local position is irrelevant
            R,t = item.getTransform()
            return R + t
        if item.numPosDims() == 3:
            loc,wor = item.getPosition()
            x += loc + wor
        elif item.numPosDims() == 2:
            #linear constraint
            loc,wor = item.getPosition()
            axis = item.getPositionDirection()
            x += loc + wor + axis
        elif item.numPosDims() == 1:
            #planar constraint
            loc,wor = item.getPosition()
            axis = item.getPositionDirection()
            x += loc + axis + [vectorops.dot(axis,wor)]
        if item.numRotDims() == 3:
            x += item.getRotation()
        elif item.numRotDims() == 2:
            loc,wor = item.getRotationAxis()
            x += loc + wor
        return x
    elif is_compound(item):
        return sum([get_config(v) for v in components(item)],[])
    elif hasattr(item,'__iter__'):
        if isinstance(item[0],(bool,int,float,str)):
            return item[:]
        else:
            return sum([get_config(v) for v in item],[])
    else:
        return []

def set_config(item, vector : Config) -> None:
    """Sets the configuration of the given item to the given vector.
    Nearly all Klamp't objects are recognized, including RobotModel's,
    RigidObjectModel's, WorldModel's, IKObjectives, and all variable types in the
    coordinates module.

    TODO: ContactPoint
    """
    if hasattr(item,'setConfig'):
        assert len(vector)==item.numLinks(),"Robot model config has %d DOFs"%(item.numLinks(),)
        item.setConfig(vector)
    elif isinstance(item,RigidObjectModel):
        assert len(vector)==12,"Rigid object model config has 12 DOFs, got "+str(len(vector))
        item.setTransform(vector[:9],vector[9:])
    elif isinstance(item,coordinates.Point):
        assert len(vector)==3,"Point config has 3 DOFs, got "+str(len(vector))
        item._localCoordinates = vector[:]
    elif isinstance(item,coordinates.Direction):
        assert len(vector)==3,"Direction config has 3 DOFs, got "+str(len(vector))
        item._localCoordinates = vector[:]
    elif isinstance(item,coordinates.Frame):
        assert len(vector)==12,"Frame config has 12 DOFs, got "+str(len(vector))
        item._relativeCoordinates = (vector[:9],vector[9:])
    elif isinstance(item,IKObjective):
        if item.numPosDims() == 3 and item.numRotDims() == 3:
            #local position is irrelevant
            assert len(vector)==12,"Fixed transform IKObjective config has 12 DOFs, got "+str(len(vector))
            R,t = vector[:9],vector[9:]
            item.setFixedTransform(item.link(),R,t)
            return
        start = 0
        if item.numPosDims() == 3:
            assert len(vector)>=6,"Point IKObjective config has 6 DOFs, got "+str(len(vector))
            loc,wor = vector[:3],vector[3:6]
            item.setFixedPosConstraint(loc,wor)
            start = 6
        elif item.numPosDims() == 2:
            #linear constraint
            assert len(vector)>=9,"Linear IKObjective config has 9 DOFs, got "+str(len(vector))
            loc,wor = vector[:3],vector[3:6]
            axis = vector[6:9]
            item.setLinearPosConstraint(loc,wor,axis)
            start = 9
        elif item.numPosDims() == 1:
            #planar constraint
            assert len(vector)>=7,"Planar IKObjective config has 7 DOFs, got "+str(len(vector))
            loc,n,o = vector[:3],vector[3:6],vector[7]
            item.setPlanarPosConstraint(loc,n,o)
            start = 7
        if item.numRotDims() == 3:
            assert len(vector) == 9+start
            item.setFixedRotConstraint(vector[start:])
        elif item.numRotDims() == 2:
            assert len(vector) == 6+start
            loc,wor = vector[start:start+3],vector[start+3:start+6]
            item.setAxialRotConstraint(loc,wor)
    elif is_compound(item):
        subitems = components(item)
        lengths = []
        for s in subitems:
            lengths.append(num_config_params(s))
        k = 0
        for (s,l) in zip(subitems,lengths):
            set_config(s,vector[k:k+l])
            k += l
    elif hasattr(item,'__iter__'):
        assert isinstance(item[0],(bool,float,int))
        assert len(item) == len(vector)
        for i in range(len(item)):
            item[i] = vector[i]
    return

_so3Names = ['R11','R21','R31','R12','R22','R32','R13','R23','R33']
_pointNames = ['x','y','z']
_se3Names = _so3Names + ['tx','ty','tz']

def get_config_names(item) -> List[str]:
    """Returns a list giving string names for each configuration dimension of given
    item. Nearly all Klamp't objects are recognized, including RobotModel's,
    RigidObjectModel's, WorldModel's, IKObjectives, and all variable types in the
    coordinates module.

    TODO: ContactPoint
    """
    if isinstance(item,RobotModel):
        return [item.link(i).getName() for i in range(item.numLinks())]
    elif isinstance(item,(RigidObjectModel,coordinates.Frame)):
        return _se3Names
    elif isinstance(item,(coordinates.Point,coordinates.Direction)):
        return _pointNames
    elif isinstance(item,IKObjective):
        if item.numPosDims() == 3 and item.numRotDims() == 3:
            #local position is irrelevant
            return _se3Names
        x = []
        if item.numPosDims() == 3:
            x += ['local_x','local_y','local_z','world_x','world_y','world_z']
        elif item.numPosDims() == 2:
            x += ['local_x','local_y','local_z','world_x','world_y','world_z','dir_x','dir_y','dir_z']
        elif item.numPosDims() == 1:
            #planar constraint
            x += ['local_x','local_y','local_z','world_x','world_y','world_z','offset']
        if item.numRotDims() == 3:
            x += _so3Names
        elif item.numRotDims() == 2:
            x += ['local_axis_x','local_axis_y','local_axis_z','world_axis_x','world_axis_y','world_axis_z']
        return x
    elif is_compound(item):
        res = []
        cnames = component_names(item)
        comps = components(item)
        for (cname,comp) in zip(cnames,comps):
            for n in get_config_names(comp):
                res.append(cname+'.'+n)
        return res
    elif hasattr(item,'__iter__'):
        if len(item)==2:
            if isinstance(item[0],(list,tuple)) and len(item[0])==9 and isinstance(item[1],(list,tuple)) and len(item[1])==3:
                #assume it's an se3 element
                return _se3Names
        if len(item)==3 and all([isinstance(v,(float,int)) for v in item]):
            return _pointNames
        if isinstance(item[0],(bool,int,float,str)):
            return ['['+str(i)+']' for i in range(len(item))]
        else:
            return sum(['['+str(i)+'].'+get_config_names(v) for i,v in enumerate(item)],[])
    else:
        return []


def distance(item, a : Config, b : Config) -> float:
    """Returns a distance metric for the given configurations a and b of the given item.
    If possible this is a geodesic distance.
    """
    if hasattr(item,'distance'):
        return item.distance(a,b)
    elif isinstance(item,RigidObjectModel) or isinstance(item,coordinates.Frame):
        return se3.distance((a[:9],a[9:]),(b[:9],b[9:]))
    elif isinstance(item,IKObjective):
        if item.numPosDims() == 3 and item.numRotDims() == 3:
            return se3.distance((a[:9],a[9:]),(b[:9],b[9:]))
        #TODO: geodesic non-fixed orientation distances?
    elif is_compound(item):
        subitems = components(item)
        lengths = []
        for s in subitems:
            lengths.append(num_config_params(s))
        d = 0
        k = 0
        for (s,l) in zip(subitems,lengths):
            d += distance(s,a[k:k+l],b[k:k+l])
            k += l
        return d
    return vectorops.distance(a,b)

def interpolate(item, a : Config, b : Config, u : float) -> Config:
    """Returns a distance metric for the given configurations a and b of the given item.
    If possible this is a geodesic distance.
    """
    if hasattr(item,'interpolate'):
        return item.interpolate(a,b,u)
    elif isinstance(item,RigidObjectModel) or isinstance(item,coordinates.Frame):
        T = se3.interpolate((a[:9],a[9:]),(b[:9],b[9:]),u)
        return T[0]+T[1]
    elif isinstance(item,IKObjective):
        if item.numPosDims() == 3 and item.numRotDims() == 3:
            T = se3.interpolate((a[:9],a[9:]),(b[:9],b[9:]),u)
            return T[0]+T[1]
        #TODO: geodesic non-fixed orientation distances?
    elif is_compound(item):
        subitems = components(item)
        lengths = []
        for s in subitems:
            lengths.append(num_config_params(s))
        res = []
        k = 0
        for (s,l) in zip(subitems,lengths):
            x = interpolate(s,a[k:k+l],b[k:k+l],u)
            assert len(x) == l
            res += x
            k += l
        return res
    return vectorops.interpolate(a,b,u)


def _deprecated_func(oldName,newName):
    import sys
    mod = sys.modules[__name__]
    f = getattr(mod,newName)
    def depf(*args,**kwargs):
        warnings.warn("{} will be deprecated in favor of {} in a future version of Klampt".format(oldName,newName),DeprecationWarning)
        return f(*args,**kwargs)
    depf.__doc__ = 'Deprecated in a future version of Klampt. Use {} instead'.format(newName)
    setattr(mod,oldName,depf)
        
_deprecated_func("isCompound","is_compound")
_deprecated_func("getConfig","get_config")
_deprecated_func("setConfig","set_config")
_deprecated_func("getConfigNames","get_config_names")
_deprecated_func("numConfigParams","num_config_params")
_deprecated_func("componentNames","component_names")

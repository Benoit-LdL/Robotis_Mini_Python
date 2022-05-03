"""Functions for loading/saving Klampt' objects to disk in the same format
as the Klampt C++ bindings / JSON formats.

Can read/write objects using the general purpose reader/writer functions
'read(type,text)' and 'write(x,type)'.

Can load/save objects using the general purpose loader/saver functions
'load(type,fileName)' and 'save(x,type,fileName)'.  The load functions also
support URLs

Json serialization/deserialization are handled using the toJson and fromJson
functions.
"""
from ..robotsim import *
from ..math import so3,vectorops
from ..model.contact import ContactPoint, Hold
from ..model.trajectory import Trajectory
from ..model import types
import os

extensionToTypes = {'.config':['Config'],
                   '.configs':['Configs'],
                   '.tri':['Geometry3D','TriangleMesh'],
                   '.off':['Geometry3D','TriangleMesh'],
                   '.stl':['Geometry3D','TriangleMesh'],
                   '.ply':['Geometry3D','TriangleMesh'],
                   '.wrl':['Geometry3D','TriangleMesh'],
                   '.dae':['Geometry3D','TriangleMesh'],
                   '.poly':['Geometry3D','TriangleMesh'],
                   '.geom':['Geometry3D','GeometricPrimitive'],
                   '.pcd':['Geometry3D','PointCloud'],
                   '.vector3':['Vector3'],
                   '.matrix3':['Matrix3'],
                   '.ikgoal':['IKGoal'],
                   '.xform':['RigidTransform'],
                   '.path':['Trajectory','LinearPath'],
                   '.hold':['Hold'],
                   '.stance':['Stance'],
                   '.grasp':['Grasp'],
                   '.rob':['RobotModel'],
                   '.urdf':['RobotModel'],
                   '.obj':['Geometry3D','RigidObjectModel','TriangleMesh'],
                   '.env':['TerrainModel'],
                   '.xml':['WorldModel','MultiPath']
                   }

unsupportedJsonTypes = ['Geometry3D','TriangleMesh','PointCloud','GeometricPrimitive','VolumeGrid',
    'RobotModel','RigidObjectModel','TerrainModel','WorldModel']

typeToExtensions = dict()
for (k,v) in extensionToTypes.items():
    for t in v:
        if t in typeToExtensions:
            typeToExtensions[t].append(k)
        else:
            typeToExtensions[t] = [k]


def filenameToTypes(name):
    """Returns the Klampt types possibly represented by the given filename's
    extension.
    """
    fileName, fileExtension = os.path.splitext(name)
    if fileExtension in extensionToTypes:
        return extensionToTypes[fileExtension]
    else:
        raise RuntimeError("Cannot determine type of object from filename "+name)

def filenameToType(name):
    """Returns one Klampt type represented by the given filename's
    extension.

    If the file is a dynamic type (.xml or .json), just 'xml' or 'json' is
    returned because the type will need to be determined after parsing the
    file.

    If the type is ambiguous (like .obj), the first type in extensionToTypes is
    returned.

    Returns:
        str: The Klamp't type
    """
    fileName, fileExtension = os.path.splitext(name)
    if fileExtension == '.xml':
        return 'xml'  #dynamic loading
    elif fileExtension == '.json':
        return 'json'  #dynamic loading
    elif fileExtension in extensionToTypes:
        ftypes = extensionToTypes[fileExtension]
        if len(ftypes) > 1 and fileExtension not in ['.path'] and (ftypes[0] != 'Geometry3D' and len(ftypes) > 2):
            print "loader.filenameToType(): Warning: filename",name,"is ambiguous, matches types",', '.join(ftypes)
        return ftypes[0]
    else:
        raise RuntimeError("Cannot determine type of object from filename "+name)

def writeVector(q):
    """Writes a vector to a string in the length-prepended format 'n v1 ... vn'"""
    return str(len(q))+'\t'+' '.join(str(v) for v in q)

def readVector(text):
    """Reads a length-prepended vector from a string 'n v1 ... vn'"""
    items = text.split()
    if len(items) == 0:
        raise ValueError("Empty text")
    if int(items[0])+1 != len(items):
        raise ValueError("Invalid number of items")
    return [float(v) for v in items[1:]]

def writeVectorRaw(x):
    """Writes a vector to a string in the raw format 'v1 ... vn'"""
    return ' '.join(str(xi) for xi in x)

def readVectorRaw(text):
    """Reads a vector from a raw string 'v1 ... vn'"""
    items = text.split()
    return [float(v) for v in items]


def writeVectorList(x):
    """Writes a list of vectors to string"""
    return '\n'.join(writeVector(xi) for xi in x)


def readVectorList(text):
    """Reads a list of endline-separated vectors from a string"""
    items = text.split()
    vectors = []
    pos = 0
    while pos < len(items):
        n = int(items[pos])
        vectors.append([float(v) for v in items[pos+1:pos+1+n]])
        pos += 1+n
    return vectors


def writeMatrix(x):
    """Writes a matrix to a string in the format
    m n
    x11 x12 ... x1n
    ...
    xm1 xm2 ... xmn
    """
    return '\n'.join([str(len(x))+' '+str(len(x[0]))]+[writeVectorRaw(xi) for xi in x])

def readMatrix(text):
    """Reads a matrix from a string in the format
    m n
    x11 x12 ... x1n
    ...
    xm1 xm2 ... xmn
    """
    items = text.split()
    if len(items) < 2: raise ValueError("Invalid matrix string")
    m,n = int(items[0]),int(items[1])
    if len(items) != 2 + m*n:
        raise ValueError("Invalid number of matrix elements, should be %d, instead got %d"%(m*n,len(items)-2))
    k = 2
    x = []
    for i in xrange(m):
        x.append([float(v) for v in items[k:k+n]])
        k += n
    return x

def writeSo3(x):
    """Writes an so3 element, i.e., rotation matrix, to string in the same
    format as written to by Klampt C++ bindings (row major)."""
    assert len(x)==9,"Argument must be an so3 element"
    return '\t'.join([' '.join([str(mij) for mij in mi ]) for mi in so3.matrix(x)])

def readSo3(text):
    """Reads an so3 element, i.e., rotation matrix, from string in the same
    format as written to by Klampt C++ bindings (row major)."""
    items = text.split()
    if len(items) != 9: raise ValueError("Invalid element of SO3, must have 9 elements")
    return so3.inv([float(v) for v in items])


def writeSe3(x):
    """Writes an se3 element, i.e., rigid transformation, to string in the
    same format as written to by Klampt C++ bindings (row major R, followed by
    t)."""
    return writeSo3(x[0])+'\t'+writeVectorRaw(x[1])

def readSe3(text):
    """Reads an se3 element, i.e., rigid transformation, to string in the
    same format as written to by Klampt C++ bindings (row major R, followed by
    t)."""
    items = text.split()
    if len(items) != 12: raise ValueError("Invalid element of SE3, must have 12 elements")
    return (so3.inv([float(v) for v in items[:9]]),[float(v) for v in items[9:]])

def writeMatrix3(x):
    """Writes a 3x3 matrix to a string"""
    return writeSo3(so3.from_matrix(text))

def readMatrix3(text):
    """Reads a 3x3 matrix from a string"""
    return so3.matrix(readSo3(text))

def writeContactPoint(cp):
    """Writes a contact point's members x,n,kFriction"""
    return ' '.join(str(v) for v in cp.tolist())

def readContactPoint(text):
    """Reads a contact point from a string 'x1 x2 x3 n1 n2 n3 kFriction'"""
    items = text.split()
    if len(items)!=7:
        raise ValueError("Invalid number of items, should be 7")
    return ContactPoint([float(v) for v in items[0:3]],[float(v) for v in items[3:6]],float(items[6]))

def writeContactPoint(cp):
    """Writes a contact point to a string 'x1 x2 x3 n1 n2 n3 kFriction'"""
    return ' '.join([str(v) for v in list(cp.x)+list(cp.n)+[cp.kFriction]]) 
    
def readIKObjective(text):
    """Reads an IKObjective from a string in the Klamp't native format
    
    ``link destLink posConstraintType [pos constraint items] ...
    rotConstraintType [rot constraint items]``
    
    where link and destLink are integers, posConstraintType is one of

    * N: no constraint
    * P: position constrained to a plane
    * L: position constrained to a line
    * F: position constrained to a point

    and rotConstraintType is one of

    * N: no constraint
    * T: two-axis constraint (not supported)
    * A: rotation constrained about axis 
    * F: fixed rotation

    The [pos constraint items] contain a variable number of whitespace-
    separated items, dependending on posConstraintType:

    * N: 0 items
    * P: the local position xl yl zl, world position x y z on the plane, and
      plane normal nx,ny,nz
    * L: the local position xl yl zl, world position x y z on the line, and
      line axis direction nx,ny,nz
    * F: the local position xl yl zl and world position x y z

    The [rot constraint items] contain a variable number of whitespace-
    separated items, dependending on rotConstraintType:

    * N: 0 items
    * T: not supported
    * A: the local axis xl yl zl and the world axis x y z
    * F: the world rotation matrix, in moment (aka exponential map) form
      mx my mz (see so3.from_moment())

    """
    items = text.split()
    if len(items) < 4:
        raise ValueError("Not enough items to unpack")
    link = int(items[0])
    destlink = int(items[1])
    ind = 2
    posType = None
    posLocal = None
    posWorld = None
    posDirection = None
    rotType = None
    rotWorld = None
    rotAxis = None
    #read pos constraint
    posType = items[ind]
    ind += 1
    if posType=='N':
        #no constraint
        pass
    elif posType=='P' or posType=='L':
        posLocal = items[ind:ind+3]
        ind += 3
        posWorld = items[ind:ind+3]
        ind += 3
        posDirection = items[ind:ind+3]
        ind += 3
    elif posType=='F':
        posLocal = items[ind:ind+3]
        ind += 3
        posWorld = items[ind:ind+3]
        ind += 3
    else:
        raise ValueError("Invalid pos type "+posType+", must be N,P,L or F")
    rotType = items[ind]
    ind += 1
    if rotType=='N':
        #no constraint
        pass
    elif rotType=='T' or rotType=='A':
        rotAxis = items[ind:ind+3]
        ind += 3
        rotWorld = items[ind:ind+3]
        ind += 3
    elif rotType=='F':
        rotWorld = items[ind:ind+3]
        ind += 3
    else:
        raise ValueError("Invalid rot type "+rotType+", must be N,T,A or F")

    if posLocal: posLocal = [float(v) for v in posLocal]
    if posWorld: posWorld = [float(v) for v in posWorld]
    if posDirection: posDirection = [float(v) for v in posDirection]
    if rotAxis: rotAxis = [float(v) for v in rotAxis]
    if rotWorld: rotWorld = [float(v) for v in rotWorld]
    
    obj = IKObjective()
    obj.setLinks(link,destlink);
    if posType=='N':
        obj.setFreePosConstraint()
    elif posType=='F':
        obj.setFixedPosConstraint(posLocal,posWorld)
    elif posType=='P':
        obj.setPlanePosConstraint(posLocal,posDirection,vectorops.dot(posDirection,posWorld))
    else:
        obj.setLinearPosConstraint(posLocal,posWorld,posDirection)
    if rotType == 'N':
        obj.setFreeRotConstraint()
    elif rotType == 'F':
        #fixed constraint
        R = so3.from_moment(rotWorld)
        obj.setFixedRotConstraint(R)
    elif rotType == 'A':
        obj.setAxialRotConstraint(rotAxis,rotWorld)
    else:
        raise NotImplementedError("Two-axis rotational constraints not supported")
    return obj

def writeIKObjective(obj):
    return obj.saveString()

def readHold(text):
    """Loads a Hold from a string"""
    lines = parseLines(text)
    if lines[0] != 'begin hold':
        raise ValueError('Invalid hold begin text')
    if lines[-1] != 'end':
        raise ValueError('Invalid hold end text')
    h = Hold()
    posLocal = None
    posWorld = None
    localPos0 = None
    rotAxis = None
    rotWorld = None
    iktype = 0
    for l in lines[1:-1]:
        items = l.split()
        if items[1] != '=':
            raise ValueError("Invalid line format")
        if items[0] == 'link':
            h.link = int(items[2])
        elif items[0] == 'contacts':
            ind = 2
            while ind < len(items):
                h.contacts.append(readContactPoint(' '.join(items[ind:ind+7])))
                ind += 7
        elif items[0] == "position":
            posLocal = [float(v) for v in items[2:5]]
            posWorld = [float(v) for v in items[5:8]]
        elif items[0] == "axis":
            rotAxis = [float(v) for v in items[2:5]]
            rotWorld = [float(v) for v in items[5:8]]
        elif items[0] == "rotation":
            rotWorld = [float(v) for v in items[2:5]]
        elif items[0] == "ikparams":
            localPos0 = [float(v) for v in items[2:5]]
            rotWorld = [float(v) for v in items[5:8]]
            iktype = 1
        else:
            raise ValueError("Invalid item "+items[0])
    if iktype == 0:
        h.ikConstraint = IKObjective()
        if posLocal==None:
            raise ValueError("Hold must have some point constraint")
        if rotWorld==None:
            h.ikConstraint.setFixedPoint(h.link,posLocal,posWorld)
        elif rotAxis==None:
            R = so3.from_moment(rotWorld)
            t = vectorops.sub(posWorld,so3.apply(R,posLocal))
            h.ikConstraint.setFixedTransform(h.link,R,t)
        else:
            raise NotImplementedError("Can't do axis rotation yet")
            h.ikConstraint.setAxisRotation(h.link,posLocal,posWorld,localAxis,worldAxis)
    else:
        raise NotImplementedError("other ik specifications not done yet")
        h.setupIKConstraint(localPos0,rotWorld)
    return h
       
def writeHold(h):
    """Writes a Hold to a string"""
    text = "begin hold\n"
    text += "  link = "+str(h.link)+"\n"
    text += "  contacts = ";
    text += " \\\n    ".join([writeContactPoint(c) for c in h.contacts])
    text += "\n"
    localPos, worldPos = h.ikConstraint.getPosition()
    text += "  position = "+" ".join(str(v) for v in localPos)+"  \\\n"
    text += "    "+" ".join(str(v) for v in worldPos)+"\n"
    #TODO: write ik constraint rotation
    if h.ikConstraint.numRotDims()==3:
        #fixed rotation
        m = so3.moment(h.ikConstraint.getRotation())
        text += "rotation = "+" ".join(str(v) for v in m)+"\n"
    elif h.ikConstraint.numRotDims()==1:
        locAxis,worldAxis = h.ikConstraint.getRotationAxis()
        text += "axis = "+" ".join(str(v) for v in locAxis)+"  \\\n"
        text += "    "+" ".join(str(v) for v in worldaxis)+"\n"
    text += "end"
    return text

def writeGeometricPrimitive(g):
    return g.saveString()

def readGeometricPrimitive(text):
    g = GeometricPrimitive()
    if not g.loadString(text):
        raise RuntimeError("Error reading GeometricPrimitive from string")
    return g

def readIntArray(text):
    """Reads a length-prepended vector from a string 'n v1 ... vn'"""
    items = text.split()
    if int(items[0])+1 != len(items):
        raise ValueError("Invalid number of items")
    return [int(v) for v in items[1:]]

def readStringArray(text):
    """Reads a length-prepended vector from a string 'n v1 ... vn'"""
    items = text.split()
    if int(items[0])+1 != len(items):
        raise ValueError("Invalid number of items")
    return items[1:]

def parseLines(text):
    """Returns a list of lines from the given text.  Understands end-of-line escapes '\\n'"""
    lines = text.strip().split('\n')
    esclines = []
    esc = False
    for l in lines:
        if esc:
            esclines[-1] = esclines[-1]+l
        else:
            esclines.append(l)
        if len(l)>0 and l[-1]=='\\':
            esclines[-1] = esclines[-1][:-1]
            esc = True
        else:
            esc = False
    return esclines





readers = {'Config':readVector,
           'Vector':readVector,
           'Configs':readVectorList,
           'Vector3':readVectorRaw,
           'Matrix':readMatrix,
           'Matrix3':readMatrix3,
           'Rotation':readSo3,
           'RigidTransform':readSe3,
           'IKObjective':readIKObjective,
           'IKGoal':readIKObjective,
           'Hold':readHold,
           'GeometricPrimitive':readGeometricPrimitive,
           'IntArray':readIntArray,
           'StringArray':readStringArray,
           }

writers = {'Config':writeVector,
           'Vector':writeVector,
           'Configs':writeVectorList,
           'Vector3':writeVectorRaw,
           'Matrix':writeMatrix,
           'Matrix3':writeMatrix3,
           'Rotation':writeSo3,
           'RigidTransform':writeSe3,
           'IKObjective':writeIKObjective,
           'IKGoal':writeIKObjective,
           'Hold':writeHold,
           'GeometricPrimitive':writeGeometricPrimitive,
           'IntArray':writeVector,
           'StringArray':writeVector,
           }

def autoType(obj,validTypes):
    """Returns a type string for the Klamp't object obj, restricted
    to the set of validTypes.  If there are multiple interpretations,
    the first type in objectToTypes that matches a valid type is
    returned.

    Args:
        obj: A Klamp't-compatible object
        validTypes: a set or dict of possible valid types

    Returns:
        str or None: The type of the object, or None if no valid type
        was found
    """
    otypes = types.objectToTypes(obj)
    if isinstance(otypes,list):
        for otype in otypes:
            if otype in validTypes:
                return otype
        return None
    else:
        #only one type
        return otypes

def write(obj,type):
    """General-purpose write of an arbitrary Klampt object to a str.

    Args:
        obj: A Klampt object
        type (str): Either the Klamp't type, 'json', or 'auto'. If 'auto', the
            type will be auto-detected from the object.

    Returns:
        str: The encoding of the object.
    """
    global writers
    if type == 'auto':
        type = autoType(obj,writers)
        if type is None:
            raise ValueError("Can't determine a writable type for object of type "+obj.__class__.__name__)
    elif type == 'json':
        import json
        return json.dumps(toJson(obj))
    if type not in writers:
        raise ValueError("Writing of objects of type "+type+" not supported")
    return writers[type](obj)

def read(type,text):
    """General-purpose read of an arbitrary Klampt object from a str.

    Args:
        type (str): Either the Klamp't type, or 'json'. Future versions may
            support 'xml' but this is not supported right now.  'auto' may
            not be specified.
        text (str): A string containing the object data.

    Returns:
        Klamp't object
    """
    global readers
    if type == 'json':
        import json
        jsonobj = json.loads(text)
        return fromJson(jsonobj)
    if type not in readers:
        raise ValueError("Reading of objects of type "+type+" not supported")
    return readers[type](text)

def loadWorldModel(fn):
    w = WorldModel()
    if not w.loadFile(fn):
        raise IOError("Error reading WorldModel from "+fn)
    return w

def loadGeometry3D(fn):
    g = Geometry3D()
    if not g.loadFile(fn):
        raise IOError("Error reading Geometry3D from "+fn)
    return g

def loadTrajectory(fn):
    value = Trajectory()
    value.load(fn)
    return value

def loadMultiPath(fn):
    from ..model import multipath
    value = multipath.MultiPath()
    value.load(fn)
    return value

def loadDynamicXML(fn):
    #XML types may only be a WorldModel or MultiPath
    value = WorldModel()
    res = value.readFile(fn)
    if res:
        return value
    try:
        return loadMultiPath(fn)
    except Exception as e:
        raise

loaders = {'Trajectory':loadTrajectory,
           'LinearPath':loadTrajectory,
           'MultiPath':loadMultiPath,
           'Geometry3D':loadGeometry3D,
           'WorldModel':loadWorldModel,
           'xml':loadDynamicXML
           }

savers = {'Trajectory':lambda x,fn:x.save(fn),
          'LinearPath':lambda x,fn:x.save(fn),
          'MultiPath':lambda x,fn:x.save(fn),
          'Geometry3D':lambda x,fn:x.save(fn),
          'WorldModel':lambda x,fn:x.writeFile(fn),
          }

def save(obj,type,fn):
    """General-purpose save of an arbitrary Klampt object to a file.

    This also works with RobotModel, RigidObjectModel, and TerrainModel
    (which don't work with load).

    Args:
        obj: a Klamp't object.
        type (str): the Klampt type, 'json', or 'auto'
        fn (str): a file name

    Returns:
        bool: True if successful.
    """
    global savers,writers

    if hasattr(obj,'saveFile'):
        return obj.saveFile(fn)

    if type == 'auto':
        savers_and_writers = savers.keys() + writers.keys()
        type = autoType(obj,savers_and_writers)
        if type is None:
            raise ValueError("Can't determine a savable type for object of type "+obj.__class__.__name__)
    elif type == 'json':
        import json
        with open(fn,'w') as f:
            json.dump(toJson(obj),f)
        return True
    if type in savers:
        return savers[type](obj,fn)
    elif type in writers:
        with open(fn,'w') as f:
            f.write(writers[type](obj)+'\n')
        return True
    else:
        raise ValueError("Saving of type "+type+" is not supported")


def load(type,fn):
    """General-purpose load of an arbitrary Klampt object from a file
    or URL.

    An exception is raised if there is an error loading or
    parsing the file.  Possible exception types include IOError,
    ValueError, and HTTPError.

    Args:
        type (str): a Klamp't type, 'json', or 'auto'
        fn (str): a filename.

    Returns: 
        Klamp't object
    """
    if type == 'auto':
        type = filenameToType(fn)
    
    global loaders,readers
    cppurl = False
    if type == 'WorldModel' or (type == 'Geometry3D' and fn.find('ros://') >= 0):  #these two types handle URLs in C++ API
        cppurl = True
    if not cppurl and fn.find('://') >= 0:
        import urllib2
        src = None
        data = None
        try:
            src = urllib2.urlopen(fn)
            data = src.read()
            print "klampt.io.loader.load(): Download %s HTTP response code %s, size %d bytes"%(fn,src.getcode(),len(data))
        finally:
            if src:
                src.close()
        if type in loaders:
            #need to write to temporary file
            import os
            import tempfile
            local_filename = None
            fileName, suffix = os.path.splitext(fn)
            with tempfile.NamedTemporaryFile(delete=False,suffix=suffix) as tmp_file:
                local_filename = tmp_file.name
                print "klampt.io.loader.load(): saving data to temp file",local_filename
                tmp_file.write(data)
                tmp_file.flush()
            res = loaders[type](local_filename)
            os.remove(local_filename)
        elif type in readers or type == 'json':
            res = readers[type](data)
        else:
            raise ValueError("Loading of type "+type+" is not supported")
        return res

    if type in loaders:
        return loaders[type](fn)
    elif type in readers or type == 'json':
        text = None
        with open(fn,'r') as f:
            text = ''.join(f.readlines())
        return read(type,text)
    else:
        raise ValueError("Loading of type "+type+" is not supported")



def toJson(obj,type='auto'):
    """Converts from a Klamp't object to a JSON-compatible structure.
    If 'type' is not provided, the type of the object is inferred
    automatically.

    The structure can be converted to a JSON string using json.dumps().
    
    Not all objects are supported yet.
    """
    if type == 'auto':
        if isinstance(obj,(list,tuple)):
            if all([isinstance(v,(bool,int,float)) for v in obj]):
                type = 'Vector'
            else:
                if len(obj)==2 and len(obj[0])==9 and len(obj[1])==3:
                    type = 'RigidTransform'
                else:
                    isconfigs = True
                    for item in obj:
                        if not all([isinstance(v,(bool,int,float)) for v in item]):
                            isconfigs = False
                    if isconfigs:
                        type = 'Configs'
                    else:
                        raise TypeError("Could not parse object "+str(obj))
        elif isinstance(obj,(bool,int,float,str,unicode)):
            type = 'Value'
        elif obj.__class__.__name__ in ['ContactPoint','IKObjective','Trajectory','MultiPath']:
            type = obj.__class__.__name__
        elif isinstance(obj,Trajectory):   #some subclasses of Trajectory may be used here too
            type = "Trajectory"
        else:
            raise TypeError("Unknown object of type "+obj.__class__.__name__)

    if type in ['Config','Configs','Vector','Matrix','Vector2','Vector3','Matrix3','Point','Rotation','Value','IntArray','StringArray']:
        return obj
    elif type == 'RigidTransform':
        return obj
    elif type == 'ContactPoint':
        return {'x':obj.x,'n':obj.n,'kFriction':kFriction}
    elif type == 'Trajectory' or type == 'LinearPath':
        return {'times':obj.times,'milestones':obj.milestones}
    elif type == 'IKObjective' or type == 'IKGoal':
        res = {'type':type,'link':obj.link()}
        if obj.destLink() >= 0:
            res['destLink'] = obj.destLink()
        if obj.numPosDims()==3:
            res['posConstraint']='fixed'
            res['localPosition'],res['endPosition']=obj.getPosition()
        elif obj.numPosDims()==2:
            res['posConstraint']='linear'
            res['localPosition'],res['endPosition']=obj.getPosition()
            res['direction']=obj.getPositionDirection()
        elif obj.numPosDims()==1:
            res['posConstraint']='planar'
            res['localPosition'],res['endPosition']=obj.getPosition()
            res['direction']=obj.getPositionDirection()
        else:
            #less verbose to just eliminate this 
            #res['posConstraint']='free'
            pass
        if obj.numRotDims()==3:
            res['rotConstraint']='fixed'
            res['endRotation']=so3.moment(obj.getRotation())
        elif obj.numRotDims()==2:
            res['rotConstraint']='axis'
            res['localAxis'],res['endRotation']=obj.getRotationAxis()
        elif obj.numRotDims()==1:
            raise NotImplementedError("twoaxis constraints are not implemented in Klampt")
        else:
            #less verbose to just eliminate this
            #res['rotConstraint']='free'
            pass
        return res
    elif type in writers:
        return {'type':type,'data':write(obj,type)}
    else:
        raise ValueError("Unknown or unsupported type "+type)


def fromJson(jsonobj,type='auto'):
    """Converts from a JSON structure to a Klamp't object of the appropriate
    type.  If 'type' is not provided, the type of the object is inferred
    automatically.

    A JSON structure can be created from a JSON string using json.loads().
    """
    if type == 'auto':
        if isinstance(jsonobj,(list,tuple)):
            return jsonobj
        elif isinstance(jsonobj,(bool,int,float,str,unicode)):
            return jsonobj
        elif isinstance(jsonobj,dict):
            if 'type' in jsonobj:
                type = jsonobj["type"]
            elif 'times' in jsonobj and 'milestones' in jsonobj:
                type = 'Trajectory'
            elif 'x' in jsonobj and 'n' in jsonobj and 'kFriction' in jsonobj:
                type = 'ContactPoint'
        else:
            raise TypeError("Unknown JSON object of type "+jsonobj.__class__.__name)

    if type in ['Config','Configs','Vector','Matrix','Matrix3','Rotation','Value','IntArray','StringArray']:
        return jsonobj
    elif type == 'RigidTransform':
        return jsonobj
    elif type == 'ContactPoint':
        return ContactPoint(jsonobj['x'],jsonobj['n'],jsonobj['kFriction'])
    elif type == 'Trajectory' or type == 'LinearPath':
        return Trajectory(jsonobj['times'],jsonobj['milestones'])
    elif type == 'IKObjective' or type == 'IKGoal':
        link = jsonobj['link']
        destlink = jsonobj['destLink'] if 'destLink' in jsonobj else -1
        posConstraint = 'free'
        rotConstraint = 'free'
        localPosition = endPosition = None
        direction = None
        endRotation = None
        localAxis = None
        if 'posConstraint' in jsonobj:
            posConstraint = jsonobj['posConstraint']
        if 'rotConstraint' in jsonobj:
            rotConstraint = jsonobj['rotConstraint']
        if posConstraint == 'planar' or posConstraint == 'linear':
            direction = jsonobj['direction']
        if posConstraint != 'free':
            localPosition = jsonobj['localPosition']
            endPosition = jsonobj['endPosition']
        if rotConstraint != 'free':
            endRotation = jsonobj['endRotation']
        if rotConstraint == 'axis' or rotConstraint == 'twoaxis':
            localAxis = jsonobj['localAxis']
        if posConstraint == 'free' and rotConstraint == 'free':
            #empty
            return IKObjective()
        elif posConstraint != 'fixed':
            raise NotImplementedError("Can't do non-fixed position constraints yet in Python API")
        if rotConstraint == 'twoaxis':
            raise NotImplementedError("twoaxis constraints are not implemented in Klampt")
        if rotConstraint == 'free':
            obj = IKObjective()
            if destlink >= 0:
                obj.setRelativePoint(link,destlink,localPosition,endPosition)
            else:
                obj.setFixedPoint(link,localPosition,endPosition)
            return obj
        elif rotConstraint == 'axis':
            obj = IKObjective()
            h = 0.1
            lpts = [localPosition,vectorops.madd(localPosition,localAxis,h)]
            wpts = [endPosition,vectorops.madd(endPosition,endRotation,h)]
            if destlink >= 0:
                obj.setRelativePoints(link,destlink,lpts,wpts)
            else:
                obj.setFixedPoints(link,lpts,wpts)
            return obj
        elif rotConstraint == 'fixed':
            obj = IKObjective()
            R = so3.from_moment(endRotation)
            t = vectorops.sub(endPosition,so3.apply(R,localPosition))
            obj.setFixedTransform(link,R,t)
            return obj
        else:
            raise ValueError("Invalid IK rotation constraint "+rotConstraint)
    elif type in readers:
        return read(type,jsonobj["data"])
    else:
        raise ValueError("Unknown or unsupported type "+type)

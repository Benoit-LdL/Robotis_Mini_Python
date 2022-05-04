#ifndef _GEOMETRY_H
#define _GEOMETRY_H

#include <vector>
#include <map>

/** @file geometry.h
 * @brief C++ bindings for geometry modeling. */

/** @brief A 3D indexed triangle mesh class.
 *
 * Attributes:
 *
 *     vertices (SWIG vector of floats):  a list of vertices, given as
 *         a flattened coordinate list [x1, y1, z1, x2, y2, ...]
 *     indices (SWIG vector of ints): a list of triangle vertices given
 *         as indices into the vertices list, i.e., [a1,b1,c2, a2,b2,c2, ...]
 *
 * Note: because the bindings are generated by SWIG, you can access
 * the indices / vertices members via some automatically generated
 * accessors / modifiers.  In particular len(), append(), and
 * indexing via [] are useful. Some other methods like resize() are
 * also provided.  However, you CANNOT set these items via assignment. 
 *
 * Examples::
 *
 *     m = TriangleMesh()
 *     m.vertices.append(0)
 *     m.vertices.append(0)
 *     m.vertices.append(0)
 *     print(len(m.vertices))  #prints 3
 *     m.vertices = [0,0,0]   #this is an error
 *     m.vertices += [1,2,3]   #this is also an error
 *
 * To get all vertices as a numpy array::
 * 
 *     verts = np.array(m.vertices).reshape((len(m.vertices)//3,3))
 *
 * To get all indices as a numpy array::
 * 
 *     inds = np.array(m.indices,dtype=np.int32).reshape((len(m.indices)//3,3))
 *
 * (Or use the convenience functions in :mod:`klampt.io.numpy_convert`)
 */
struct TriangleMesh
{
  TriangleMesh();
  ///Retrieves a view of the vertices as an nx3 Numpy array
  void getVertices(double** np_view2, int* m, int* n);
  ///Sets all vertices to the given nx3 Numpy array
  void setVertices(double* np_array2, int m, int n);
  ///Retrieves a view of the vertices as an mx3 Numpy array
  void getIndices(int** np_view2, int* m, int* n);
  ///Sets all indices to the given mx3 Numpy array
  void setIndices(int* np_array2, int m, int n);
  ///Translates all the vertices by v=v+t
  void translate(const double t[3]);
  ///Transforms all the vertices by the rigid transform v=R*v+t
  void transform(const double R[9],const double t[3]);

  std::vector<int> indices;
  std::vector<double> vertices;
};

/** @brief Stores a set of points to be set into a ConvexHull type. Note: 
 * These may not actually be the vertices of the convex hull; the actual
 * convex hull may be computed internally for some datatypes.
 *
 * Attributes:
 * 
 *     points (SWIG vector of floats): a list of points, given  as a flattened
 *         coordinate list [x1,y1,z1,x2,y2,...]
 *
 */
struct ConvexHull
{
  ConvexHull();
  ///Returns the # of points
  int numPoints() const; 
  ///Retrieves a view of the points as an nx3 Numpy array
  void getPoints(double** np_view2, int* m, int* n);
  ///Sets all points to the given nx3 Numpy array
  void setPoints(double* np_array2, int m, int n);
  ///Adds a point
  void addPoint(const double pt[3]);
  ///Retrieves a point
  void getPoint(int index,double out[3]) const;
  ///Translates all the vertices by v=v+t
  void translate(const double t[3]);
  ///Transforms all the vertices by the rigid transform v=R*v+t
  void transform(const double R[9],const double t[3]);

  std::vector<double> points;
};

/** @brief A 3D point cloud class.  
 *
 * Attributes:
 * 
 *     vertices (SWIG vector of floats): a list of vertices, given as a
 *         list [x1, y1, z1, x2, y2, ... zn]
 *     properties (SWIG vector of floats): a list of vertex properties,
 *        given as a list [p11, p21, ..., pk1,  p12, p22, ..., pk2, ...,
 *        p1n, p2n, ..., pkn] where each vertex has k properties.  The
 *        name of each property is given by the ``propertyNames`` member.
 *     propertyNames (SWIG vector of strs): a list of the names of each
 *        property
 *     settings (SWIG map of strs to strs): a general property map .
 *
 * .. note::
 *
 *     Because the bindings are generated by SWIG, you can access the members
 *     via some automatically generated accessors / modifiers.  In particular
 *     len(), append(), and indexing via [] are useful. Some other methods like
 *     resize() and iterators are also provided.  However, you CANNOT set these
 *     items via assignment, i.e., ``pc.vertices = [0,0,0]`` is not allowed. 
 *
 * Property names are usually lowercase but follow PCL naming convention, and 
 * often include:
 *
 * - ``normal_x``, ``normal_y``, ``normal_z``: the outward normal 
 * - ``rgb``, ``rgba``: integer encoding of RGB (24 bit int, format 0xrrggbb)
 *   or RGBA color (32 bit int, format 0xaarrggbb) 
 * - ``opacity``: opacity, in range [0,1]
 * - ``c``: opacity, in range [0,255]
 * - ``r,g,b,a``: color channels, in range [0,1]
 * - ``u,v``: texture coordinate
 * - ``radius``: treats the point cloud as a collection of balls 
 * 
 * Settings are usually lowercase but follow PCL naming convention, and often
 * include:
 *
 * - ``version``: version of the PCL file, typically "0.7" 
 * - ``id``: integer id
 * - ``width``: the width (in pixels) of a structured point cloud
 * - ``height``: the height (in pixels) of a structured point cloud
 * - ``viewpoint``: Camera position and orientation in the form 
 *   ``ox oy oz qw qx qy qz``, with (ox,oy,oz) the focal point and 
 *   (qw,qx,qy,qz) the quaternion representation of the orientation (canonical
 *   representation, with X right, Y down, Z forward).
 *
 * Examples::
 * 
 *     pc = PointCloud()
 *     pc.propertyNames.append('rgb')
 *     #add 1 point with coordinates (0,0,0) and color #000000 (black)
 *     pc.vertices.append(0)
 *     pc.vertices.append(0)
 *     pc.vertices.append(0)
 *     pc.properties.append(0)
 *     print(len(pc.vertices))  #prints 3
 *     print(pc.numPoints())  #prints 1
 *     #add another point with coordinates (1,2,3)
 *     pc.addPoint([1,2,3])
 *     #this prints 2
 *     print(pc.numPoints() )
 *     #this prints 2, because there is 1 property category x 2 points
 *     print(len(pc.properties.size()))
 *     #this prints 0; this is the default value added when addPoint is called
 *     print(pc.getProperty(1,0) )
 *
 * To get all points as an n x 3 numpy array::
 *
 *     points = np.array(pc.vertices).reshape((pc.numPoints(),3))
 * 
 * To get all properties as a n x k numpy array::
 *
 *     properties = np.array(pc.properties)
 *     properties.reshape((p.numPoints(),p.numProperties()))
 *
 * (Or use the convenience functions in :mod:`klampt.io.numpy_convert`)
 */
struct PointCloud
{
  PointCloud();
  ///Returns the number of points
  int numPoints() const;
  ///Returns the number of properties
  int numProperties() const;
  ///Returns a view of the points as an nx3 Numpy array
  void getPoints(double** np_view2, int* m, int* n);
  ///Sets all the points to the given nx3 Numpy array
  void setPoints(double* np_array2, int m, int n);
  ///Sets all the points and m properties from the given n x (3+m) array
  void setPointsAndProperties(double* np_array2, int m,int n);
  ///Adds a point. Sets all its properties to 0.  
  ///
  ///Returns the point's index.
  int addPoint(const double p[3]);
  ///Sets the position of the point at the given index to p
  void setPoint(int index,const double p[3]);
  ///Returns the position of the point at the given index
  void getPoint(int index,double out[3]) const;
  ///Sets all the properties of all points to the given nxp array 
  void setProperties(double* np_array2, int m, int n);
  ///Adds a new property.  All values for this property are set to 0.
  void addProperty(const std::string& pname);
  ///Adds a new property with name pname, and sets values for this property to the given length-n array
  void addProperty(const std::string& pname,double* np_array,int m);
  ///Sets property pindex of all points to the given length-n array
  void setProperties(int pindex,double* np_array,int m);
  ///Sets property pindex of point index to the given value
  void setProperty(int index,int pindex,double value);
  ///Sets the property named pname of point index to the given value
  void setProperty(int index,const std::string& pname,double value);
  ///Returns property pindex of point index 
  double getProperty(int index,int pindex) const;
  ///Returns the property named pname of point index
  double getProperty(int index,const std::string& pname) const;
  ///Returns property pindex of all points as an array
  void getProperties(int pindex,double** np_out,int* m) const;
  ///Returns property named pindex of all points as an array
  void getProperties(const std::string& pname,double** np_out,int* m) const;
  ///Returns all the properties as an nxp array
  void getAllProperties(double** np_view2, int* m, int* n);
  ///Translates all the points by v=v+t
  void translate(const double t[3]);
  ///Transforms all the points by the rigid transform v=R*v+t
  void transform(const double R[9],const double t[3]);
  ///Adds the given point cloud to this one.  They must share the same
  ///properties or else an exception is raised
  void join(const PointCloud& pc);
  ///Sets the given setting
  void setSetting(const std::string& key,const std::string& value);
  ///Returns the given setting
  std::string getSetting(const std::string& key) const;
  ///Sets a structured point cloud from a depth image.  [fx,fy,cx,cy] are the intrinsics parameters.  The depth is given as a size hxw array, top to bottom.
  void setDepthImage_d(const double intrinsics[4],double* np_array2,int m,int n,double depth_scale);
  ///Sets a structured point cloud from a depth image.  [fx,fy,cx,cy] are the intrinsics parameters.  The depth is given as a size hxw array, top to bottom.
  void setDepthImage_f(const double intrinsics[4],float* np_depth2,int m2,int n2,double depth_scale);
  ///Sets a structured point cloud from a depth image.  [fx,fy,cx,cy] are the intrinsics parameters.  The depth is given as a size hxw array, top to bottom.
  void setDepthImage_s(const double intrinsics[4],unsigned short* np_depth2,int m2,int n2,double depth_scale);
  ///Sets a structured point cloud from an RGBD (color,depth) image pair.  [fx,fy,cx,cy] are the intrinsics parameters.  The RGB colors are packed in 0xrrggbb order, size hxw, top to bottom.
  void setRGBDImages_i_d(const double intrinsics[4],unsigned int* np_array2,int m,int n,double* np_depth2,int m2,int n2,double depth_scale);
  ///Sets a structured point cloud from an RGBD (color,depth) image pair.  [fx,fy,cx,cy] are the intrinsics parameters.  The RGB colors are packed in 0xrrggbb order, size hxw, top to bottom.
  void setRGBDImages_i_f(const double intrinsics[4],unsigned int* np_array2,int m,int n,float* np_depth2,int m2,int n2,double depth_scale);
  ///Sets a structured point cloud from an RGBD (color,depth) image pair.  [fx,fy,cx,cy] are the intrinsics parameters.  The RGB colors are packed in 0xrrggbb order, size hxw, top to bottom.
  void setRGBDImages_i_s(const double intrinsics[4],unsigned int* np_array2,int m,int n,unsigned short* np_depth2,int m2,int n2,double depth_scale);
  ///Sets a structured point cloud from an RGBD (color,depth) image pair.  [fx,fy,cx,cy] are the intrinsics parameters.  The RGB colors are packed in 0xrrggbb order, size hxw, top to bottom.
  void setRGBDImages_b_d(const double intrinsics[4],unsigned char* np_array3,int m,int n,int p,double* np_depth2,int m2,int n2,double depth_scale);
  ///Sets a structured point cloud from an RGBD (color,depth) image pair.  [fx,fy,cx,cy] are the intrinsics parameters.  The RGB colors are an h x w x 3 array, top to bottom.
  void setRGBDImages_b_f(const double intrinsics[4],unsigned char* np_array3,int m,int n,int p,float* np_depth2,int m2,int n2,double depth_scale);
  ///Sets a structured point cloud from an RGBD (color,depth) image pair.  [fx,fy,cx,cy] are the intrinsics parameters.  The RGB colors are an h x w x 3 array, top to bottom.
  void setRGBDImages_b_s(const double intrinsics[4],unsigned char* np_array3,int m,int n,int p,unsigned short* np_depth2,int m2,int n2,double depth_scale);
  

  std::vector<double> vertices;
  std::vector<std::string> propertyNames;
  std::vector<double> properties;
  std::map<std::string,std::string> settings;
};

/** @brief A geometric primitive.  So far only points, spheres, segments,
 * and AABBs can be constructed manually in the Python API. 
 *
 * Attributes:
 *
 *     type (str): Can be "Point", "Sphere", "Segment", "Triangle", 
 *         "Polygon", "AABB", and "Box".  Semi-supported types include 
 *         "Ellipsoid", and "Cylinder".
 *     properties (SWIG vector): a list of parameters defining the 
 *         primitive. The interpretation is type-specific.
 *
 */
struct GeometricPrimitive
{
  GeometricPrimitive();
  void setPoint(const double pt[3]);
  void setSphere(const double c[3],double r);
  void setSegment(const double a[3],const double b[3]);
  void setTriangle(const double a[3],const double b[3],const double c[3]);
  void setPolygon(const std::vector<double>& verts);
  void setAABB(const double bmin[3],const double bmax[3]);
  void setBox(const double ori[3],const double R[9],const double dims[3]);
  bool loadString(const char* str);
  std::string saveString() const;

  std::string type;
  std::vector<double> properties;
};

/** @brief An axis-aligned volumetric grid, typically a signed distance
 * transform with > 0 indicating outside and < 0 indicating inside. 
 * Can also store an occupancy grid with 1 indicating inside and 0
 * indicating outside.
 * 
 * In general, values are associated with cells rather than vertices. So,
 * cell (i,j,k) is associated with a single value, and has size
 * (w,d,h) = ((bmax[0]-bmin[0])/dims[0], (bmax[1]-bmin[1])/dims[1], (bmax[2]-bmin[2])/dims[2]).
 * It ranges over the box [w*i,w*(i+1)) x [d*j,d*(j+1)) x [h*k,h*(k+1)).
 * 
 * For SDFs and TSDFs which assume values at vertices, the values are specified
 * at the **centers** of cells.  I.e., at (w*(i+1/2),d*(j+1/2),h*(k+1/2)).
 *
 * Attributes:
 *
 *     bbox (SWIG vector of 6 doubles): contains min and max bounds
 *         (xmin,ymin,zmin),(xmax,ymax,zmax)
 *     dims (SWIG vector of  of 3 ints): size of grid in each of 3 dimensions
 *     values (SWIG vector of doubles): contains a 3D array of
 *          ``dims[0]*dims[1]*dims[1]`` values. 
 * 
 *          The cell index (i,j,k) is flattened to
 *          ``i*dims[1]*dims[2] + j*dims[2] + k``.
 *
 *          The array index i is associated to cell index
 *          ``(i/(dims[1]*dims[2]), (i/dims[2]) % dims[1], i%dims[2])``
 * 
 */
class VolumeGrid
{
public:
  VolumeGrid();
  void setBounds(const double bmin[3],const double bmax[3]);
  void resize(int sx,int sy,int sz);
  void set(double value);
  void set(int i,int j,int k,double value);
  double get(int i,int j,int k);
  void shift(double dv);
  ///Returns a 3D Numpy array view of the values
  void getValues(double** np_view3, int* m, int* n, int* p);
  void setValues(double* np_array3, int m, int n, int p);

  std::vector<double> bbox; 
  std::vector<int> dims;
  std::vector<double> values; 
};

/** @brief Configures the _ext distance queries of
 * :class:`~klampt.Geometry3D`.
 *
 * The calculated result satisfies :math:`Dcalc \leq D(1+relErr) + absErr`
 * unless :math:`D \geq upperBound`, in which case Dcalc=upperBound may 
 * be returned.
 *
 * Attributes:
 * 
 *     relErr (float, optional): Allows a relative error in the reported
 *         distance to speed up computation.  Default 0.
 *     absErr (float, optional): Allows an absolute error in the reported
 *         distance to speed up computation.  Default 0.
 *     upperBound (float, optional): The calculation may branch if D exceeds
 *         this bound.
 *
 */
class DistanceQuerySettings
{
public:
  DistanceQuerySettings();
  double relErr;
  double absErr;
  double upperBound;
};

/** @brief The result from a "fancy" distance query of 
 * :class:`~klampt.Geometry3D`.
 *
 * Attributes:
 *
 *     d (float): The calculated distance, with negative values indicating
 *         penetration.  Can also be upperBound if the branch was hit.
 *     hasClosestPoints (bool):  If true, the closest point information is
 *         given in cp0 and cp1, and elem1 and elem2
 *     hasGradients (bool):  f true, distance gradient information is given
 *         in grad0 and grad1.
 *     cp1, cp2 (list of 3 floats, optional): closest points on self vs other,
 *         both given in world coordinates
 *     grad1, grad2 (list of 3 floats, optional): the gradients of the
 *         objects' signed distance fields at the closest points.  Given in
 *         world coordinates. 
 *         
 *         I.e., to move object1 to touch object2, move it in direction
 *         grad1 by distance -d.  Note that grad2 is always -grad1.
 *     elems1, elems2 (int): for compound objects, these are the
 *         element indices corresponding to the closest points.
 *
 */
class DistanceQueryResult
{
public:
  DistanceQueryResult();
  double d;
  bool hasClosestPoints;
  bool hasGradients;
  std::vector<double> cp1,cp2;
  std::vector<double> grad1,grad2;
  int elem1,elem2;
};

/** @brief The result from a contact query of :class:`~klampt.Geometry3D`.
 * The number of contacts n is variable.
 *
 * Attributes:
 *
 *     depths (list of n floats): penetration depths for each contact point. 
 *         The depth is measured with respect to the padded geometry, and must
 *         be nonnegative. A value of 0 indicates that depth cannot be 
 *         determined accurately.
 *     points1, points2 (list of n lists of floats): contact points on self vs 
 *         other,  The top level list has n entries, and each entry is a
 *         3-list expressed in world coordinates.  If an object is padded,
 *         these points are on the surface of the padded geometry.
 *     normals (list of n lists of floats): the outward-facing contact normal
 *         from this to other at each contact point, given in world
 *         coordinates.  Each entry is a 3-list, and can be a unit vector,
 *         or [0,0,0] if the the normal cannot be computed properly.
 *     elems1, elems2 (list of n ints): for compound objects, these are the
 *         element indices corresponding to each contact.
 * 
 */
class ContactQueryResult
{
public:
  ContactQueryResult();
  std::vector<double> depths;
  std::vector<std::vector<double> > points1,points2;
  std::vector<std::vector<double> > normals;
  std::vector<int> elems1,elems2;
};

/** @brief The three-D geometry container used throughout Klampt.  
 *
 * There are five currently supported types of geometry:
 *
 * - primitives (:class:`GeometricPrimitive`)
 * - triangle meshes (:class:`TriangleMesh`)
 * - point clouds (:class:`PointCloud`)
 * - volumetric grids (:class:`VolumeGrid`)
 * - groups ("Group" type)
 * - convex hulls (:class:`ConvexHull`)
 * 
 * This class acts as a uniform container of all of these types.
 *
 * There are two modes in which a Geometry3D can be used.  It can be a
 * standalone geometry, which means it is a container of geometry data,
 * or it can be a reference to a world item's geometry.  For references,
 * modifiers change the world item's geometry.
 *
 * **Current transform**
 *
 * Each geometry stores a "current" transform, which is automatically
 * updated for world items' geometries.  Proximity queries are then
 * performed *with respect to the transformed geometries*.  Crucially, the
 * underlying geometry is not changed, because that could be computationally
 * expensive. 
 *
 * **Creating / modifying the geometry**
 *
 * Use the constructor, the :meth:`set`, or the set[TYPE]() methods to
 * completely change the geometry's data.
 *
 * Note: if you want to set a world item's geometry to be equal to a standalone
 * geometry, use the set(rhs) function rather than the assignment (=)
 * operator.
 *
 * Modifiers include:
 * 
 * - :meth:`setCurrentTransform`: updates the current transform.  (This call is
 *   very fast.)
 * - :meth:`translate`, :meth:`scale`, :meth:`rotate`, and :meth:`transform`
 *   transform the underlying geometry.  Any collision data structures will
 *   be recomputed after transformation. 
 * - :meth:`loadFile`: load from OFF, OBJ, STL, PCD, etc.  Also supports native
 *   Klamp't types .geom and .vol.
 * 
 * .. note::
 *
 *     Avoid the use of translate, rotate, and transform to represent object
 *     movement.  Use setCurrentTransform instead.
 *
 * **Proximity queries**
 * 
 * - :meth:`collides`: boolean collision query.
 * - :meth:`withinDistance`: boolean proximity query.
 * - :meth:`distance` and :meth:`distance_ext`: numeric-valued distance query.
 *   The distance may be negative to indicate signed distance, available for
 *   certain geometry types. Also returns closest points for certain geometry
 *   types.
 * - :meth:`distance_point` and :meth:`distance_point_ext`: numeric valued
 *   distance-to-point queries.
 * - :meth:`contacts`: estimates the contact region between two objects.
 * - :meth:`rayCast` and :meth:`rayCast_ext`: ray-cast queries.
 *
 * For most geometry types (TriangleMesh, PointCloud, ConvexHull), the
 * first time you perform a query, some collision detection data structures
 * will be initialized.  This preprocessing step can take some time for complex
 * geometries.
 *
 * **Collision margins**
 * 
 * Each object also has a "collision margin" which may virtually fatten the
 * object, as far as proximity queries are concerned. This is useful
 * for setting collision avoidance margins in motion planning.  Use the
 * :meth:`setCollisionMargin` and :meth:`getCollisionMargin` methods to access
 * the margin. By default the margin is zero. 
 *
 * .. note::
 *
 *     The geometry margin is NOT the same thing as simulation body collision
 *     padding!  All proximity queries are affected by the collision padding,
 *     inside or outside of simulation.
 *
 * **Conversions**
 *
 * Many geometry types can be converted to and from one another using the
 * :meth:`convert` method.  This can also be used to remesh TriangleMesh
 * objects and PointCloud objects.
 *
 */
class Geometry3D
{
 public:
  Geometry3D();
  Geometry3D(const Geometry3D&);
  Geometry3D(const GeometricPrimitive&);
  Geometry3D(const ConvexHull&);
  Geometry3D(const TriangleMesh&);
  Geometry3D(const PointCloud&);
  Geometry3D(const VolumeGrid&);
  ~Geometry3D();
  const Geometry3D& operator = (const Geometry3D& rhs);
  ///Creates a standalone geometry from this geometry (identical to copy... will be deprecated in a future version)
  Geometry3D clone();
  ///Creates a standalone geometry from this geometry
  Geometry3D copy();
  ///Copies the geometry of the argument into this geometry.
  void set(const Geometry3D&);
  ///Returns True if this is a standalone geometry
  bool isStandalone();
  ///Frees the data associated with this geometry, if standalone 
  void free();
  ///Returns the type of geometry: TriangleMesh, PointCloud, VolumeGrid, 
  ///GeometricPrimitive, or Group
  std::string type();
  ///Returns True if this has no contents (not the same as numElements()==0)
  bool empty();
  ///Returns a TriangleMesh if this geometry is of type TriangleMesh
  TriangleMesh getTriangleMesh();
  ///Returns a PointCloud if this geometry is of type PointCloud
  PointCloud getPointCloud();
  ///Returns a GeometricPrimitive if this geometry is of type GeometricPrimitive
  GeometricPrimitive getGeometricPrimitive();
  ///Returns a ConvexHull if this geometry is of type ConvexHull
  ConvexHull getConvexHull();
  ///Returns a VolumeGrid if this geometry is of type VolumeGrid
  VolumeGrid getVolumeGrid();
  ///Sets this Geometry3D to a TriangleMesh
  void setTriangleMesh(const TriangleMesh&);
  ///Sets this Geometry3D to a PointCloud
  void setPointCloud(const PointCloud&);
  ///Sets this Geometry3D to a GeometricPrimitive
  void setGeometricPrimitive(const GeometricPrimitive&);
  ///Sets this Geometry3D to a ConvexHull
  void setConvexHull(const ConvexHull&);
  ///Sets this Geometry3D to be a convex hull of two geometries.  Note: the relative
  ///transform of these two objects is frozen in place; i.e., setting the current
  ///transform of g2 doesn't do anything to this object.
  void setConvexHullGroup(const Geometry3D& g1, const Geometry3D & g2);
  ///Sets this Geometry3D to a volumeGrid
  void setVolumeGrid(const VolumeGrid&);
  ///Sets this Geometry3D to a group geometry.  To add sub-geometries, 
  ///repeatedly call setElement() with increasing indices.
  void setGroup();
  ///Returns an element of the Geometry3D if it is a Group, TriangleMesh, or 
  ///PointCloud.  Raises an error if this is of any other type.  
  ///
  ///The element will be in local coordinates.
  Geometry3D getElement(int element);
  ///Sets an element of the Geometry3D if it is a Group, TriangleMesh, or
  /// PointCloud. The element will be in local coordinates.
  ///Raises an error if this is of any other type.  
  void setElement(int element,const Geometry3D& data);
  ///Returns the number of sub-elements in this geometry
  int numElements();

  ///Loads from file.  Standard mesh types, PCD files, and .geom files are
  ///supported.
  ///
  ///Returns:
  ///
  ///    True on success, False on failure
  ///
  bool loadFile(const char* fn);
  ///Saves to file.  Standard mesh types, PCD files, and .geom files are
  ///supported.
  bool saveFile(const char* fn);
  ///Sets the current transformation (not modifying the underlying data)
  void setCurrentTransform(const double R[9],const double t[3]);
  ///Gets the current transformation 
  void getCurrentTransform(double out[9],double out2[3]);
  ///Translates the geometry data.
  ///Permanently modifies the data and resets any collision data structures.
  void translate(const double t[3]);
  ///Scales the geometry data uniformly.
  ///Permanently modifies the data and resets any collision data structures.
  void scale(double s);
  ///Scales the geometry data with different factors on each axis.
  ///Permanently modifies the data and resets any collision data structures.
  void scale(double sx,double sy,double sz);
  ///Rotates the geometry data.
  ///Permanently modifies the data and resets any collision data structures.
  void rotate(const double R[9]);
  ///Translates/rotates/scales the geometry data.
  ///Permanently modifies the data and resets any collision data structures.
  void transform(const double R[9],const double t[3]);
  ///Sets a padding around the base geometry which affects the results of
  ///proximity queries
  void setCollisionMargin(double margin);
  ///Returns the padding around the base geometry.  Default 0
  double getCollisionMargin();
  ///Returns an axis-aligned bounding box of the object as a tuple (bmin,bmax). 
  ///
  ///Note: O(1) time, but may not be tight
  void getBB(double out[3],double out2[3]);
  ///Computes a tighter axis-aligned bounding box of the object than
  ///:meth:`Geometry3D.getBB`. Worst case O(n) time.
  void getBBTight(double out[3],double out2[3]);
  /** @brief Converts a geometry to another type, if a conversion is
   * available.  The interpretation of param depends on the type of
   * conversion, with 0 being a reasonable default.
   *
   * Available conversions are:
   *
   *   - TriangleMesh -> PointCloud.  param is the desired dispersion of
   *        the points, by default set to the average triangle diameter. 
   *        At least all of the mesh's vertices will be returned.
   *   - TriangleMesh -> VolumeGrid.  Converted using the fast marching
   *        method with good results only if the mesh is watertight.
   *        param is the grid resolution, by default set to the average
   *        triangle diameter.
   *   - TriangleMesh -> ConvexHull.  If param==0, just calculates a convex
   *        hull. Otherwise, uses convex decomposition with the HACD library.
   *   - PointCloud -> TriangleMesh. Available if the point cloud is
   *        structured. param is the threshold for splitting triangles
   *        by depth discontinuity. param is by default infinity.
   *   - PointCloud -> ConvexHull.  Converted using SOLID / Qhull.
   *   - GeometricPrimitive -> anything.  param determines the desired
   *        resolution.
   *   - VolumeGrid -> TriangleMesh.  param determines the level set for
   *         the marching cubes algorithm.
   *   - VolumeGrid -> PointCloud.  param determines the level set.
   *   - ConvexHull -> TriangleMesh. 
   *   - ConvexHull -> PointCloud.  param is the desired dispersion of the
   *         points.  Equivalent to ConvexHull -> TriangleMesh -> PointCloud
   *
   */
  Geometry3D convert(const char* type,double param=0);
  /** @brief Returns true if this geometry collides with the other
   *
   * Unsupported types:
   *
   * - VolumeGrid - GeometricPrimitive [aabb, box, triangle, polygon]
   * - VolumeGrid - TriangleMesh
   * - VolumeGrid - VolumeGrid
   * - ConvexHull - anything else besides ConvexHull
   */
  bool collides(const Geometry3D& other);
  ///Returns true if this geometry is within distance ``tol`` to other
  bool withinDistance(const Geometry3D& other,double tol);
  ///Version 0.8: this is the same as the old distance() function.
  ///
  ///Returns the distance from this geometry to the other.  If either geometry 
  ///contains volume information, this value may be negative to indicate
  ///penetration.  See :meth:`Geometry3D.distance` for more information.
  double distance_simple(const Geometry3D& other,double relErr=0,double absErr=0);
  ///Returns the the distance and closest point to the input point, given in 
  ///world coordinates.  An exception is raised if this operation is not 
  ///supported with the given geometry type.
  ///
  ///The return value contains the distance, closest points, and gradients if
  ///available.
  ///
  ///For some geometry types, the signed distance is returned.  The signed
  ///distance returns the negative penetration depth if pt is within this.
  ///The following geometry types return signed distances:
  ///
  ///- GeometricPrimitive
  ///- PointCloud (approximate, if the cloud is a set of balls with the radius
  ///  property)
  ///- VolumeGrid
  ///- ConvexHull
  ///
  ///For other types, a signed distance will be returned if the geometry has
  ///a positive collision margin, and the point penetrates less than this margin.
  DistanceQueryResult distance_point(const double pt[3]);
  ///A customizable version of :meth:`Geometry3D.distance_point`.
  ///The settings for the calculation can be customized with relErr, absErr, 
  ///and upperBound, e.g., to break if the closest points are at least
  ///upperBound distance from one another.
  DistanceQueryResult distance_point_ext(const double pt[3],const DistanceQuerySettings& settings);
  ///Returns the the distance and closest points between the given geometries.
  ///This may be either the normal distance or the signed distance, depending on
  ///the geometry type. 
  ///
  ///The normal distance returns 0 if the two objects are touching
  ///(this.collides(other)=True).
  ///
  ///The signed distance returns the negative penetration depth if the objects
  ///are touching.  Only the following combinations of geometry types return
  ///signed distances:
  ///
  ///- GeometricPrimitive-GeometricPrimitive (Python-supported sub-types only)
  ///- GeometricPrimitive-TriangleMesh (surface only)
  ///- GeometricPrimitive-PointCloud
  ///- GeometricPrimitive-VolumeGrid
  ///- TriangleMesh (surface only)-GeometricPrimitive
  ///- PointCloud-VolumeGrid
  ///- ConvexHull - ConvexHull
  ///
  ///If penetration is supported, a negative distance is returned and cp1,cp2
  ///are the deepest penetrating points.
  ///
  ///Unsupported types:
  ///
  ///- GeometricPrimitive-GeometricPrimitive subtypes segment vs aabb
  ///- PointCloud-PointCloud
  ///- VolumeGrid-TriangleMesh
  ///- VolumeGrid-VolumeGrid
  ///- ConvexHull - anything else besides ConvexHull
  ///
  ///See the comments of the distance_point function
  DistanceQueryResult distance(const Geometry3D& other);
  ///A customizable version of :meth:`Geometry3D.distance`.
  ///The settings for the calculation can be customized with relErr, absErr,
  ///and upperBound, e.g., to break if the closest points are at least
  ///upperBound distance from one another.  
  DistanceQueryResult distance_ext(const Geometry3D& other,const DistanceQuerySettings& settings);
  ///Performs a ray cast.
  ///
  ///Supported types:
  ///
  ///- GeometricPrimitive
  ///- TriangleMesh
  ///- PointCloud (need a positive collision margin, or points need to have a
  ///  'radius' property assigned)
  ///- VolumeGrid
  ///- Group (groups of the aforementioned types)
  ///
  ///Returns:
  ///
  ///    (hit,pt) where hit is true if the ray starting at s and pointing
  ///    in direction d hits the geometry (given in world coordinates); pt is
  ///    the hit point, in world coordinates.
  ///
  bool rayCast(const double s[3],const double d[3],double out[3]);
  ///A more sophisticated ray cast. 
  ///
  ///Supported types:
  ///
  ///- GeometricPrimitive
  ///- TriangleMesh
  ///- PointCloud (need a positive collision margin, or points need to have a
  ///  'radius' property assigned)
  ///- VolumeGrid
  ///- Group (groups of the aforementioned types)
  ///
  ///Returns:
  ///
  ///    (hit_element,pt) where hit_element is >= 0 if ray starting at 
  ///    s and pointing in direction d hits the geometry (given in world 
  ///    coordinates).  
  ///
  ///    - hit_element is -1 if the object is not hit, otherwise it gives the
  ///      index of the element (triangle, point, sub-object) that was hit.  
  ///      For geometric primitives, this will be 0.
  ///    - pt is the hit point, in world coordinates.
  ///
  int rayCast_ext(const double s[3],const double d[3],double out[3]);
 
  ///Returns the set of contact points between this and other.  This set
  ///is a discrete representation of the region of surface overlap, which
  ///is defined as all pairs of points within distance
  ///self.collisionMargin + other.collisionMargin + padding1 + padding2.
  ///
  ///For some geometry types (TriangleMesh-TriangleMesh,
  ///TriangleMesh-PointCloud, PointCloud-PointCloud) padding must be positive
  ///to get meaningful contact poitns and normals.
  ///
  ///If maxContacts != 0  a clustering postprocessing step is performed.
  ///
  ///Unsupported types:
  ///
  ///- GeometricPrimitive-GeometricPrimitive subtypes segment vs aabb
  ///- VolumeGrid-GeometricPrimitive any subtypes except point and sphere.
  ///  also, the results are potentially inaccurate for non-convex VolumeGrids.
  ///- VolumeGrid-TriangleMesh
  ///- VolumeGrid-VolumeGrid
  ///- ConvexHull - anything
  ///
  ContactQueryResult contacts(const Geometry3D& other,double padding1,double padding2,int maxContacts=0);
  ///Calculates the furthest point on this geometry in the direction dir.
  ///
  ///Supported types:
  ///
  ///- ConvexHull
  ///
  void support(const double dir[3], double out[3]);
  ///Calculates a 2D slice through the data. The slice is given by the local X-Y plane of a 
  ///transform (R,T) with orientation R and translation t.  The return Geometry's data is in
  ///the local frame of (R,t), and (R,t) is set as its current transform. 
  ///
  ///The geometry's current transform is respected.
  ///
  ///O(N) time.
  ///
  ///Supported types:
  ///
  ///- PointCloud.  Needs tol > 0.  A PointCloud is returned.
  ///- TriangleMesh. tol is ignored. A Group of GeometricPrimitives (segments) is returned.
  ///
  Geometry3D slice(const double R[9],const double t[3],double tol);
  ///Calculates a region of interest of the data for the bounding box [bmin,bmax]. 
  ///The geometry's current transform is respected.
  ///
  ///`query` can be "intersect", "touching", or "within". If "intersect", this tries to get a
  ///representation of the geometry intersecting the box.  If "touching", all elements touching
  ///the box are returned.  If "within", only elements entirely inside the box are returned.
  ///
  ///`query` can also be prefaced with a '~' which indicates that the ROI should be inverted,
  ///i.e. select everything that does NOT intersect with a box.
  ///
  ///O(N) time.
  ///
  ///Supported types:
  ///
  ///- PointCloud
  ///- TriangleMesh
  ///
  Geometry3D roi(const char* query,const double bmin[3],const double bmax[3]);

  int world;
  int id;
  void* geomPtr;
};

#endif
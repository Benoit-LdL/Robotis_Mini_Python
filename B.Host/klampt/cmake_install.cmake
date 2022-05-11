# Install script for directory: /home/benoit/Desktop/motion-planner/klampt

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/opt/klampt-0.9.0")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/benoit/Desktop/motion-planner/klampt/Cpp/Main/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/benoit/Desktop/motion-planner/klampt/Python/cmake_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xlibrariesx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/benoit/Desktop/motion-planner/klampt/lib/libKlampt.a")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/Contact" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/ContactDistance.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/ContactFeature.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/ContactFeatureMapping.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/Grasp.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/Hold.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/HoldReader.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/LineReader.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/Polygon2DSampler.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/Stance.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/TriangleSampler.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Contact/Utils.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/Control" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/Command.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/ContactController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/ControlledRobot.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/Controller.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/FeedforwardController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/JointTrackingController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/LoggingController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/OperationalSpaceController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/PathController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/PyController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/SerialControlledRobot.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/SerialController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Control/TabulatedController.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/IO" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/JSON.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/ROS.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/URDFConverter.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/XmlODE.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/XmlWorld.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/three.js.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_color.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_exception.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_joint.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_link.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_model.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_model_state.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_parser.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_pose.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_sensor.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_twist.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/IO/urdf_world.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/Interface" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/GLUIGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/GLUTGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/GenericGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/InputProcessor.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/NavigationGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/ResourceGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/RobotInterface.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/RobotPoseGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/RobotTestGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/SimTestGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/SimViewProgram.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/SimulationGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/UserInterface.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/WorldGUI.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Interface/WorldViewProgram.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/Modeling" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/Config.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/Conversions.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/DynamicPath.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/GeneralizedRobot.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/Interpolate.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/ManagedGeometry.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/Mass.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/MultiPath.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/ParabolicRamp.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/Paths.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/RandomizedSelfCollisions.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/Resources.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/RigidObject.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/Robot.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/SplineInterpolate.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/Terrain.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Modeling/World.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/Planning" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/ConfigFixer.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/ConstrainedInterpolator.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/ConstraintChecker.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/ContactCSpace.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/ContactTimeScaling.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/DistanceQuery.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/NumericalConstraint.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/ParameterizedVectorField.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/PlannerObjective.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/PlannerSettings.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/RampCSpace.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/RealTimeIKPlanner.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/RealTimePlanner.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/RealTimeRRTPlanner.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/RobotCSpace.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/RobotConstrainedInterpolator.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/RobotTimeScaling.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/SelfTest.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/StanceCSpace.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/TimeScaling.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Planning/ZMP.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/Sensing" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Sensing/Common_Internal.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Sensing/ForceSensors.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Sensing/InertialSensors.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Sensing/JointSensors.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Sensing/OtherSensors.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Sensing/Sensor.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Sensing/StateEstimator.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Sensing/VisualSensors.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/Simulation" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/ODECommon.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/ODECustomGeometry.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/ODEGeometry.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/ODERigidObject.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/ODERobot.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/ODESimulator.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/ODESurface.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/Settings.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/SimRobotController.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/Simulation/Simulator.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xheadersx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Klampt/View" TYPE FILE FILES
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/Callbacks.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ObjectPoseWidget.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/RobotPoseWidget.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/Texturizer.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewCamera.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewGrasp.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewHold.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewIK.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewPlot.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewResource.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewRobot.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewStance.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewTextures.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/ViewWrench.h"
    "/home/benoit/Desktop/motion-planner/klampt/Cpp/View/WorldDragWidget.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdocumentationx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/." TYPE DIRECTORY FILES "/home/benoit/Desktop/motion-planner/klampt/Documentation")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/benoit/Desktop/motion-planner/klampt/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")

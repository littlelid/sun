INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_TCPMATLAB tcpmatlab)

FIND_PATH(
    TCPMATLAB_INCLUDE_DIRS
    NAMES tcpmatlab/api.h
    HINTS $ENV{TCPMATLAB_DIR}/include
        ${PC_TCPMATLAB_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    TCPMATLAB_LIBRARIES
    NAMES gnuradio-tcpmatlab
    HINTS $ENV{TCPMATLAB_DIR}/lib
        ${PC_TCPMATLAB_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(TCPMATLAB DEFAULT_MSG TCPMATLAB_LIBRARIES TCPMATLAB_INCLUDE_DIRS)
MARK_AS_ADVANCED(TCPMATLAB_LIBRARIES TCPMATLAB_INCLUDE_DIRS)


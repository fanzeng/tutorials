cmake_minimum_required(VERSION 2.8)
find_package(PkgConfig)

pkg_check_modules(GSTV REQUIRED  gstreamer-video-1.0)
include_directories(${GSTV_INCLUDE_DIRS})

pkg_check_modules(GST REQUIRED  gstreamer-1.0)
include_directories(${GST_INCLUDE_DIRS})

pkg_check_modules(GTK3 REQUIRED gtk+-3.0)
include_directories(${GTK3_INCLUDE_DIRS})

pkg_check_modules(GSTA REQUIRED  gstreamer-audio-1.0)
include_directories(${GSTA_INCLUDE_DIRS})

pkg_check_modules(GSTPBU REQUIRED  gstreamer-pbutils-1.0)
include_directories(${GSTPBU_INCLUDE_DIRS})

set(SRC_DIR src)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(basic-tutorial-1 ${SRC_DIR}/basic-tutorial-1.c)
target_link_libraries(basic-tutorial-1 ${GST_LIBRARIES})

add_executable(basic-tutorial-2 ${SRC_DIR}/basic-tutorial-2.c)
target_link_libraries(basic-tutorial-2 ${GST_LIBRARIES})

add_executable(basic-tutorial-3 ${SRC_DIR}/basic-tutorial-3.c)
target_link_libraries(basic-tutorial-3 ${GST_LIBRARIES})

add_executable(basic-tutorial-4 ${SRC_DIR}/basic-tutorial-4.c)
target_link_libraries(basic-tutorial-4 ${GST_LIBRARIES})

add_executable(basic-tutorial-5 ${SRC_DIR}/basic-tutorial-5.c)
target_link_libraries(basic-tutorial-5
    ${GSTV_LIBRARIES}
    ${GTK3_LIBRARIES}
    ${GST_LIBRARIES}
)

add_executable(basic-tutorial-6 ${SRC_DIR}/basic-tutorial-6.c)
target_link_libraries(basic-tutorial-6 ${GST_LIBRARIES})

add_executable(basic-tutorial-7 ${SRC_DIR}/basic-tutorial-7.c)
target_link_libraries(basic-tutorial-7 ${GST_LIBRARIES})

add_executable(basic-tutorial-8 ${SRC_DIR}/basic-tutorial-8.c)
target_link_libraries(basic-tutorial-8 ${GST_LIBRARIES} ${GSTA_LIBRARIES})

add_executable(basic-tutorial-9 ${SRC_DIR}/basic-tutorial-9.c)
target_link_libraries(basic-tutorial-9 ${GST_LIBRARIES} ${GSTPBU_LIBRARIES})

add_executable(basic-tutorial-12 ${SRC_DIR}/basic-tutorial-12.c)
target_link_libraries(basic-tutorial-12 ${GST_LIBRARIES})
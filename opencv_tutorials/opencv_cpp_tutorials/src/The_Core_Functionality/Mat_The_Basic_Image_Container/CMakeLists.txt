add_executable(MatTheBasicImageContainer MatTheBasicImageContainer.cpp)
target_link_libraries(MatTheBasicImageContainer ${OpenCV_LIBS})
set_target_properties(MatTheBasicImageContainer
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# CMake generated Testfile for 
# Source directory: /home/fzeng/CMakeTest
# Build directory: /home/fzeng/CMakeTest/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
ADD_TEST(TutorialRuns "Tutorial" "25")
ADD_TEST(TutorialHalf25 "Tutorial" "25")
SET_TESTS_PROPERTIES(TutorialHalf25 PROPERTIES  PASS_REGULAR_EXPRESSION "25 is 12.5")
ADD_TEST(TutorialComp25 "Tutorial" "25")
SET_TESTS_PROPERTIES(TutorialComp25 PROPERTIES  PASS_REGULAR_EXPRESSION "25 is 5")
ADD_TEST(TutorialUsage "Tutorial")
SET_TESTS_PROPERTIES(TutorialUsage PROPERTIES  PASS_REGULAR_EXPRESSION "Usage: .*number")
ADD_TEST(TutorialComp4 "Tutorial" "4")
SET_TESTS_PROPERTIES(TutorialComp4 PROPERTIES  PASS_REGULAR_EXPRESSION "4 is 2")
ADD_TEST(TutorialComp9 "Tutorial" "9")
SET_TESTS_PROPERTIES(TutorialComp9 PROPERTIES  PASS_REGULAR_EXPRESSION "9 is 3")
SUBDIRS(src/MathFunctions)

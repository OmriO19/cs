cmake_minimum_required(VERSION 3.17)
project(ex4)

set(CMAKE_CXX_STANDARD 14)

add_executable(ex4 SimpleTest.cpp VirtualMemory.cpp VirtualMemory.h PhysicalMemory.cpp
        PhysicalMemory.h MemoryConstants.h)

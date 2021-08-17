cmake_minimum_required(VERSION 3.17)
project(ex3)

set(CMAKE_CXX_STANDARD 14)

add_executable(ex3 SampleClient.cpp MapReduceClient.h MapReduceFramework.h MapReduceFramework.cpp
        Barrier.cpp Barrier.h)

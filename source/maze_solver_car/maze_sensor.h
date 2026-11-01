#ifndef MAZE_SENSOR_H
#define MAZE_SENSOR_H

struct MazeDistances {
  int left;
  int front;
  int right;
};

void initSensor();
MazeDistances scanMaze();

#endif
#pragma once

#include <math.h>
#include <limits>
#include <float.h>
#include <cstdlib>
#include <cmath>

#define piValue 3.14159265359
#define piValD2 1.570796326794
#define piValTimes2 6.28318530718
#define radToDeg 57.2957795130785499
#define degToRad 0.017453292519944444

#define piValue_f 3.14159265359f
#define piValD2_f 1.570796326794f
#define piValTimes2_f 6.28318530718f
#define radToDeg_f 57.2957795130785499f
#define degToRad_f 0.017453292519944444f

#define SIM_MAX_FLOAT (0.01f*FLT_MAX)
#define SIM_MAX_DOUBLE (0.01*DBL_MAX)
#define SIM_MAX_INT INT_MAX
#define SIM_RAND_FLOAT (static_cast<float>(rand())/static_cast<float>(RAND_MAX))
#define VREP_IS_NAN(x) ((std::isnan)(x))
#define VREP_IS_FINITE(x) ((std::isfinite)(x))

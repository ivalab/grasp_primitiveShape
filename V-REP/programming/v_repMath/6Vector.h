#pragma once

#include "mathDefines.h"
#include "3Vector.h"

class C6X6Matrix;

class C6Vector  
{
public:
    C6Vector();
    C6Vector(float v0,float v1,float v2,float v3,float v4,float v5);
    C6Vector(const float v[6]);
    C6Vector(const C3Vector& v0,const C3Vector& v1);
    C6Vector(const C6Vector& v);
    ~C6Vector();

    void clear();
    C6X6Matrix getSpatialCross() const;

    C6Vector operator* (float d) const;
    C6Vector operator/ (float d) const;
    C6Vector operator+ (const C6Vector& v) const;
    C6Vector operator- (const C6Vector& v) const;

    void operator*= (float d);
    void operator/= (float d);
    void operator+= (const C6Vector& v);
    void operator-= (const C6Vector& v);

    float operator* (const C6Vector& v) const;
    C6Vector& operator= (const C6Vector& v);

    inline void getInternalData(float d[6]) const
    {
        V[0].getInternalData(d+0);
        V[1].getInternalData(d+3);
    }
    inline void setInternalData(const float d[6])
    {
        V[0].setInternalData(d+0);
        V[1].setInternalData(d+3);
    }
    inline float& operator() (unsigned i)
    {
        if (i<3)
            return(V[0](i));
        else
            return(V[1](i-3));
    }
    inline const float& operator() (unsigned i) const
    {
        if (i<3)
            return(V[0](i));
        else
            return(V[1](i-3));
    }

    C3Vector V[2];
};

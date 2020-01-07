#pragma once

#include "mathDefines.h"
#include "3Vector.h"
#include "4Vector.h"

class C4X4Matrix; // Forward declaration

class C7Vector  
{
public:
    C7Vector();
    C7Vector(const C7Vector& v);
    C7Vector(const C4Vector& q);
    C7Vector(const C3Vector& x);
    C7Vector(const C4Vector& q,const C3Vector& x);
    C7Vector(const float m[4][4]);
    C7Vector(const C4X4Matrix& m);
    C7Vector(float angle,const C3Vector& pos,const C3Vector& dir);
    ~C7Vector();

    void setIdentity();
    void set(float m[4][4]);
    void set(const C4X4Matrix& m);
    C4X4Matrix getMatrix() const;
    C7Vector getInverse() const;
    void setMultResult(const C7Vector& v1,const C7Vector& v2);
    void buildInterpolation(const C7Vector& fromThis,const C7Vector& toThat,float t);
    void inverse();
    void copyTo(float m[4][4]) const;
    C3Vector getAxis(int index) const;

    C7Vector operator* (const C7Vector& v) const;

    void operator*= (const C7Vector& v);

    C3Vector operator* (const C3Vector& v) const;
    C7Vector& operator= (const C7Vector& v);

    inline void getInternalData(float d[7]) const
    {
        X.getInternalData(d+0);
        Q.getInternalData(d+3);
    }
    inline void setInternalData(const float d[7])
    {
        X.setInternalData(d+0);
        Q.setInternalData(d+3);
    }
    inline bool operator!= (const C7Vector& v)
    {
        return( (Q!=v.Q)||(X!=v.X) );
    }
    inline float& operator() (unsigned i)
    {
        if (i<3)
            return(X(i));
        else
            return(Q(i-3));
    }
    inline const float& operator() (unsigned i) const
    {
        if (i<3)
            return(X(i));
        else
            return(Q(i-3));
    }

    static const C7Vector identityTransformation;
    
    C4Vector Q;
    C3Vector X;
};

#pragma once

#include "mathDefines.h"
#include "3Vector.h"
#include "4Vector.h"
#include "6Vector.h"
#include "7Vector.h"

class CVector  
{
public:
    CVector();
    CVector(int nElements);
    CVector(const C3Vector& v);
    CVector(const C4Vector& v);
    CVector(const C6Vector& v);
    CVector(const C7Vector& v);
    CVector(const CVector& v);
    ~CVector();

    CVector operator* (float d) const;
    CVector operator/ (float d) const;
    CVector operator+ (const CVector& v) const;
    CVector operator- (const CVector& v) const;

    void operator*= (float d);
    void operator/= (float d);
    void operator+= (const CVector& v);
    void operator-= (const CVector& v);
    
    float operator* (const C3Vector& v) const;
    float operator* (const C4Vector& v) const;
    float operator* (const C6Vector& v) const;
    float operator* (const C7Vector& v) const;
    float operator* (const CVector& v) const;

    CVector& operator= (const C3Vector& v);
    CVector& operator= (const C4Vector& v);
    CVector& operator= (const C6Vector& v);
    CVector& operator= (const C7Vector& v);
    CVector& operator= (const CVector& v);

inline float& operator() (int i)
{
    return(data[i]);
}

inline const float& operator() (int i) const
{
    return(data[i]);
}

    int elements;
private:
    float* data;
};


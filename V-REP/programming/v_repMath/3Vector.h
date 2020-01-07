#pragma once

#include "mathDefines.h"

class C3X3Matrix;
class C4X4Matrix;
class C7Vector;

class C3Vector  
{
public:

    C3Vector();
    C3Vector(float v0,float v1,float v2);
    C3Vector(const float v[3]);
    C3Vector(const C3Vector& v);
    ~C3Vector();

    void buildInterpolation(const C3Vector& fromThis,const C3Vector& toThat,float t);
    float getAngle(const C3Vector& v) const;
    C3X3Matrix getProductWithStar() const;

    void operator*= (const C4X4Matrix& m);
    void operator*= (const C3X3Matrix& m);
    void operator*= (const C7Vector& transf);

    inline void getInternalData(float d[3]) const
    {
        d[0]=data[0];
        d[1]=data[1];
        d[2]=data[2];
    }
    inline void setInternalData(const float d[3])
    {
        data[0]=d[0];
        data[1]=d[1];
        data[2]=d[2];
    }
    inline float* ptr()
    {
        return(data);
    }
    inline bool isColinear(const C3Vector& v,float precision) const
    {
        float scalProdSq=(*this)*v;
        scalProdSq=scalProdSq*scalProdSq;
        float l1=(*this)*(*this);
        float l2=v*v;
        return((scalProdSq/(l1*l2))>=precision);
    }
    inline float& operator() (unsigned i)
    {
        return(data[i]);
    }
    inline const float& operator() (unsigned i) const
    {
        return(data[i]);
    }
    inline float getLength() const
    {
        return(sqrtf(data[0]*data[0]+data[1]*data[1]+data[2]*data[2]));
    }
    inline void copyTo(float v[3]) const
    {
        v[0]=data[0];
        v[1]=data[1];
        v[2]=data[2];
    }
    inline void set(const float v[3])
    {
        data[0]=v[0];
        data[1]=v[1];
        data[2]=v[2];
    }
    inline void get(float v[3]) const
    {
        v[0]=data[0];
        v[1]=data[1];
        v[2]=data[2];
    }
    inline C3Vector getNormalized() const
    {
        C3Vector retV;
        float l=sqrtf(data[0]*data[0]+data[1]*data[1]+data[2]*data[2]);
        if (l!=0.0f)
        {
            retV(0)=data[0]/l;
            retV(1)=data[1]/l;
            retV(2)=data[2]/l;
            return(retV);
        }
        return(C3Vector::zeroVector);
    }
    inline void keepMax(const C3Vector& v)
    {
        if (v(0)>data[0])
            data[0]=v(0);
        if (v(1)>data[1])
            data[1]=v(1);
        if (v(2)>data[2])
            data[2]=v(2);
    }
    inline void keepMin(const C3Vector& v)
    {
        if (v(0)<data[0])
            data[0]=v(0);
        if (v(1)<data[1])
            data[1]=v(1);
        if (v(2)<data[2])
            data[2]=v(2);
    }
    inline bool isValid() const
    {
        return((VREP_IS_FINITE(data[0])!=0)&&(VREP_IS_FINITE(data[1])!=0)&&(VREP_IS_FINITE(data[2])!=0)&&(VREP_IS_NAN(data[0])==0)&&(VREP_IS_NAN(data[1])==0)&&(VREP_IS_NAN(data[2])==0));
    }
    inline void set(float v0,float v1,float v2)
    {
        data[0]=v0;
        data[1]=v1;
        data[2]=v2;
    }
    inline void normalize()
    {
        float l=sqrtf(data[0]*data[0]+data[1]*data[1]+data[2]*data[2]);
        if (l!=0.0f)
        {
            data[0]=data[0]/l;
            data[1]=data[1]/l;
            data[2]=data[2]/l;
        }
    }
    inline void clear()
    {
        data[0]=0.0f;
        data[1]=0.0f;
        data[2]=0.0f;
    }
    inline C3Vector operator/ (float d) const
    {
        C3Vector retV;
        retV(0)=data[0]/d;
        retV(1)=data[1]/d;
        retV(2)=data[2]/d;
        return(retV);
    }
    inline void operator/= (float d)
    {
        data[0]/=d;
        data[1]/=d;
        data[2]/=d;
    }
    inline C3Vector operator* (float d) const
    {
        C3Vector retV;
        retV(0)=data[0]*d;
        retV(1)=data[1]*d;
        retV(2)=data[2]*d;
        return(retV);
    }
    inline void operator*= (float d)
    {
        data[0]*=d;
        data[1]*=d;
        data[2]*=d;
    }
    inline C3Vector& operator= (const C3Vector& v)
    {
        data[0]=v(0);
        data[1]=v(1);
        data[2]=v(2);
        return(*this);
    }
    inline bool operator!= (const C3Vector& v)
    {
        return( (data[0]!=v(0))||(data[1]!=v(1))||(data[2]!=v(2)) );
    }
    inline C3Vector operator+ (const C3Vector& v) const
    {
        C3Vector retV;
        retV(0)=data[0]+v(0);
        retV(1)=data[1]+v(1);
        retV(2)=data[2]+v(2);
        return(retV);
    }
    inline void operator+= (const C3Vector& v)
    {
        data[0]+=v(0);
        data[1]+=v(1);
        data[2]+=v(2);
    }
    inline C3Vector operator- (const C3Vector& v) const
    {
        C3Vector retV;
        retV(0)=data[0]-v(0);
        retV(1)=data[1]-v(1);
        retV(2)=data[2]-v(2);
        return(retV);
    }
    inline void operator-= (const C3Vector& v)
    {
        data[0]-=v(0);
        data[1]-=v(1);
        data[2]-=v(2);
    }
    inline C3Vector operator^ (const C3Vector& v) const
    { // Cross product
        C3Vector retV;
        retV(0)=data[1]*v(2)-data[2]*v(1);
        retV(1)=data[2]*v(0)-data[0]*v(2);
        retV(2)=data[0]*v(1)-data[1]*v(0);
        return(retV);
    }
    inline void operator^= (const C3Vector& v)
    { // Cross product
        C3Vector retV;
        retV(0)=data[1]*v(2)-data[2]*v(1);
        retV(1)=data[2]*v(0)-data[0]*v(2);
        retV(2)=data[0]*v(1)-data[1]*v(0);
        data[0]=retV(0);
        data[1]=retV(1);
        data[2]=retV(2);
    }
    inline float operator* (const C3Vector& v) const
    { // Scalar product
        return(data[0]*v.data[0]+data[1]*v.data[1]+data[2]*v.data[2]);
    }

    static const C3Vector oneOneOneVector;
    static const C3Vector unitXVector;
    static const C3Vector unitYVector;
    static const C3Vector unitZVector;
    static const C3Vector zeroVector;

    float data[3];
};





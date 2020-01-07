#pragma once

#include "mathDefines.h"
#include "3Vector.h"
#include "3X3Matrix.h"

class C4Vector  
{
public:
    C4Vector();
    C4Vector(float v0,float v1,float v2,float v3);
    C4Vector(const float v[4]);
    C4Vector(const C3Vector& v);
    C4Vector(const C4Vector& q);
    C4Vector(float a,float b,float g);
    C4Vector(float angle,const C3Vector& axis);
    C4Vector(const C3Vector& startV,const C3Vector& endV);
    ~C4Vector();

    void setEulerAngles(const C3Vector& v);
    void setEulerAngles(float a,float b,float g);
    void setAngleAndAxis(float angle,const C3Vector& axis);
    void setVectorMapping(const C3Vector& startV,const C3Vector& endV);
    void buildInterpolation(const C4Vector& fromThis,const C4Vector& toThat,float t);
    void buildInterpolation_otherWayRound(const C4Vector& fromThis,const C4Vector& toThat,float t);
    void buildRandomOrientation();

    float getAngleBetweenQuaternions(const C4Vector& q) const;
    C4Vector getAngleAndAxis() const;
    C4Vector getAngleAndAxisNoChecking() const;
    
    C3Vector getEulerAngles() const;

    inline void getInternalData(float d[4]) const
    {
        d[0]=data[0];
        d[1]=data[1];
        d[2]=data[2];
        d[3]=data[3];
    }
    inline void setInternalData(const float d[4])
    {
        data[0]=d[0];
        data[1]=d[1];
        data[2]=d[2];
        data[3]=d[3];
    }
    inline float& operator() (unsigned i)
    {
        return(data[i]);
    }
    inline const float& operator() (unsigned i) const
    {
        return(data[i]);
    }
    inline void normalize()
    {
        float l=sqrtf(data[0]*data[0]+data[1]*data[1]+data[2]*data[2]+data[3]*data[3]);
        data[0]/=l;
        data[1]/=l;
        data[2]/=l;
        data[3]/=l;
    }
    inline void clear()
    {
        data[0]=0.0f;
        data[1]=0.0f;
        data[2]=0.0f;
        data[3]=0.0f;
    }
    inline void setIdentity()
    {
        data[0]=1.0f;
        data[1]=0.0f;
        data[2]=0.0f;
        data[3]=0.0f;
    }
    inline C4Vector getInverse() const
    {
        return(C4Vector(data[0],-data[1],-data[2],-data[3]));
    }
    inline void inverse()
    {
        data[1]=-data[1];
        data[2]=-data[2];
        data[3]=-data[3];
    }
    inline C4Vector operator/ (float d) const
    {
        C4Vector retV;
        retV(0)=data[0]/d;
        retV(1)=data[1]/d;
        retV(2)=data[2]/d;
        retV(3)=data[3]/d;
        return(retV);
    }
    inline C4Vector operator* (float d) const
    {
        C4Vector retV;
        retV(0)=data[0]*d;
        retV(1)=data[1]*d;
        retV(2)=data[2]*d;
        retV(3)=data[3]*d;
        return(retV);
    }
    inline C4Vector& operator= (const C4Vector& v)
    {
        data[0]=v(0);
        data[1]=v(1);
        data[2]=v(2);
        data[3]=v(3);
        return(*this);
    }
    inline bool operator!= (const C4Vector& v)
    {
        return( (data[0]!=v(0))||(data[1]!=v(1))||(data[2]!=v(2))||(data[3]!=v(3)) );
    }
    inline C4Vector operator* (const C4Vector& v) const
    { // Quaternion multiplication.
        C4Vector retV;
        retV(0)=data[0]*v(0)-data[1]*v(1)-data[2]*v(2)-data[3]*v(3);
        retV(1)=data[0]*v(1)+v(0)*data[1]+data[2]*v(3)-data[3]*v(2);
        retV(2)=data[0]*v(2)+v(0)*data[2]+data[3]*v(1)-data[1]*v(3);
        retV(3)=data[0]*v(3)+v(0)*data[3]+data[1]*v(2)-data[2]*v(1);
        //  retV.normalize(); // NOOOOOOO!!!!!! We might compute the rotation of a vector which should be (q*v*qI).normalize and not q*((v*qi).normalize).normalize !!
        return(retV);
    }
    inline C3Vector getAxis(int index) const
    {
        C3X3Matrix m=getMatrix();
        return(m.axis[index]);
    }
    inline C3Vector operator* (const C3Vector& v) const
    { // Rotation of a vector.
        C4Vector tmpV(1.0f,v(0),v(1),v(2));
        tmpV=(*this)*(tmpV*getInverse());
        return(C3Vector(tmpV(1),tmpV(2),tmpV(3)));
    }
    inline C4Vector operator+ (const C4Vector& v) const
    {
        C4Vector retV;
        retV(0)=data[0]+v(0);
        retV(1)=data[1]+v(1);
        retV(2)=data[2]+v(2);
        retV(3)=data[3]+v(3);
        return(retV);
    }
    inline C3X3Matrix getMatrix() const
    {
        C3X3Matrix retM;
        float xx=data[1]*data[1];
        float xy=data[1]*data[2];
        float xz=data[1]*data[3];
        float xw=data[1]*data[0];
        float yy=data[2]*data[2];
        float yz=data[2]*data[3];
        float yw=data[2]*data[0];
        float zz=data[3]*data[3];
        float zw=data[3]*data[0];

        retM(0,0)=1.0f-2.0f*(yy+zz);
        retM(0,1)=2.0f*(xy-zw);
        retM(0,2)=2.0f*(xz+yw);
        retM(1,0)=2.0f*(xy+zw);
        retM(1,1)=1.0f-2.0f*(xx+zz);
        retM(1,2)=2.0f*(yz-xw);
        retM(2,0)=2.0f*(xz-yw);
        retM(2,1)=2.0f*(yz+xw);
        retM(2,2)=1.0f-2.0f*(xx+yy);
        return(retM);
    }
    inline void operator/= (float d)
    {
        data[0]/=d;
        data[1]/=d;
        data[2]/=d;
        data[3]/=d;
    }
    inline void operator*= (float d)
    {
        data[0]*=d;
        data[1]*=d;
        data[2]*=d;
        data[3]*=d;
    }
    inline void operator*= (const C4Vector& v)
    {
        (*this)=(*this)*v;
        // Already normalized through * operator
    }
    inline void operator+= (const C4Vector& v)
    {
        data[0]+=v(0);
        data[1]+=v(1);
        data[2]+=v(2);
        data[3]+=v(3);
    }

    static const C4Vector identityRotation;

    float data[4];
};

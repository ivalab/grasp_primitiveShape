#include "4Vector.h"
#include "MyMath.h"

C4Vector::C4Vector()
{
}

C4Vector::C4Vector(float v0,float v1,float v2,float v3)
{
    data[0]=v0;
    data[1]=v1;
    data[2]=v2;
    data[3]=v3;
    // We don't normalize here
}

C4Vector::C4Vector(const float v[4])
{
    data[0]=v[0];
    data[1]=v[1];
    data[2]=v[2];
    data[3]=v[3];
    // We don't normalize here
}

C4Vector::C4Vector(const C4Vector& q)
{
    data[0]=q(0);
    data[1]=q(1);
    data[2]=q(2);
    data[3]=q(3);
    // We don't normalize here
}

C4Vector::C4Vector(const C3Vector& v)
{ // Alpha, beta and gamma are in radians!
    setEulerAngles(v);
}

C4Vector::C4Vector(float a,float b,float g)
{ // Alpha, beta and gamma are in radians!
    setEulerAngles(a,b,g);
}

C4Vector::C4Vector(float angle,const C3Vector& axis)
{ // Builds a rotation quaternion around axis (angle in radian!)
    setAngleAndAxis(angle,axis);
}

C4Vector::C4Vector(const C3Vector& startV,const C3Vector& endV)
{
    setVectorMapping(startV,endV);
}

C4Vector::~C4Vector()
{

}

void C4Vector::setEulerAngles(float a,float b,float g)
{ // a,b anf g are in radian!
    C4Vector vx(a,C3Vector(1.0f,0.0f,0.0f));
    C4Vector vy(b,C3Vector(0.0f,1.0f,0.0f));
    C4Vector vz(g,C3Vector(0.0f,0.0f,1.0f));
    (*this)=vx*vy*vz;
}

void C4Vector::setEulerAngles(const C3Vector& v)
{ // v(0), v(1) and v(2) are in radian!
    setEulerAngles(v(0),v(1),v(2));
}

void C4Vector::setAngleAndAxis(float angle,const C3Vector& axis)
{ // angle in radian!
    C3Vector axisTmp=axis;
    axisTmp.normalize();
    float sinA=(float)sin(angle/2.0f);
    data[1]=axisTmp(0)*sinA;
    data[2]=axisTmp(1)*sinA;
    data[3]=axisTmp(2)*sinA;
    data[0]=(float)cos(angle/2.0f);
}

void C4Vector::setVectorMapping(const C3Vector& startV,const C3Vector& endV)
{
    C3Vector v0(startV.getNormalized());
    C3Vector v1(endV.getNormalized());
    C3Vector cross(v0^v1);
    float cosAngle=v0*v1;
    if (cosAngle>1.0f)
        setIdentity();
    else
        setAngleAndAxis(CMath::robustAcos(cosAngle),cross);
}

C4Vector C4Vector::getAngleAndAxis() const
{ // Returned vector is (angle,x,y,z) (angle is in radians)
    C4Vector retV;
    C4Vector d(*this);
    if (d(0)<0.0f)  // Condition added on 2009/02/26
        d=d*-1.0f;
    float l=sqrtf(d(0)*d(0)+d(1)*d(1)+d(2)*d(2)+d(3)*d(3));
    float cosA=d(0)/l; // Quaternion needs to be normalized
    if (cosA>1.0f) // Just make sure..
        cosA=1.0f;
    retV(0)=CMath::robustAcos(cosA)*2.0f;
    float sinA=sqrtf(1.0f-cosA*cosA); 
    if (fabs(sinA)<0.00005f)
        sinA=1.0f;
    else
        sinA*=l; // Quaternion needs to be normalized
    retV(1)=d(1)/sinA;
    retV(2)=d(2)/sinA;  
    retV(3)=d(3)/sinA;
    return(retV);
}

C4Vector C4Vector::getAngleAndAxisNoChecking() const
{ // Returned vector is (angle,x,y,z) (angle is in radians)
    C4Vector retV;
    C4Vector d(*this);
    if (d(0)<0.0f)  // Condition added on 2009/02/26
        d=d*-1.0f;
    float l=sqrtf(d(0)*d(0)+d(1)*d(1)+d(2)*d(2)+d(3)*d(3));
    float cosA=d(0)/l; // Quaternion needs to be normalized
    if (cosA>1.0f) // Just make sure..
        cosA=1.0f;
    retV(0)=acos(cosA)*2.0f;
    float sinA=sqrtf(1.0f-cosA*cosA); 
    if (fabs(sinA)<0.00005f)
        sinA=1.0f;
    else
        sinA*=l; // Quaternion needs to be normalized
    retV(1)=d(1)/sinA;
    retV(2)=d(2)/sinA;  
    retV(3)=d(3)/sinA;
    return(retV);
}


C3Vector C4Vector::getEulerAngles() const
{ // angles are in radians!
    return(getMatrix().getEulerAngles());
}


float C4Vector::getAngleBetweenQuaternions(const C4Vector& q) const
{
    float angle=fabs(data[0]*q(0)+data[1]*q(1)+data[2]*q(2)+data[3]*q(3));
    return(CMath::robustAcos(angle)*2.0f);
}

void C4Vector::buildInterpolation(const C4Vector& fromThis,const C4Vector& toThat,float t)
{
    C4Vector AA(fromThis);
    C4Vector BB(toThat);
    if (AA(0)*BB(0)+AA(1)*BB(1)+AA(2)*BB(2)+AA(3)*BB(3)<0.0f)
        AA=AA*-1.0f;
    C4Vector r((AA.getInverse()*BB).getAngleAndAxis());
    (*this)=(AA*C4Vector(r(0)*t,C3Vector(r(1),r(2),r(3))));
    // Already normalized through * operator
}

void C4Vector::buildInterpolation_otherWayRound(const C4Vector& fromThis,const C4Vector& toThat,float t)
{
    C4Vector AA(fromThis);
    C4Vector BB(toThat);
    if (AA(0)*BB(0)+AA(1)*BB(1)+AA(2)*BB(2)+AA(3)*BB(3)<0.0f)
        AA=AA*-1.0f;
    C4Vector r((AA.getInverse()*BB).getAngleAndAxis());

    // r(0) is the rotation angle
    // r(1),r(2),r(3) is the rotation axis
    // Here, since we want to rotate the other way round, we inverse the axis and rotate by 2*pi-r(0) instead:
    (*this)=(AA*C4Vector((piValTimes2_f-r(0))*t,C3Vector(r(1)*-1.0f,r(2)*-1.0f,r(3)*-1.0f)));
    // Already normalized through * operator
}

void C4Vector::buildRandomOrientation()
{
    C3Vector u(SIM_RAND_FLOAT,SIM_RAND_FLOAT,SIM_RAND_FLOAT);
    data[0]=sqrtf(1.0f-u(0))*(float)sin(piValTimes2*u(1));
    data[1]=sqrtf(1.0f-u(0))*(float)cos(piValTimes2*u(1));
    data[2]=sqrtf(u(0))*(float)sin(piValTimes2*u(2));
    data[3]=sqrtf(u(0))*(float)cos(piValTimes2*u(2));
}

const C4Vector C4Vector::identityRotation(1.0f,0.0f,0.0f,0.0f);

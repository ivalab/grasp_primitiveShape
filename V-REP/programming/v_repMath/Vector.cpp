#include "Vector.h"

CVector::CVector()
{
}

CVector::CVector(int nElements)
{
    data=new float[nElements];
    elements=nElements;
}

CVector::CVector(const C3Vector& v)
{
    data=new float[3];
    elements=3;
    (*this)=v;
}

CVector::CVector(const C4Vector& v)
{
    data=new float[4];
    elements=4;
    (*this)=v;
}

CVector::CVector(const C6Vector& v)
{
    data=new float[6];
    elements=6;
    (*this)=v;
}

CVector::CVector(const C7Vector& v)
{
    data=new float[7];
    elements=7;
    (*this)=v;
}

CVector::CVector(const CVector& v)
{
    data=new float[v.elements];
    elements=v.elements;
    (*this)=v;
}
 
CVector::~CVector()
{
   delete[] data;
} 

CVector& CVector::operator= (const C3Vector& v)
{
    for (int i=0;i<3;i++)
        data[i]=v(i);
    return(*this);
}

CVector& CVector::operator= (const C4Vector& v)
{
    for (int i=0;i<4;i++)
        data[i]=v(i);
    return(*this);
}

CVector& CVector::operator= (const C6Vector& v)
{
    for (int i=0;i<6;i++)
        data[i]=v(i);
    return(*this);
}

CVector& CVector::operator= (const C7Vector& v)
{
    for (int i=0;i<7;i++)
        data[i]=v(i);
    return(*this);
}

CVector& CVector::operator= (const CVector& v)
{
    for (int i=0;i<elements;i++)
        data[i]=v.data[i];
    return(*this);
}

CVector CVector::operator* (float d) const
{
    CVector retV(elements);
    for (int i=0;i<elements;i++)
        retV.data[i]=data[i]*d;
    return(retV);
}

CVector CVector::operator/ (float d) const
{
    CVector retV(elements);
    for (int i=0;i<elements;i++)
        retV.data[i]=data[i]/d;
    return(retV);
}

CVector CVector::operator+ (const CVector& v) const
{
    CVector retV(elements);
    for (int i=0;i<elements;i++)
        retV.data[i]=data[i]+v.data[i];
    return(retV);
}

CVector CVector::operator- (const CVector& v) const
{
    CVector retV(elements);
    for (int i=0;i<elements;i++)
        retV.data[i]=data[i]-v.data[i];
    return(retV);
}
    
float CVector::operator* (const C3Vector& v) const
{
    float retVal=0.0f;
    for (int i=0;i<3;i++)
        retVal+=(data[i]*v(i));
    return(retVal);
}

float CVector::operator* (const C4Vector& v) const
{
    float retVal=0.0f;
    for (int i=0;i<4;i++)
        retVal+=(data[i]*v(i));
    return(retVal);
}

float CVector::operator* (const C6Vector& v) const
{
    float retVal=0.0f;
    for (int i=0;i<6;i++)
        retVal+=(data[i]*v(i));
    return(retVal);
}

float CVector::operator* (const C7Vector& v) const
{
    float retVal=0.0f;
    for (int i=0;i<7;i++)
        retVal+=(data[i]*v(i));
    return(retVal);
}

float CVector::operator* (const CVector& v) const
{
    float retVal=0.0f;
    for (int i=0;i<elements;i++)
        retVal+=(data[i]*v.data[i]);
    return(retVal);
}

void CVector::operator*= (float d) 
{
    for (int i=0;i<elements;i++)
        data[i]*=d;
}

void CVector::operator/= (float d) 
{
    for (int i=0;i<elements;i++)
        data[i]/=d;
}

void CVector::operator+= (const CVector& v) 
{
    for (int i=0;i<elements;i++)
        data[i]+=v.data[i];
}

void CVector::operator-= (const CVector& v) 
{
    for (int i=0;i<elements;i++)
        data[i]-=v.data[i];
}

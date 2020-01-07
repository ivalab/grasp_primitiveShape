#include "MyMath.h"

CMath::CMath()
{
}

CMath::~CMath()
{
}

void CMath::limitValue(float minValue,float maxValue,float &value)
{
    if (value>maxValue)
        value=maxValue;
    if (value<minValue) 
        value=minValue;
}

void CMath::limitValue(int minValue,int maxValue,int &value)
{
    if (value>maxValue) 
        value=maxValue;
    if (value<minValue) 
        value=minValue;
}

float CMath::robustAsin(float v)
{
    if (!isFloatNumberOk(v))
    {
        // GENERATE AN ERROR MESSAGE HERE: IDSNOTR_NO_NUMBER_ERROR1
        return(0.0);
    }
    if (v>=1.0)
        return(piValD2_f);
    if (v<=-1.0)
        return(-piValD2_f);
    return(asinf(v));
}

float CMath::robustAcos(float v)
{
    if (!isFloatNumberOk(v))
    {
        // GENERATE AN ERROR MESSAGE HERE: IDSNOTR_NO_NUMBER_ERROR2
        return(0.0);
    }
    if (v>=1.0)
        return(0.0);
    if (v<=-1.0)
        return(piValue_f);
    return(acosf(v));
}

float CMath::robustFmod(float v,float w)
{
    if ( (!isFloatNumberOk(v))||(!isFloatNumberOk(w)) )
    {
        // GENERATE AN ERROR MESSAGE HERE: IDSNOTR_NO_NUMBER_ERROR3
        return(0.0);
    }
    if (w==0.0)
        return(0.0);
    return(fmod(v,w));
}

double CMath::robustmod(double v,double w)
{
    if ( (!isDoubleNumberOk(v))||(!isDoubleNumberOk(w)) )
    {
        // GENERATE AN ERROR MESSAGE HERE: IDSNOTR_NO_NUMBER_ERROR4
        return(0.0);
    }
    if (w==0.0)
        return(0.0);
    return(fmod(v,w));
}

bool CMath::isFloatNumberOk(float v)
{
    return ( (!VREP_IS_NAN(v))&&(fabs(v)!=std::numeric_limits<float>::infinity()) );    
}

bool CMath::isDoubleNumberOk(double v)
{
    return ( (!VREP_IS_NAN(v))&&(fabs(v)!=std::numeric_limits<double>::infinity()) );   
}

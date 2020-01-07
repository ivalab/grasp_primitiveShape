#pragma once

#include "mathDefines.h"
#include "4X4Matrix.h"
#include "3Vector.h"

class C4X4FullMatrix  
{
public:
    C4X4FullMatrix();   // Needed for serialization
    C4X4FullMatrix(const C4X4Matrix& m);
    C4X4FullMatrix(const C4X4FullMatrix& m);
    ~C4X4FullMatrix();

    void invert();
    void clear();
    void setIdentity();
    void buildZRotation(float angle);
    void buildTranslation(float x, float y, float z);
    C3Vector getEulerAngles() const;

    C4X4FullMatrix operator* (const C4X4FullMatrix& m) const;
    C4X4FullMatrix operator* (float d) const;
    C4X4FullMatrix operator/ (float d) const;
    C4X4FullMatrix operator+ (const C4X4FullMatrix& m) const;
    C4X4FullMatrix operator- (const C4X4FullMatrix& m) const;
    
    void operator*= (const C4X4FullMatrix& m);
    void operator+= (const C4X4FullMatrix& m);
    void operator-= (const C4X4FullMatrix& m);
    void operator*= (float d);
    void operator/= (float d);

    C4X4FullMatrix& operator= (const C4X4Matrix& m);
    C4X4FullMatrix& operator= (const C4X4FullMatrix& m);

    inline float& operator() (int row,int col)
    {
        return(data[row][col]);
    }
    inline const float& operator() (int row,int col) const
    {
        return(data[row][col]);
    }
        
private:
    float data[4][4];
};


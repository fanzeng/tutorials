#include <MathFunctions.h>

double mysqrt(double inputValue)
{
#if defined (HAVE_LOG) && defined (HAVE_EXP)
	return exp(log(x)*0.5);
	
#else
	return inputValue/2; // Test, divide by 2 so as to be different from sqrt
#endif
}

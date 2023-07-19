# floor-tracer

In 3D visualisation, clients provide drawings they’ve created as an architectural plan in mind.\
Their drawings have from a 3d modelerer perpective, among other things, imprecisions, unclosed shapes, duplicate or overlapping lines, etc...\
Those doesn’t matters to the architect.\
The 3d artist have to draw them from scratch, using the architect’s drawing as a reference.\
This script, generate needed shapes after correcting imprecisions.
- python 2.7
- no required libraries

Examples :
1. Openings have been closed with new spline.\
	![](/assets/e11.jpg)
	&rarr![](/assets/e12.jpg)
2. Imprecisions have been corrected.\
	![](/assets/e21.jpg)
	&rarr![](/assets/e22.jpg)
3. Related lines have been turned into geometric regions.\
	![](/assets/e31.jpg)
	&rarr![](/assets/e32.jpg)

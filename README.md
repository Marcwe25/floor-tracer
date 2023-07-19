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
	&#8594;![](/assets/e12.jpg)
2. Imprecisions have been corrected.\
	![](/assets/e21.jpg)
	&#8594;![](/assets/e22.jpg)
3. Related lines have been turned into geometric regions.\
	![](/assets/e31.jpg)
	&#8594;![](/assets/e32.jpg)

## current limitation:
	- result are z planar
	- curved spline are not supported,
	  also you can apply a normalize spline modifier or divide the curves.
	- window, door and other symbol must be hidden,
	  splines will be created for windows / doors by guessing walls openings.


## Usage
some parameters should be tweaked, among other max_wall_width, max_bridge_size (max opening width),...

Floor Tracer is written for 3ds Max 2018\
To launch the application:\
Update path to reflect path to directory \
3ds Max rollout \maxscript\floorTracer.ms 

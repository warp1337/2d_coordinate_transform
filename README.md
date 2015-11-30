What this does
===============

"In geometry, an affine transformation or affine map or an affinity 
(from the Latin, affinis, "connected with") between two vector spaces 
(strictly speaking, two affine spaces) consists of a linear transformation 
followed by a translation..."

[http://en.wikipedia.org/wiki/Affine_transformation]

You may use this code if you need to derive the transformation between
two 2 dimensional coordinate systems without including any 3rd party
library. This one is straight forward and uses native data types.
You just need to provide four sample points from each system.

In the example used in the code base we are transforming between 1024 * 768 
(origin) and 1280 * 1024 (target) [think of screen resolutions]. We derive the 
corresponding point in the target system, for a given point in the origin system.

# Copyright (c) 2015.
# Florian Lier <flier[at]techfak.uni-bielefeld.de>
#
# Released to public domain under terms of the BSD Simplified license.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the organization nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
#    See <http://www.opensource.org/licenses/bsd-license>

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# You may use this code if you need to derive the transformation between
# two 2 dimensional coordinate systems without including any 3rd party
# library. This one is straight forward and uses native data types.

# In the example below we are transforming between 1024 * 768 (origin) and
# 1280 * 1024 (target) [think of screen resolutions]. For a given point in the
# origin system [512, 384], we derive the corresponding point in the target system.

import sys

class AffineTransform:

    def __init__(self):

        # Target ---> The ones you want to map to
        self.target0 = [1.0, 1.0]
        self.target1 = [1.0, 1.0]
        self.target2 = [1.0, 1.0]
        self.target3 = [1.0, 1.0]

        # Origin ---> The ones that are mapped to [target0, target1, target2, target3]
        self.origin0 = [1.0, 1.0]
        self.origin1 = [1.0, 1.0]
        self.origin2 = [1.0, 1.0]
        self.origin3 = [1.0, 1.0]

        # Divider
        self.divider = 1.0

        # Calculated and mapped Coordinates
        mappedCoords = [1.0, 1.0]

        # Affine transformation coefficients
        self.An = 1.0
        self.Bn = 1.0
        self.Cn = 1.0
        self.Dn = 1.0
        self.En = 1.0
        self.Fn = 1.0

        # Test coord
        self.test = [1.0, 1.0]

        # Well, let's do this...
        self.set_coords()
        self.calculate_divider()
        self.derive_mapping_coords()

    def set_coords(self):
        # These are sample coords for mapping from 1024 * 786 up to 1280 * 1024

        # Upper left corner
        self.target0[0] = 0.0
        self.target0[1] = 0.0

        # Lower left corner
        self.target1[0] = 0.0
        self.target1[1] = 1024.0

        # Upper right corner
        self.target2[0] = 1280.0
        self.target2[1] = 0.0

        # Lower right corner
        self.target3[0] = 1280.0
        self.target3[1] = 1024.0

        # Sample Coords which are mapped to [t0,t1,t2,t3]

        # Upper left corner
        self.origin0[0] = 0.0
        self.origin0[1] = 0.0

        # Lower left corner
        self.origin1[0] = 0.0
        self.origin1[1] = 768.0

         # Upper right corner
        self.origin2[0] = 1024.0
        self.origin2[1] = 0.0

         # Lower right corner
        self.origin3[0] = 1024.0
        self.origin3[1] = 768.0

        # And finally the test coordinate
        self.test[0] = 512.0
        self.test[1] = 384.0

    def calculate_divider(self):
        result = ((self.origin0[0] - self.origin2[0]) * (self.origin1[1] - self.origin2[1])) - \
                 ((self.origin1[0] - self.origin2[0]) * (self.origin0[1] - self.origin2[1]))

        if result == 0.0:
            print(">> Divider is ZERO - Check your Coordinates?")
            sys.exit(1)
        else:
            self.divider = result
            print(">> Divider " + str(self.divider))
            self.calculateAn()
            self.calculateBn()
            self.calculateCn()
            self.calculateDn()
            self.calculateEn()
            self.calculateFn()

        return result

    def calculateAn(self):
        result = ((self.target0[0] - self.target2[0]) * (self.origin1[1] - self.origin2[1])) - \
                 ((self.target1[0] - self.target2[0]) * (self.origin0[1] - self.origin2[1]))
        self.An = result
        print(">> An " + str(self.An))
        return result

    def calculateBn(self):
        result = ((self.origin0[0] - self.origin2[0]) * (self.target1[0] - self.target2[0])) - \
                 ((self.target0[0] - self.target2[0]) * (self.origin1[0] - self.origin2[0]))
        self.Bn = result
        print(">> Bn " + str(self.Bn))
        return result

    def calculateCn(self):
        result = (self.origin2[0] * self.target1[0] - self.origin1[0] * self.target2[0]) * self.origin0[1] + \
                 (self.origin0[0] * self.target2[0] - self.origin2[0] * self.target0[0]) * self.origin1[1] + \
                 (self.origin1[0] * self.target0[0] - self.origin0[0] * self.target1[0]) * self.origin2[1]
        self.Cn = result
        print(">> Cn " + str(self.Cn))
        return result

    def calculateDn(self):
        result = ((self.target0[1] - self.target2[1]) * (self.origin1[1] - self.origin2[1])) - \
                 ((self.target1[1] - self.target2[1]) * (self.origin0[1] - self.origin2[1]))
        self.Dn = result
        print(">> Dn " + str(self.Dn))
        return result

    def calculateEn(self):
        result = ((self.origin0[0] - self.origin2[0]) * (self.target1[1] - self.target2[1])) - \
                 ((self.target0[1] - self.target2[1]) * (self.origin1[0] - self.origin2[0]))
        self.En = result
        print(">> En " + str(self.En))
        return result

    def calculateFn(self):
        result = (self.origin2[0] * self.target1[1] - self.origin1[0] * self.target2[1]) * self.origin0[1] + \
                 (self.origin0[0] * self.target2[1] - self.origin2[0] * self.target0[1]) * self.origin1[1] + \
                 (self.origin1[0] * self.target0[1] - self.origin0[0] * self.target1[1]) * self.origin2[1]
        self.Fn = result
        print(">> Fn " + str(self.Fn))
        return result

    # Use this method (test case)
    def derive_mapping_coords(self):
        # r->x = ((matrixPtr->An * ad->x) + (matrixPtr->Bn * ad->y) + matrixPtr->Cn) / matrixPtr->Divider
        # r->y = ((matrixPtr->Dn * ad->x) + (matrixPtr->En * ad->y) + matrixPtr->Fn) / matrixPtr->Divider
        if self.divider != 0.0:
            x = ((self.An * self.test[0]) + (self.Bn * self.test[1]) + self.Cn) / self.divider
            y = ((self.Dn * self.test[0]) + (self.En * self.test[1]) + self.Fn) / self.divider
            print "\n>> Test Point", self.test
            print ">> X was mapped to %s || Y was mapped to %s" % (str(x), str(y))


if __name__ == "__main__":
    at = AffineTransform()
"""
Name: Diego Torres-Ramos
Class: CSCI 3725

This program generates an image with a fractal-like
nature and is distorted, recolored and magnified dependeing
on the user's input (between 1 - 15) which will trigger a sequence of 
more integer/config. to dictate the overall attributes of the image.

Dependencies: numpy, random, Pillow
"""
import random as rand
import numpy as np
from PIL import Image

"""
setting the width, height and zoom of the image to be created
"""
IMGWIDTH, IMGHEIGHT, ZOOM = 1080,720, rand.randint(4, 10)
"""
setting up the variables according to the equation to create the pattern
"""
FRACTAL_CONSTANT_ONE, FRACTAL_CONSTANT_TWO = -0.7, 0.27015
MAX_ITERATIONS = 255

class DistortionPattern:
    """
    A class to represent a distorted and manipulated fractal pattern.
    ...

    Attributes
    ----------
    bitmap : PIL.Image
            image object responsible for certain configurations like the color
            space (RGB), height and width of image (pixels), and default background color.
    pixels : PixelAccess
            allocate the storage for the image and loading the pixel data to be
            modified in a 'pixels[x,y]' format.
    matrix : Dictionary
            table of keys (states) and probabilities to used to choose the next states using
            corresponding probabilities
    matrixNotes: List
            list of all the possible states to transition to.
    """

    def __init__(self, matrix) -> None:
        """
        Constructs the necessary attributes to generate the distorted pattern.
        ...

        Attributes
        ----------
        bitmap : PIL.Image
                image object responsible for certain configurations like the color
                space (RGB), height and width of image (pixels), and default background color.
        pixels : PixelAccess
                allocate the storage for the image and loading the pixel data to be
                modified in a 'pixels[x,y]' format.
        matrix : Dictionary
                table of keys (states) and probabilities to used to choose the next states using
                corresponding probabilities
        matrixNotes: List
                list of all the possible states to transition to.
        """
        self.bitmap = Image.new("RGB", (IMGWIDTH, IMGHEIGHT), "white")
        self.pixels = self.bitmap.load()
        self.matrix = matrix
        self.matrixNotes = list(matrix.keys())
    
    def generateRandomInteger( self, j: int, deviation: int ) -> int:
        """ 
        Generates and returns an integer value within a given range
        ...

        Parameters
        ----------
        j : int 
            is a parameter that serves as the center value in the range
            j - deviatation and j + deviation. 
        Deviation : int
            serves to modify the range in which the random number is generated.
        
        Returns
        -------
        integer within a given range
        """
        return rand.randint( j - deviation, j + deviation )
    
    def generateRandomDecimal( self, lowerBound: float, upperBound: float ) -> float:
        """
        randomly generates and returns a float within a given range
        ...

        Parameters
        ----------
        lowerBound : float
                the minimum possible value that can randomly be generated.
        upperBound : float
                the maximum possible value that can randomly be generated.

        Returns
        -------
        returns a float within a given range
        ...
        """
        return rand.uniform( lowerBound, upperBound )
    
    def getNextConfirguration( self, currentConfiguration : int ) -> int:
        """
        Helper function to the drawDistortion class. Serves to choose the next configuration (integer)
        based on the previous configuration. The chosen configuration is based on the fixed probability 
        in the matrix table.
        ...

        Parameters
        ----------
        currentConfiguration : int
                the current integer used for the most recent configuration to generate image, and influences
                the state of the next configuration.
        
        Returns
        -------
        returns an integer of the new configuration
        """
        return np.random.choice(
            self.matrixNotes,
            p=[self.matrix[currentConfiguration][nextConfirguration] for nextConfirguration in self.matrixNotes]
        )
    
    def messageToUser(self, starting : bool) -> None:
        """
        prints the message 'running' if the img is generating, and 
        'completed' in the img is done generating
        ...

        Parameters
        ----------
        starting : boolean
                indicates which of the two messages should be printed
        """
        if starting: print("Running...\n")
        else: print("...Completed")

    def locatePixelXCoordinate(self, widthIdx : int, transitionX : float) -> float:
        """
        locates and returns the x-coordinate of the current pixel
        ...

        Parameter:
        ----------
        widthIdx : int
                current idx in loaded pixel data

        Returns
        -------
        x-coordinate of the current pixel
        """
        return 1.5 * (widthIdx - IMGWIDTH/2) / (0.5*ZOOM*IMGWIDTH) + transitionX
        
    def locatePixelYCoordinate(self, heightIdx : int, transitionY : float) -> float:
        """
        locates and returns the y-coordinate of the current pixel
        ...

        Parameter:
        ----------
        heightIdx : int
                current idx in loaded pixel data

        Returns
        -------
        y-coordinate of the current pixel
        """
        return 1.0 * (heightIdx - IMGHEIGHT/2) / (0.5*ZOOM*IMGHEIGHT) + transitionY
    
    def drawDistortion(self, initialConfiguration : int) -> None:
        """
        Uses Markov Chain to generate a chain of values (dependent on previous values) to dictate
        the color scheme, distortion and magnitude of focus of a fractal pattern to produce an abstract, 
        obscure and vibrant image. We iterate and through each pixel to generate its assigned color.
        ...

        Parameters
        ----------
        initialConfiguration : int
                user input used for the first state/configuration used to generate image.
        """
        transitionX, transitionY = self.generateRandomDecimal(0.0, 0.3), self.generateRandomDecimal(0.0, 0.3)
        secondConfiguration = int(self.getNextConfirguration( initialConfiguration ))
        thirdConfiguration = int(self.getNextConfirguration( secondConfiguration ))
        self.messageToUser(True)

        for widthIdx in range(IMGWIDTH):
            for heightIdx in range(IMGHEIGHT):
                pixelX = self.locatePixelXCoordinate(widthIdx, transitionX)
                pixelY = self.locatePixelYCoordinate(heightIdx, transitionY)
                i = MAX_ITERATIONS
                while (pixelX * pixelX) + (pixelY * pixelY) < 4 and i > 1:
                    tmp = (pixelX * pixelX) - (pixelY * pixelY) + FRACTAL_CONSTANT_ONE
                    pixelY = (2.0 * pixelX * pixelY) + FRACTAL_CONSTANT_TWO
                    pixelX = tmp
                    i -= 1
                # convert byte to RGB (3 bytes)
                self.pixels[widthIdx,heightIdx] = (i << initialConfiguration) + (i << (secondConfiguration + 10)) + i * (thirdConfiguration + 5) 
    
        self.messageToUser(False)
        self.bitmap.show()

def main():
    """
    Driver function
    ...
    This function serves to request user input, create a DistortionPattern object using the premade probability table, and 
    calling the generate image function.
    """
    randomNumberInput = int(input("Select a random number between 1 and 15: ")) + 3
    if randomNumberInput <= 0 or 16 <= randomNumberInput:
        print("number not in range")
        return
    img = DistortionPattern({
        4 : {4: 0.05, 5: 0.0, 6: 0.0, 7: 0.05, 8: 0.25, 9: 0.05, 10: 0.05, 11: 0.25, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.05, 18: 0.0},
        5 : {4: 0.05, 5: 0.05, 6: 0.05, 7: 0.05, 8: 0.05, 9: 0.05, 10: 0.25, 11: 0.0, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.25, 16: 0.05, 17: 0.0, 18: 0.0},
        6 : {4: 0.05, 5: 0.0, 6: 0.05, 7: 0.05, 8: 0.05, 9: 0.25, 10: 0.25, 11: 0.05, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.0, 17: 0.05, 18: 0.0},
        7 : {4: 0.0, 5: 0.05, 6: 0.05, 7: 0.05, 8: 0.0, 9: 0.0, 10: 0.05, 11: 0.25, 12: 0.05, 13: 0.05, 14: 0.25, 15: 0.05, 16: 0.05, 17: 0.05, 18: 0.05},
        8 : {4: 0.05, 5: 0.0, 6: 0.05, 7: 0.05, 8: 0.25, 9: 0.0, 10: 0.05, 11: 0.05, 12: 0.05, 13: 0.25, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.05, 18: 0.0},
        9 : {4: 0.05, 5: 0.25, 6: 0.05, 7: 0.0, 8: 0.05, 9: 0.25, 10: 0.05, 11: 0.05, 12: 0.0, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.05, 18: 0.0},
        10 : {4: 0.05, 5: 0.0, 6: 0.25, 7: 0.0, 8: 0.05, 9: 0.05, 10: 0.05, 11: 0.25, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.0, 18: 0.05},
        11 : {4: 0.05, 5: 0.05, 6: 0.05, 7: 0.0, 8: 0.05, 9: 0.25, 10: 0.05, 11: 0.25, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.0, 17: 0.05, 18: 0.0},
        12 : {4: 0.25, 5: 0.05, 6: 0.0, 7: 0.05, 8: 0.05, 9: 0.05, 10: 0.05, 11: 0.05, 12: 0.25, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.0, 18: 0.0},
        13 : {4: 0.0, 5: 0.05, 6: 0.05, 7: 0.05, 8: 0.25, 9: 0.05, 10: 0.05, 11: 0.25, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.0, 18: 0.0},
        14 : {4: 0.05, 5: 0.05, 6: 0.0, 7: 0.0, 8: 0.05, 9: 0.05, 10: 0.05, 11: 0.25, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.25, 16: 0.05, 17: 0.05, 18: 0.0},
        15 : {4: 0.05, 5: 0.05, 6: 0.25, 7: 0.0, 8: 0.25, 9: 0.05, 10: 0.05, 11: 0.0, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.05, 18: 0.0},
        16 : {4: 0.05, 5: 0.0, 6: 0.05, 7: 0.0, 8: 0.25, 9: 0.05, 10: 0.05, 11: 0.05, 12: 0.05, 13: 0.25, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.05, 18: 0.0},
        17 : {4: 0.05, 5: 0.05, 6: 0.0, 7: 0.05, 8: 0.25, 9: 0.05, 10: 0.05, 11: 0.25, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.0, 17: 0.0, 18: 0.05},
        18 : {4: 0.05, 5: 0.0, 6: 0.0, 7: 0.05, 8: 0.25, 9: 0.05, 10: 0.05, 11: 0.05, 12: 0.05, 13: 0.05, 14: 0.05, 15: 0.05, 16: 0.05, 17: 0.25, 18: 0.0},
    })
    img.drawDistortion(randomNumberInput)

if __name__ == "__main__":
    main()
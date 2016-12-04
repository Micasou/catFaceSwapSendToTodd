#! /usr/bin/env python

import sys
import numpy as np
import cv2
import operator
from PIL import Image
from PIL import ImageDraw

def detectCatFace(imgPath):
    # load the input image and convert it to grayscale
    image =  cv2.imread(imgPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    # load the cat detector Haar cascade, then detect cat faces
    # in the input image
    detector = cv2.CascadeClassifier("frontcat_extended.xml")
    rects = detector.detectMultiScale(gray, scaleFactor=1.3,
    	minNeighbors=1, minSize=(5, 5))
    # loop over the cat faces and draw a rectangle surrounding each
    aList = []
    for (i, (x, y, w, h)) in enumerate(rects):
        #temp = x +","+ y +","+ w + "," + h 
        aList.append((x,y))
        aList.append((x,y+h))
        aList.append((x+w,y))
        aList.append((x+w,y+h))
        print x   #x point
        print y     #y point
        print h     #height form origin
        print w     #width from origin
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, "Cat #{}".format(i + 1), (x, y - 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    print aList
    # show the detected cat faces
    #cv2.imshow("Cat Faces" + imgPath, image)
    return aList
    
def detectHumanFaceRect(imgPath):
    # load the input image and convert it to grayscale
    image =  cv2.imread(imgPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    # load the cat detector Haar cascade, then detect cat faces
    # in the input image
    detector = cv2.CascadeClassifier("front_human_face.xml")
    rects = detector.detectMultiScale(gray, scaleFactor=1.3,
    	minNeighbors=1, minSize=(5, 5))
    # loop over the cat faces and draw a rectangle surrounding each
    aList = []
    for (i, (x, y, w, h)) in enumerate(rects):
        #temp = x +","+ y +","+ w + "," + h 
        aList.append((x,y))
        aList.append((x,y+h))
        aList.append((x+w,y))
        aList.append((x+w,y+h))
        print x   #x point
        print y     #y point
        print h     #height form origin
        print w     #width from origin
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, "human #{}".format(i + 1), (x, y - 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    print aList
    # show the detected cat faces
    #cv2.imshow("Human Faces" + imgPath, image)
    return aList
# Read points from text file
def readPoints(path) :
    # Create an array of points.
    points = [];
    
    # Read points
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))
    

    return points

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :
    
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Check if a point is inside a rectangle
def rectContains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[0] + rect[2] :
        return False
    elif point[1] > rect[1] + rect[3] :
        return False
    return True


#calculate delanauy triangle
def calculateDelaunayTriangles(rect, points):
    #create subdiv
    subdiv = cv2.Subdiv2D(rect);
    
    # Insert points into subdiv
    for p in points:
        subdiv.insert(p) 
    
    triangleList = subdiv.getTriangleList();
    
    delaunayTri = []
    
    pt = []    
    
    count= 0    
    
    for t in triangleList:        
        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))
        
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])        
        
        if rectContains(rect, pt1) and rectContains(rect, pt2) and rectContains(rect, pt3):
            count = count + 1 
            ind = []
            for j in xrange(0, 3):
                for k in xrange(0, len(points)):                    
                    if(abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                        ind.append(k)                            
            if len(ind) == 3:                                                
                delaunayTri.append((ind[0], ind[1], ind[2]))
        
        pt = []        
            
    
    return delaunayTri
        

# Warps and alpha blends triangular regions from img1 and img2 to img
def warpTriangle(img1, img2, t1, t2) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of the respective rectangles
    t1Rect = [] 
    t2Rect = []
    t2RectInt = []

    for i in xrange(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    #img2Rect = np.zeros((r2[3], r2[2]), dtype = img1Rect.dtype)
    
    size = (r2[2], r2[3])

    img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)
    
    img2Rect = img2Rect * mask

    # Copy triangular region of the rectangular patch to the output image
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( (1.0, 1.0, 1.0) - mask )
     
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Rect 
    
def swap(src1, src2, pointSet1, pointSet2):
    filename1 = src1
    filename2 = src2
    
    img1 = cv2.imread(filename1);
    img2 = cv2.imread(filename2);
    img1Warped = np.copy(img2);    
    
    # Read array of corresponding points
    points1 = pointSet1
    points2 = pointSet2    
    
    # Find convex hull
    hull1 = []
    hull2 = []

    hullIndex = cv2.convexHull(np.array(points2), returnPoints = False)
          
    for i in xrange(0, len(hullIndex)):
        hull1.append(points1[hullIndex[i]])
        hull2.append(points2[hullIndex[i]])
    
    
    # Find delanauy traingulation for convex hull points
    sizeImg2 = img2.shape    
    rect = (0, 0, sizeImg2[1], sizeImg2[0])
     
    dt = calculateDelaunayTriangles(rect, hull2)
    
    if len(dt) == 0:
        quit()
    
    # Apply affine transformation to Delaunay triangles
    for i in xrange(0, len(dt)):
        t1 = []
        t2 = []
        
        #get points for img1, img2 corresponding to the triangles
        for j in xrange(0, 3):
            t1.append(hull1[dt[i][j]])
            t2.append(hull2[dt[i][j]])
        
        warpTriangle(img1, img1Warped, t1, t2)
    
            
    # Calculate Mask
    hull8U = []
    for i in xrange(0, len(hull2)):
        hull8U.append((hull2[i][0], hull2[i][1]))
    
    mask = np.zeros(img2.shape, dtype = img2.dtype)  
    
    cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))
    
    r = cv2.boundingRect(np.float32([hull2]))    
    
    center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))
        
    
    # Clone seamlessly.
    output = cv2.seamlessClone(np.uint8(img1Warped), img2, mask, center, cv2.NORMAL_CLONE)
    
    cv2.imshow("Face Swapped" + filename1, output)
    
if __name__ == '__main__' :
    print "hey"
    # Make sure OpenCV is version 3.0 or above
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver) < 3 :
        print >>sys.stderr, 'ERROR: Script needs OpenCV 3.0 or higher'
        sys.exit(1)
    catFileName = "testcat5.jpg"
    catFileName2 = "testcat2.jpg"
    filename1 = 'testcat.jpg'
    filename2 = 'donald_trump.jpg'
    filename3 = 'ted_cruz.jpg'
    todd = 'todd.jpg'
    
    catbounds = detectCatFace(catFileName)
    todbounds = detectHumanFaceRect(todd)
    humanbounds = detectHumanFaceRect(filename3)
    swap(catFileName,filename3,catbounds,humanbounds)
    swap(todd,catFileName,todbounds,catbounds)
    swap(catFileName,todd,catbounds,todbounds)
    print catbounds
    print humanbounds
    #swap(filename3,filename1,filename2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
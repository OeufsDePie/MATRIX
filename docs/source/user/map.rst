****************
Map localization
****************

Once you have a workspace and a scene with your pictures, our application extract the GPS data from the exif data in the photos. If a photo doesn't have exif data, then the 
GPS default value will be 0.

Then you have two options : 

- If you switch off the map, then you will only see the renderer in the center of the screen once a reconstruction has been done.
- If you switch on the map, you will see some blue points on a map corresponding to the location where you take your pictures. If you click on a picture in the list, then the map will be centered on the point corresponding to this picture.

Points in the map can have different colors corresponding to their state :

- Blue : the picture is in state *New*
- Green : the picture is in state *Processed*
- Red : the picture is either in state *Rejected*, *Discarded* or *Thumbnail*



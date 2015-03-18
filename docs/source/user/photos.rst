=============================
Managing the photo selection
=============================

Once photos have been imported in your scene, you will be able to
manipulate them. But first, you have to know the different states a
photo can have. It can either be:

- Discarded : you don't the photo to be in the next reconstruction or
  the photo was in thumbnail state, but you don't want to download the
  real picture from the camera
- New : the photo had just been imported or the photo was in discarded
  state, but you changed your mind and you actually want to download
  it.
- Processed : the photo has been processed by the reconstruction
- Rejected : the photo couldn't be used by the reconstruction
  processed and was rejected by openMVG
- Thumbnails : the photo is not the actual photo but just a thumbnail
- Valid : the photo is either in the state *New* or *Processed* (all
  the files that will be used for the next reconstruction)
- Reconstruction : the photo is being used for the reconstruction

Note that only photos in *New* and *Processed* state will be used for
the next reconstruction.

Then, you can do a few things with them :

- You can manipulate them, sort them in any order you want.
- You can obviously select several photos by using *Ctrl* key or you
  can use the well known *Ctrl+Shift* key shortcut. Once a photo is
  selected, you can drag and drop it wherever you want.
- You can discard a photo, renew it (meaning it won't be discarded
  anymore), or you can delete it from the list.
- You can filter the picture list to display only photos in a specific
  state.


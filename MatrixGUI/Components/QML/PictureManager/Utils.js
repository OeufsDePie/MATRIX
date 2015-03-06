function iterateOnSelected(id, callback) {
  for(var i = 0; i < selectedPictures.model.count; i++) {
    if(selectedPictures.model.get(i).idSelected == id) {
      return callback(i);
    }
  }
  return false;
}

function unselect(id) {
  iterateOnSelected(id, function(i){
    selectedPictures.model.remove(i);
  });
}

function isSelected(id) {
  return iterateOnSelected(id, function(i){ return true; });
}

function selectedIndexes() {
  var indexes = [];
  for(var i = 0; i < selectedPictures.model.count; i++)
    indexes.push(selectedPictures.model.get(i).index);
  return indexes;
}

function togglePictureSelection(name, index){
  var removed = iterateOnSelected(name, function(i) {
    selectedPictures.model.remove(i);  
    return true;
  });
  if(!removed) {
    selectedPictures.model.append({"idSelected": name, "index": index});
  }
}
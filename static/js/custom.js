function setSelectedValue(value ,top) {
  var devices_nodes = JSON.parse(JSON.stringify( top ));
  if (value.length == 0) document.getElementById("node_selected").innerHTML = "<option></option>";
  else {
    var catOptions = "";
    for (node in devices_nodes[value]) {
        catOptions += "<option selected='selected'>" + devices_nodes[value][node] + "</option>";
    }
    document.getElementById("node_selected").innerHTML = catOptions;
  }
}




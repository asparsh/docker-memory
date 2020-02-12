// Before refreshing the page, save the form data to sessionStorage
window.onbeforeunload = function() {
  sessionStorage.setItem("device_selected", $('#device_selected').val());
  sessionStorage.setItem("node_selected", $('#node_selected').val());
}

$("#device_selected").change(function () {
  var prev_device = sessionStorage.getItem("device_selected");
  var prev_node = sessionStorage.getItem("node_selected");
  var device = $(this).val();
  var node = $("#node_selected").val();
  $.ajax({
    url: '/ajax/get_device/',
    cache: false,
    async : false, //must set async to false
    data: {
      'device': device,
      'node': node
    },
    dataType: 'json'
    })
    .done(function(data, textStatus, jqxhr){
        console.log(data.imageContent)
        if (prev_device != device || prev_node != node) {
          $('#timeseries').html(data.fileContent);
          // $('#sevendays').att
          $('#widget3').attr('src', 'data:image/jpeg;base64,'+data.imageContent);
        }
    })
    .fail(function(jqxhr, data, errorThrown){
        console.log(data)
        console.log(errorThrown);
    });
});

$("#node_selected").change(function () {
  var prev_device = sessionStorage.getItem("device_selected");
  var prev_node = sessionStorage.getItem("node_selected");
  var device = $("#device_selected").val();
  var node = $(this).val();
  $.ajax({
    url: '/ajax/getdevice_node/',
    data: {
      'device': device,
      'node': node
    },
    dataType: 'json'
    })
    .done(function(data, textStatus, jqxhr){
      console.log(data.fileContent)
      // alert(prev_device+" "+prev_node+" "+device+" "+node)
      if (prev_device != device || prev_node != node) {
        $('#timeseries').html(data.fileContent);
          // $('#sevendays').att
        $('#widget3').attr('src', 'data:image/jpeg;base64,'+data.imageContent);
      }
    })
    .fail(function(jqxhr, data, errorThrown){
        console.log(errorThrown);
    });
});

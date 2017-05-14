
// ************* FUNZIONI VARIE ***********************************************

// Funzione che carica le foto da Instagram via AJAX
function lastPhotos(){
    var access_token=(window.location.href).split("=")[1]
    $.ajax({
		    type: 'GET',
		    url: 'https://api.instagram.com/v1/users/self/media/recent/?access_token='+access_token+"&count=10&callback=?",
		    xhrFields: {
		        withCredentials: false
        },
		    crossDomain: true,
		    dataType: "jsonp",
		    
        }).done(function(res) {
            showPhotos(res);
		});
  
}

// Funzione che renderizza le foto ottenute tramite lastPhotos()
function showPhotos(res){
    console.log('res from Instagram API', res);
    for (i = 0; i<res.data.length; i++){
        
        newbox = $('#image').clone();
        
        newbox.attr('id', 'image-'+i);
        newbox.attr('style', 'position:relative; display:inline-block;')
        
        newimg = newbox.find("#img");
        newimg.attr('id','img-'+i);
        newimg.attr('src',res.data[i].images.thumbnail.url);
        newimg.attr('onclick', 'showModal("#img-'+i+'")');
        
        newtick = newbox.find("#tick");
        newtick.attr('id','tick-'+i);
                		        
        $("#photo-container").append(newbox);
    }
    $('#img').remove();
}


// Funzione che prepara il modal
function showModal(imgID){
    $('#image2crop').attr("src", $(imgID).attr("src") );
    $('#saveButton').attr("onclick", "selectPicture('"+imgID+"')" );
    $('#myModal').modal('show');
}

// Funzione che seleziona le immagini aperte al click di "Salva"
function selectPicture(imgID){
    id = imgID.split('-')[1];
    $('#tick-'+id).show();
    $('#image-'+id).attr('id', '#selected-image-'+id);
    
    $('#image-form').append('<input id="load-image-"'+i+' type="file" name="files[]" style="display:none;">');
    $('#load-image-'+i).val( $(this).find('#img-*').attr('src') );
    
    $('#myModal').modal('hide');
}

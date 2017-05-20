
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
        
        newfull = newbox.find("#max-res-img");
        newfull.attr('id','max-res-img-'+i);
        newfull.attr('href', res.data[i].images.standard_resolution.url);
                		        
        $("#photo-container").append(newbox);
    }
    $('#img').remove();
}


// Funzione che prepara il modal
function showModal(imgID){
    id = imgID.split('-')[1];
    $('#img2crop').attr("src", $('#max-res-img-'+id).attr("href") );
    $('#saveButton').attr("onclick", "selectPicture('"+imgID+"', window.cropper.getData() )" );
    $('#myModal').modal('show');
}


// Funzione che seleziona le immagini aperte al click di "Salva"
function selectPicture(imgID, obj){
    id = imgID.split('-')[1];
    
    // Imposta i dati del ritaglio sotto #image-* (che diventa poi #selected-image-*) 
    $('#image-'+id).data('x', obj.x);
    $('#image-'+id).data('y', obj.y);
    $('#image-'+id).data('w', obj.width);
    $('#image-'+id).data('h', obj.height);
    
    // Mostra il tick e cambia #image-* in selected-image-*
    $('#tick-'+id).show();
    $('#image-'+id).attr('id', 'selected-image-'+id);
    
    // Chiude forzatamente il modale
    $('#myModal').modal('hide');
}


// Funzione che prepara il form per essere inviato a /page3
function prepareForm() {
    
    // Calcola il numero di immagini di Instagram nella pagina
    images_number = $('[id*="image-"]').length;
    console.log(images_number);
    
    // Trova le immagini selezionate e appende i loro dati a un array
    selected_info = [];
    for (i=0; i<images_number; i++){
        if ($("#selected-image-"+i).length) { // Significa "se esiste #selected-image-i"
            
            data = $("#selected-image-"+i).data(); // Dati del ritaglio
            data.url =  $('#max-res-img-'+i).attr('href') ; // Url dell'immagine
            selected_info.push( data );
        }
    }
    // Converte in json, mette nel form e invia
    info = JSON.stringify( selected_info );
    $("#imageArray").val(info);
    $("#imageForm").submit();
}

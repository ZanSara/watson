
// Funzione che carica le foto da Instagram via AJAX
function loadPhotos(local){

    if(local){
        $.get( "/userPicture", function() {
        }).done(function(json_res) {
        
            res = JSON.parse(json_res);
            console.log("res from local: ", res);
            showPhotos(res);
            
        }).fail(function() {
            alert( "error" );
            
        });
        
    } else {

        var access_token=(window.location.href).split("=")[1]
        
        if (access_token == 'debug'){
            $.get( "/fake_login_service", function() {
            }).done(function(json_res) {
                res = JSON.parse(json_res);
                showPhotos(res.data);
                
            }).fail(function() {
                alert( "error" );
                
            });
        } else {
            $.ajax({
		            type: 'GET',
		            url: 'https://api.instagram.com/v1/users/self/media/recent/?access_token='+access_token+"&count=10&callback=?",
		            xhrFields: {
		                withCredentials: false
                },
		            crossDomain: true,
		            dataType: "jsonp",
		            
                }).done(function(res) {
                    showPhotos(res.data);
                    
		        }).fail(function(res) {
                    alert('Failed!');
		        }); 
        }
    }
}



// Funzione che renderizza le foto ottenute tramite lastPhotos()
function showPhotos(resdata){

    $("#pre-loader").show();
    $("#main-box").hide();
    $("#post-loader").hide(); // Who knows
    
    console.log('showPhotos received this RESDATA', resdata);
    
    for (i = 0; i<resdata.length; i++){
        
        newbox = $('#image').clone();
        
        newbox.attr('id', 'image-'+i);
        newbox.attr('style', 'position:relative; display:inline-block;')
        
        newimg = newbox.find("#img");
        newimg.attr('id','img-'+i);
        newimg.attr('src',resdata[i].images.thumbnail.url);
        newimg.attr('onclick', 'showModal("#img-'+i+'")');
        
        newtick = newbox.find("#tick");
        newtick.attr('id','tick-'+i);
        
        newfull = newbox.find("#max-res-img");
        newfull.attr('id','max-res-img-'+i);
        newfull.attr('href', resdata[i].images.standard_resolution.url);
        
        $("#photo-container").append(newbox);
    }
    $('#img').remove();
    
    $("#pre-loader").hide();
    $("#main-box").show();
    $("#post-loader").hide(); // Who knows
}

//Funzione che renderizza le immagini caricate dall' utente
function loadLocalPhotos(){
	
	
}

// Funzione che prepara il modal
function showModal(imgID){
    id = imgID.split('-')[1];
    $('#img2crop').attr("src", $('#max-res-img-'+id).attr("href") );
    $('#saveButton').attr("onclick", "selectPicture('"+imgID+"', window.cropper.getData(), window.cropper.getImageData() )" );
    $('#myModal').modal('show');
}




// Funzione che seleziona le immagini aperte al click di "Salva"
function selectPicture(imgID, obj, imageInfo){
    
    id = imgID.split('-')[1];
    image = $('#image-'+id);
    
    // Rimuove eventuali mask e crop rimasti
    $(image.selector).find(".mask").remove();
    $(image.selector).find(".crop").remove();
    
    // Mostra l'immagine ritagliata
    var x = (obj.x / imageInfo.naturalWidth)*100; 
    var y = (obj.y / imageInfo.naturalHeight)*100;
    var w = (obj.width / imageInfo.naturalWidth)*100;
    var h = (obj.height / imageInfo.naturalHeight)*100;
    
    var cx = x * (100 / (100 - w));
    var cy = y * (100 / (100 - h));
    
    // Imposta i dati del ritaglio sotto #img-*
    var img = $('#img-'+id)
    img.data('x', obj.x);
    img.data('y', obj.y);
    img.data('w', obj.width);
    img.data('h', obj.height);
    
    var img_url = img.attr('src');
    var inner = $(image.selector).find(".inner-img");
    console.log(id, img_url, inner);
    
    //$('#img-'+id).addClass('cropped');
    $(inner.selector).prepend( "<div class='crop' style='position: absolute; top:"+y+"%; left:"+x+"%; background-image: url("+img_url+"); background-position: left "+cx+"% top "+cy+"%; height: "+h+"%; width: "+w+"%;'></div>" );
    $(inner.selector).prepend( "<div class='mask' style='position: absolute; top:0; left:0; bottom:0; right:0; background-color:black; opacity:0.7;'></div>");
    
    // Mostra il tick e seleziona #image-*
    $('#tick-'+id).show();
    image.data('selected', 'yes');
    
    // Chiude forzatamente il modale
    $('#myModal').modal('hide');
}




// Funzione che, date le immagini tagliate, ottiene l'outfit con una AJAX.
function getOutfitData() {
    
    data =  JSON.stringify( collectSelected() );
    //console.log("stringify: ", data);
    if( data == "[]" ){
        $('#errorAlert').show();
        return;
    }
    
    $("#pre-loader").hide(); // Who knows
    $("#main-box").hide();
    $("#post-loader").show();
    
    $.get( "/service4page3", {'data':data}, function() {
    
        }).done(function(json_res) {
        
            $('#imageArray').val(json_res);
            $('#imageForm').submit();
            
        }).fail(function() {
            alert( "Error" );
            
        });

}



// Funzione che raccoglie le informazioni sulle foto selezionate
function collectSelected() {
    
    $('#errorAlert').hide();
    // Calcola il numero di immagini di Instagram nella pagina
    images_number = $('[id*="image-"]').length;
    
    // Trova le immagini selezionate e appende i loro dati a un array
    selected_info = [];
    for (id=0; id<images_number; id++){
        if ($("#image-"+id).data('selected') == 'yes' ){
            data = $("#img-"+id).data(); // Dati del ritaglio
            data.url =  $('#max-res-img-'+id).attr('href') ; // Url dell'immagine
            selected_info.push( data );
        }
    }
    console.log(images_number, selected_info.lenght);
    return selected_info;
}




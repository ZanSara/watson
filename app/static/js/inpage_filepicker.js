
function handleFiles()
{
    var filesToUpload = document.getElementById('input').file;
    var file = filesToUpload;

    // Create an image
    var img = document.createElement("img");
    // Create a file reader
    var reader = new FileReader();
    // Set the image once loaded into file reader
    reader.onload = function(e)
    {
        img.src = e.target.result;

        var canvas = document.createElement("canvas");
        //var canvas = $("<canvas>", {"id":"testing"})[0];
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);

        var MAX_WIDTH = 400;
        var MAX_HEIGHT = 300;
        var width = img.width;
        var height = img.height;

        if (width > height) {
          if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
          }
        } else {
          if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
          }
        }
        canvas.width = width;
        canvas.height = height;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);
       
        var imgData=ctx.getImageData(0, 0, width, height);
        document.getElementById('input').file = imgData;
        
    }
    // Load files into file reader
    reader.readAsDataURL(file);


    // Post the data
    /*
    var fd = new FormData();
    fd.append("name", "some_filename.jpg");
    fd.append("image", dataurl);
    fd.append("info", "lah_de_dah");
    */
}


var n=0;
(function ( $ ) {
	 
    $.fn.imagePicker = function( options ) {
        
        // Define plugin options
        var settings = $.extend({
            // Input name attribute
            name: "",
            // Classes for styling the input
            class: "form-control btn btn-default btn-block",
            // Icon which displays in center of input
            icon: "glyphicon glyphicon-plus"
        }, options );
        
        // Create an input inside each matched element
        return this.each(function() {
            $(this).html(create_btn(this, settings));
        });
 
    };
 
    // Private function for creating the input element
    function create_btn(that, settings) {
        // The input icon element
        var picker_btn_icon = $('<i class="'+settings.icon+'"></i>');
        
        // The actual file input which stays hidden
        var picker_btn_input = $('<input id="'+n+'" type="file" onchange="handleFiles()" name="'+settings.name+""+n+'" />');
        
        
        // The actual element displayed
        var picker_btn = $('<div class="'+settings.class+' img-upload-btn"></div>')
            .append(picker_btn_icon)
            .append(picker_btn_input);
            
        // File load listener
        picker_btn_input.change(function() {
            if ($(this).prop('files')[0]) {
                // Use FileReader to get file
                var reader = new FileReader();
                
                // Create a preview once image has loaded
                reader.onload = function(e) {
                    var preview = create_preview(that, e.target.result, settings );
                    
                    $(that).html(preview);
                	add();
                }
                
                // Load image
                reader.readAsDataURL(picker_btn_input.prop('files')[0]);
            }                
        });

        return picker_btn
    };
    
    // Private function for creating a preview element
    function create_preview(that, src, settings) {
        	
    	
            // The preview image
            var picker_preview_image = $('<img src="'+src+'" class="img-responsive img-rounded" />');
            
            // The remove image button
            var picker_preview_remove = $('<button class="btn btn-link"><small>Remove</small></button>');
            
            
            // The preview element
			
            var tetx = document.getElementById(String(n));
            tetx.className = "hidden";
            var picker_preview = $('<div class="text-center" id="container'+n+'"></div>')
           
                .append(picker_preview_image)
                .append(picker_preview_remove).append(tetx);
            // Remove image listener
			
             picker_preview_remove.click(function() {
                var btn = create_btn(that, settings);
                $(that).html(btn); 
            		//elementToRemove = document.getElementsByClassName("form-group col-lg-2 col-md-2 col-sm-3 col-xs-6 text-center")[n]
            		//elementToRemove = document.getElementById("container"+n);
            		//elementToRemove.outerHTML = "";
            		//delete elementToRemove;
            });
            
            return picker_preview;
    };
    
}( jQuery ));

$(document).ready(function() {
    $('.img-picker').imagePicker({name: 'images'});
})

function add(){
    n=n+1;
    if( n>1 ){
        document.getElementById("submitBtn").removeAttribute('disabled');
    } else {
        document.getElementById("submitBtn").setAttribute('disabled','disabled');
    }
	var node1 = document.createElement("div");
	var node2 = document.createElement("div");
	node1.type = "image"
    node1.className = "form-group col-lg-2 col-md-2 col-sm-3 col-xs-6";
    node2.className = "img-picker" + n;
    node1.appendChild(node2);
    document.getElementById("riga").appendChild(node1);
    $('.img-picker'+ n).imagePicker({name: 'images'});
}


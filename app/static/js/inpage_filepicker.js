
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
        var picker_btn_input = $('<input id="'+n+'" type="file" name="'+settings.name+""+n+'" />');
        
        
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
            var picker_preview = $('<div class="text-center"></div>')
           
                .append(picker_preview_image)
                .append(picker_preview_remove).append(tetx);
            // Remove image listener
			
             picker_preview_remove.click(function() {
                var btn = create_btn(that, settings);
                $(that).html(btn);
            });
            
            return picker_preview;
    };
    
}( jQuery ));

$(document).ready(function() {
    $('.img-picker').imagePicker({name: 'images'});
})

function add(){
    n=n+1;
    if( n>0 ){
        document.getElementById("submitBtn").removeAttribute('disabled');
    } else {
        document.getElementById("submitBtn").setAttribute('disabled','disabled');
    }
	var node1 = document.createElement("div");
	var node2 = document.createElement("div");
	node1.type = "image"
    node1.className = "form-group col-lg-2 col-md-2 col-sm-3 col-xs-6 text-center";
    node2.className = "img-picker" + n;
    node1.appendChild(node2);
    document.getElementById("riga").appendChild(node1);
    $('.img-picker'+ n).imagePicker({name: 'images'});
}


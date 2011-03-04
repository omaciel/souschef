$(document).ready( function() {
    var editor = CodeMirror.fromTextArea('id_body', {
        parserfile: "../contrib/python/js/parsepython.js",
        stylesheet: "/media/js/codemirror/contrib/python/css/pythoncolors.css",
        path: "/media/js/codemirror/js/",
        lineNumbers: true,
        textWrapping: false,
        indentUnit: 4,
        height: 100,
        width: "600px",
        tabMode: "spaces",
        parserConfig: {
            'pythonVersion': 2,
            'strictErrors': true
        }
    });

    $("#recipe_sync").click(function(){
        $( "#sync-confirm" ).dialog({
            resizable: false,
            height:140,
            modal: true,
            buttons: {
                "Sync": function() {
                    $( this ).dialog( "close" );
                    $( "#spinner" ).fadeIn();
                    $("#recipe_sync").fadeOut();
                    $("#sync_status").text('Syncing. Please wait.');
                    var build_label_form = $("#id_install_path").val()
                    $.post("/recipe_sync/", {
                        build_label: build_label_form
                    }, function(data){
                        if (data == "Error"){
                            $( "#spinner" ).fadeOut();
                            $("#recipe_sync").fadeIn();
                            $("#sync_status").html('<b>Sync error</b>');
                        }
                        else {
                            $( "#spinner" ).fadeOut();
                            $("#recipe_sync").fadeIn();
                            recipe_data = data;
                            editor.setCode(data)
                            $("#sync_status").html('<b>Sync success</b>');

                        }
                    });
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });

    });

});
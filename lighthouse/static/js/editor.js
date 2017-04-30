var editor = ''

$(function(){
    $('.editor').each(
        function() {
            id = $(this).attr('id')
            if(this.nodeName == "TEXTAREA") {
                editablediv = $('<div>').addClass('editor').addClass('form-control')
                                        .attr('id', 'editor-'+id)
                                        .insertAfter($(this))
                id = editablediv.attr('id')
            }
            editor = ace.edit(id);
            editor.setTheme("ace/theme/chrome");
            editor.session.setMode("ace/mode/yaml");
            editor.setAutoScrollEditorIntoView(true);
            editor.session.setOptions({ tabSize: 2, useSoftTabs: true });
            editor.setOption("maxLines", 30);
            editor.setOption("minLines", 10);
            if($(this).data('ro')) {
                editor.setOption("readOnly", true);
            }
            if(this.nodeName == "TEXTAREA") {
                self = $(this)
                editor.getSession().setValue(self.val())
                editor.getSession().on('change', function(){
                    self.val(editor.getSession().getValue())
                })
                self.hide()
            }
        }
    )
})

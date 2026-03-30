$(document).ready(function(){

    // Set automatic language direction of various elements
    // so English (etc) content will be left to right (ltr)
    // and Arabic (etc) will be right to left (rtl)
    $('input, textarea').attr('dir', 'auto');

    // After 1 second (enough time for ckeditor iframes to load)
    setTimeout(function(){
        // Set the direction of ckeditor text input p tags as auto,
        // so each paragraph in the textarea can be left or right depending on language
        $('.cke_wysiwyg_frame').each(function(){
            $(this).contents().find('p').attr('dir', 'auto');
        });
    }, 1000);

    // TODO
    // Move inlines to more appropriate place in the page
    // $('.inline-group').detach().insertBefore($('.field-admin_published').parent());

});
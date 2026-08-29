$(function() {
    function removeNote() {
        $(".remove-note").off('click').on('click', function(event) {
          event.stopPropagation();
          $(this).parents('.single-note-item').remove();
        })
    }

    function favouriteNote() {
        $(".favourite-note").off('click').on('click', function(event) {
          event.stopPropagation();
          $(this).parents('.single-note-item').toggleClass('note-favourite');

          fetch(`/important?idx=${event.target.dataset.idx}`)
          .then((res) => res.json())
          .then((res) => {
            if(res.result == "success"){
                location.href = "/"
            }
            else{
                alert(res.message)
            }
          })
        })
    }

    function addLabelGroups() {
        $('.category-selector .badge-group-item').off('click').on('click', function(event) {
          event.preventDefault();
          /* Act on the event */
          var getclass = this.className;
          var getSplitclass = getclass.split(' ')[0];
          if ($(this).hasClass('badge-business')) {
            $(this).parents('.single-note-item').removeClass('note-social');
            $(this).parents('.single-note-item').removeClass('note-important');
            $(this).parents('.single-note-item').toggleClass(getSplitclass);
          } else if ($(this).hasClass('badge-social')) {
            $(this).parents('.single-note-item').removeClass('note-business');
            $(this).parents('.single-note-item').removeClass('note-important');
            $(this).parents('.single-note-item').toggleClass(getSplitclass);
          } else if ($(this).hasClass('badge-important')) {
            $(this).parents('.single-note-item').removeClass('note-social');
            $(this).parents('.single-note-item').removeClass('note-business');
            $(this).parents('.single-note-item').toggleClass(getSplitclass);
          }
        });
    }

    var $btns = $('.note-link').click(function() {
        if (this.id == 'all-category') {
          var $el = $('.' + this.id).fadeIn();
          $('#note-full-container > div').not($el).hide();
        } if (this.id == 'important') {
          var $el = $('.' + this.id).fadeIn();
          $('#note-full-container > div').not($el).hide();
        } else {
          var $el = $('.' + this.id).fadeIn();
          $('#note-full-container > div').not($el).hide();
        }
        $btns.removeClass('active');
        $(this).addClass('active');  
    })

    $('#add-notes').on('click', function(event) {
        $('#addnotesmodal').modal('show');
        $('#btn-n-save').hide();
        $('#btn-n-add').show();
    })

    $(".preview").on("click", function() {
        let noteTitle = document.getElementById('note-has-title').value;
        let noteDescription = document.getElementById('note-has-description').value;

        window.open(
            `/preview?title=${noteTitle}&content=${noteDescription}`,
            '_blank'
          );
    })

    $('#addnotesmodal').on('hidden.bs.modal', function (event) {
        event.preventDefault();
        document.getElementById('note-has-title').value = '';
        document.getElementById('note-has-description').value = '';
    })

    removeNote();
    favouriteNote();
    addLabelGroups();

    $('#btn-n-add').attr('disabled', 'disabled'); 
})

 $('#note-has-title').keyup(function() {
      var empty = false;
      $('#note-has-title').each(function() {
          if ($(this).val() == '') {
                  empty = true;
          }
      });

      if (empty) {
          $('#btn-n-add').attr('disabled', 'disabled'); 
      } else {
          $('#btn-n-add').removeAttr('disabled');
      }
});
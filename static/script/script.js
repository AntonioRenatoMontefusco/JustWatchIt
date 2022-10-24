//select open/close
$(document).ready(function () {
    $('.select-btn-main').click(function () {
        $('.select-btn-option').slideToggle();
    });
    //add Select List
    $('.select-btn-option').on('click', 'button',
        function () {
            var item = $(this).parent('li');
            item.remove();
            $('#selectList').append(item);
            $('#selectList i').removeClass('fa-plus');
            $('#selectList i').addClass("fa-remove");
        });
    //remove Select List
    $('#selectList').on('click', 'button',
        function () {
            var list_item = $(this).parent('li');
            list_item.remove();
            $('.select-btn-option').append(list_item);
            $('.select-btn-option i').removeClass('fa-remove');
            $('.select-btn-option i').addClass("fa-plus");
        })

    $('#date_added').val((formatDate(new Date($('#date_added_hidden').val()))))

//platforms

    $('.select-btn-option-gen').on('click', 'button',
        function () {
            var item = $(this).parent('li');
            item.remove();
            $('#selectListGen').append(item);
            $('#selectListGen i').removeClass('fa-plus');
            $('#selectListGen i').addClass("fa-remove");
        });
    //remove Select List
    $('#selectListGen').on('click', 'button',
        function () {
            var list_item = $(this).parent('li');
            list_item.remove();
            $('.select-btn-option-gen').append(list_item);
            $('.select-btn-option-gen i').removeClass('fa-remove');
            $('.select-btn-option-gen i').addClass("fa-plus");
        })


    $('#submitButton').click(
        (event) => {
            event.preventDefault();

            let listItems = $('#selectList')[0].children;

            let newGenres = ""
            for (i in listItems) {

                newGenres += listItems[i].innerText === undefined ? '' : listItems[i].innerText + ','
            }

            $('#genresValue').val(newGenres.slice(0, newGenres.lastIndexOf(",")))


            let listItemsPla = $('#selectListGen')[0].children;

            let newPlat = ""
            for (i in listItemsPla) {

                newPlat += listItemsPla[i].innerText === undefined ? '' : listItemsPla[i].innerText + ','
            }

            $('#platformsValue').val(newPlat.slice(0, newPlat.lastIndexOf(",")))


            $("#theForm").submit();
        }
    )


    var genresValue = $("#genresValue").val();
    let values = genresValue.split(",").map(element => {
      return  element.trim().replaceAll(" ","");
    });

    for (i in values) {

        var item = $("#" + values[i]).parent('li');
        item.remove();
        $('#selectList').append(item);
        $('#selectList i').removeClass('fa-plus');
        $('#selectList i').addClass("fa-remove");
    }


    var platformsValue = $("#platformsValue").val();

    let valuesPla = platformsValue.split(",").map(element => {
      return element.trim().replaceAll(" ","");
    });

    for (j in valuesPla) {

        var item = $("#" + valuesPla[j]).parent('li');
        item.remove();
        $('#selectListGen').append(item);
        $('#selectListGen i').removeClass('fa-plus');
        $('#selectListGen i').addClass("fa-remove");
    }

    let elem = $('#ratingValue').val().trim();
    $('#rating').val(elem);

})

function formatDate(date) {
    var year = date.toLocaleString("default", {year: "numeric"});
    var month = date.toLocaleString("default", {month: "2-digit"});
    var day = date.toLocaleString("default", {day: "2-digit"});

// Generate yyyy-mm-dd date string
    var formattedDate = year + "-" + month + "-" +day ;
    return formattedDate;
}

function disableFields() {
    let elem = $('#typeIns').find(":selected").val();
    if(elem === "Movie"){
        $("#film_duration").prop('disabled', false);
        $("#number_of_seasons").prop('disabled', true);
    } else{
        $("#film_duration").prop('disabled', true);
        $("#number_of_seasons").prop('disabled', false);
    }

}

  
$(document).ready(function() {


    $('.pagination').click(
        (event) =>{
            let clicked = event.target.id;
            let curr_page = $('#page').val();
            let max_pages = $('#max_pages').val();

            if(clicked === "next" && ( 1 + parseInt(curr_page)) <= max_pages )
                $('#modifier').val("+1");
            else if(clicked === "prev" && (-1 + parseInt(curr_page)) >= 0)
                $('#modifier').val("-1");
            else{
                event.preventDefault();
            }

        }
    );
    
})


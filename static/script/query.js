$(document).ready(function() {


    $('.pagination').click(
        (event) =>{
            let clicked = event.target.id;
            let curr_page = $('#page').val();
            let max_pages = $('#max_pages').val();

            if(clicked === "next" && ( 1 + parseInt(curr_page)) <= max_pages )
                $('#modifier').val("+1");
            else if(clicked === "prev" && (-1 + parseInt(curr_page)) >= 1)
                $('#modifier').val("-1");
            else{
                event.preventDefault();
            }

        }
    );
    
    let list = $('.rating');

    for(let i in list ){
        let elem = list[i].innerText;

        switch(elem){

            case "0":
                list[i].innerText = "General"
                break;
              
                
            case "1":
                list[i].innerText = "Children Over 7"
                break;
              
                
            case "2":
                list[i].innerText = "Children Over 11"
                break;
              
                
            case "3":
                list[i].innerText = "Parental Guidance Under 13"
                break;
              
                
            case "4":
                list[i].innerText = "Children Over 16"
                break;
              
                
            case "5":
                list[i].innerText = "Parental Guidance Under 17"
                break;
              

            case "6":
                list[i].innerText = "Under 17 Not Admitted"
                break;    

            case "7":
                list[i].innerText = "Over 18"
                break;  


            case "8":
                list[i].innerText = "Not Rated"
                break;  

            }
    }
})


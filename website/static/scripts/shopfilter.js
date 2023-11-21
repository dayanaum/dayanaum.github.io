const className = document.getElementsByClassName("scontainer");
function shopFilter(selection){
    
    if(selection==='all'){
        visible();
                
    }
    else{
        genreSelect(selection);
    }
}

function visibleHelper(arr){
    for(let i = 0;i<arr.length;i++){
        arr[i].style.display="grid";
    }
}

function visible(){
    className[0].style.visibility = "visible";

    var action =  className[0].getElementsByClassName("Action");
    var adventure =  className[0].getElementsByClassName("Adventure");
    var comics =  className[0].getElementsByClassName("Comics");
    var fantasy =  className[0].getElementsByClassName("Fantasy");
    var fiction =  className[0].getElementsByClassName("Fiction");
    var nonfiction =  className[0].getElementsByClassName("Non-Fiction");


    visibleHelper(action);
    visibleHelper(adventure);
    visibleHelper(comics);
    visibleHelper(fantasy);
    visibleHelper(fiction);
    visibleHelper(nonfiction);

}

function invisible(arr){
    for(let i = 0;i<arr.length;i++){
        arr[i].style.display="none";
               
    }
}


function genreSelect(genre){

    var action =  className[0].getElementsByClassName("Action");
    var adventure =  className[0].getElementsByClassName("Adventure");
    var comics =  className[0].getElementsByClassName("Comics");
    var fantasy =  className[0].getElementsByClassName("Fantasy");
    var fiction =  className[0].getElementsByClassName("Fiction");
    var nonfiction =  className[0].getElementsByClassName("Non-Fiction");

    
    visible();

    switch(genre){
        case "Action":
            invisible(adventure);
            invisible(comics);
            invisible(fantasy);
            invisible(fiction);
            invisible(nonfiction);
            break;
        case "Adventure":
            invisible(action);
            invisible(comics);
            invisible(fantasy);
            invisible(fiction);
            invisible(nonfiction);
            break;
        case "Comics":
            invisible(adventure);
            invisible(action);
            invisible(fantasy);
            invisible(fiction);
            invisible(nonfiction);
            break;
        case "Fantasy":
            invisible(adventure);
            invisible(comics);
            invisible(action);
            invisible(fiction);
            invisible(nonfiction);
            break;
        case "Fiction":
            invisible(adventure);
            invisible(comics);
            invisible(fantasy);
            invisible(action);
            invisible(nonfiction);   
            break;
        case "Non-Fiction":
            invisible(adventure);
            invisible(comics);
            invisible(fantasy);
            invisible(fiction);
            invisible(action);    
            break;       

        default:
            visible();
    }



        
   

} 
        

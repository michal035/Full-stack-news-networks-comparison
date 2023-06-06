var div = document.getElementById("thediv")
var url = "http://127.0.0.1:8000/api/key_words"


async function getapi(url) {
    

    const response = await fetch(url);
    

    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show(data);
}

getapi(url);

function hideloader() {
    document.getElementById('loading').style.display = 'none';
}




function show(data) {
    var div = document.getElementById("thediv");
    var tab = ''


    for (let i = 0; i < data.length; i++) {
        tab += `<div class="col mb-5 h-100">
        
       <center>  <h2 class="h5">`+ data[i].headline +`</h2> <center> 
        <br>

        <table  style=" width: 80%; height: 60%;">
            <tr><td style=" border-right: 2px solid black; width: 50%; height: 50%;"><p class="mb-0">`  + data[i].first_cell + `</p></td><td style="border-left: 2px solid black; padding-left: 10%;"><p class="mb-0">`+ data[i].second_cell + `</p></td></tr>
        </table>

    </div> `;

    }
    


    div.innerHTML = tab;
    
}

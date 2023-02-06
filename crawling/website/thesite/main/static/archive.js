

var current_page =  window.location.href

var url = "http://127.0.0.1:8000/api/"+current_page.charAt(current_page.length - 2)+"/";
console.log(url);


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

    let tab = 
        ` <table class="table">
        <tthead>
        
            <tr  style="position: sticky; top: 0;background-color: white; padding: 10px;">
            <th scope="col" id="A"><style="font-weight: bold; ">TVN</center></th>
            <th scope="col" id="B"><center style="font-weight: bold; ">TVP</center></th>
            </tr>
        
        </thead>
        <tbody id="in">
            
        </tbody>
    </table>`;
    

    document.getElementById("theone").innerHTML = tab;
    tab =  '';
    

    var range = data[1].length;
    if (data[0].length > data[1].length){
        range = data[0].length 
    }
    

    for (let i = 0; i < range; i++) {
        if (data[0][i] == undefined){data[0][i] = " ";}
        else if (data[1][i] == undefined){data[1][i] = " ";}
        
        tab += '<tr> <td>'+data[0][i]+'</td><td>'+data[1][i]+'</td></tr>';
      }
    
    
  
    
    document.getElementById("in").innerHTML = tab;
    document.getElementById("theplace").innerHTML = '<center><div style="width: 40%;"><button id="thebtn" name="thebtN" value="nampage" class="btn btn-outline-primary" style="width: 100%;" >Load another month!</button></div></center>'
}



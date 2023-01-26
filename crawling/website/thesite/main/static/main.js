console.log("test");


const url = "http://127.0.0.1:8000/api/2/";


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
    var a = data
    let tab = 
        ` <table class="table">
        <tthead>
        
            <tr  style="position: sticky; top: 0;background-color: white; padding: 10px;">
            <th scope="col" id="A"><center>TVN</center></th>
            <th scope="col" id="B"><center>TVP</center></th>
            </tr>
        
        </thead>
        <tbody id="in">
            
        </tbody>
    </table>`;
    
    document.getElementById("theone").innerHTML = tab;
    tab =  '';
    // Loop to access all rows

    console.log(data.length)
    for (let i = 0; i < data[0].length; i++) {
        tab += '<tr> <td>'+data[0][i]+'</td><td>'+data[1][i]+'</td></tr>';
      }
    
    
  
    
    // Setting innerHTML as tab variable
    document.getElementById("in").innerHTML = tab;
}
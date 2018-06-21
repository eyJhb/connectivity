var readings = [
{%for reading in readings%}
  <tr>
    <td>{{reading[0]}}</td>
  </tr>   
{%endfor%}

];

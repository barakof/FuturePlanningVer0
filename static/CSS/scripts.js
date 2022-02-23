

// var tableNames = ['tInTable', 'tExpTable' ,'tSavTable','tLoanTable'];
// var tabName="";
// for (tabName of tableNames)
// {
//   var inTable=document.getElementById(tabName);
//   var inTableBody=inTable.children[1]
//   inTableBody.innerHTML="<tr></tr>"
//   var inTableFirstRawData=inTableBody.querySelector("tr")
//
//   for(i=0;i<20;i++)
//   {
//    inTableFirstRawData.innerHTML+="<td></td>"
//    var inTableRawDataTdsList=inTableFirstRawData.querySelectorAll("td")
//    inTableRawDataTdsList[inTableRawDataTdsList.length-1].textContent=tabName+i.toString()
//   }
//   inTableRawDataTdsList[0].textContent=""
// }
// var xValues = [50,60,70,80,90,100,110,120,130,140,150];
// var yValues = [7,8,8,9,9,9,10,11,14,14,15];
// // var yValues = {{gd}};
// new Chart("myChart", {
//   type: "line",
//   data: {
//     labels: xValues,
//     datasets: [{
//       fill: false,
//       lineTension: 0,
//       backgroundColor: "rgba(0,0,255,1.0)",
//       borderColor: "rgba(0,0,255,0.1)",
//       data: yValues
//     }]
//   },
//   options: {
//     legend: {display: false},
//     scales: {
//       yAxes: [{ticks: {min: 6, max:16}}],
//     }
//   }
//   });



  // var xArray = [50,60,70,80,90,100,110,120,130,140,150];
  // var yArray = [7,8,8,9,9,9,10,11,14,14,15];
  //
  // // Define Data
  // var data = [{
  //   x: xArray,
  //   y: yArray,
  //   mode:"lines"
  // }];
  //
  // // Define Layout
  // var layout = {
  //   xaxis: {range: [40, 160], title: "Square Meters"},
  //   yaxis: {range: [5, 16], title: "Price in Millions"},
  //   title: "House Prices vs. Size"
  // };
  //
  // // Display using Plotly
  // Plotly.newPlot("myPlot", data, layout);

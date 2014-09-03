var numApps = 2;


var xAxis = ["4:00","3:50","3:40","3:30","3:20","3:10","3:00",
             "2:50","2:40","2:30","2:20","2:10","2:00",
             "1:50","1:40","1:30","1:20","1:10","1:00",
             "0:50","0:40","0:30","0:20","0:10"];

var colors = [
    "rgba(212,238,94,0.9)",
    "rgba(255,66,66,0.9)",
    "rgba(78, 205, 196,1)"
]

var fetchData = function()
{
    // grab samples and split the string
    var temp = document.getElementById("samples").innerHTML.split(" ");

    var singleLen = temp.length / (numApps + 1);

    // reset label length if too few samples
    if (singleLen < xAxis.length)
    {
      for (var i = 0, j = 2; j < singleLen; i += 2, j += 2)
      {
          xAxis[i] = xAxis[j];
          xAxis[i + 1] = xAxis[j + 1];
      }

      xAxis.length = singleLen;
    }

    // the first array is for the total
    var ret = [[]];

    // create arrays for the apps
    for (var app = 0; app < numApps; ++app)
    { ret.push([]); }

    // store the values for each column
    for (var i = 0; i < temp.length;)
    {
	    ret[0].push(parseInt(temp[i++]));

	    for (var j = 1; j <= numApps; ++j)
	    { ret[j].push(parseInt(temp[i++])); }
    }

    return ret;
}

var samples = fetchData();

console.log("Fetched data successfully!");

var newChart = function(selector,colors,data)
{
    var item = $(selector);
    var wrapper = item.parent();

    var ctx = item.get(0).getContext("2d");

    // Set dimension to that of parent initially, the
    // library takes care of responsiveness after that
    item.attr('width', $(wrapper).width());
    item.attr('height', $(wrapper).height());

    var settings = {
        labels: xAxis,
        datasets: []
    };

    // append all datasets
    for (var i = 0; i < data.length; ++i)
    {
      settings.datasets.push({
                               fillColor: colors[i],
                               strokeColor: colors[i],
                               pointColor: colors[i],
                               pointStrokecolor : "#FFF",
                               pointHighlightFill: "#FFF",
                               pointHighlightStroke: "#FFF",
                               data : data[i]
                      });
    }

    return new Chart(ctx).Line(settings,{
	  pointDot : false,
	  animation: false,
    responsive: true,
    bezierCurve : false
    });

}

var draw = function()
{
    newChart("#overview-chart",[colors[0]],[samples[0]]);

    for (var app = 0; app < numApps; ++app)
    {
	    var id = "#app" + String.fromCharCode(65+app) + "-chart";
	    newChart(id,[colors[app+1]],[samples[app+1]]);
    }
}

draw();

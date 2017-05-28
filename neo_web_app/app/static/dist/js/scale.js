sortNumber = function(a,b) {
    return a - b;
}
sortCopy = function(arr) {
  return arr.slice(0).sort(sortNumber);
}
//takes a list of values and scales them based on low and high parameters
scaleScores = function(data, highvalue, lowvalue=0) {
   //default lowvalue is zero
   var d = sortCopy(data);
   //number of items
   itemNum = d.length;
   //max
   var max = d[d.length - 1];
   //min
   var min = d[0];

   //difference between min and max to scale
   var diff = max - min;
   var scale_diff = highvalue - lowvalue;

   scaled_data = [];
   for (z = 0; z < data.length; z++) {
      //for each item in data, return a scaled value between 0 and highvalue
      var scaled = (((data[z]-min)*scale_diff) / diff) + lowvalue;
      scaled_data.push(scaled);
            }
    return scaled_data;
    };

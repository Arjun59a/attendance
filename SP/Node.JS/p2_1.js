var arr = process.argv;
var len = arr.length

if (arr[len-1] == 'sum') {
    var sum = 0 ; 

    for (var i = 2 ; i < len - 1 ; i++)
    {
        sum += parseInt(arr[i])
    }

    console.log(sum)
}

else if (arr[len-1]== 'min')
    {
        var min = arr[2] ;

        for (var  i = 3 ; i < len -1 ; i++)
        {
            if (arr[i] < min) 
            {
                min = arr[i];
            }

        }
        console.log("The min value is "+min);
    } 

else if (arr[len-1] == 'avg')
{
    var sum = 0 ; 

    for (var i = 2 ; i < len - 1 ; i++)
    {
        sum += parseInt(arr[i])
    }

    var avg = sum / len

    console.log(avg);


}
else if (arr[len-1] == 'max')
{
    var max = arr[2];

    for (var i = 3 ; i < len - 1 ; i++)
    {
        if (arr[i] > max) 
        {
            max = arr[i];
        }
    }

    console.log("The maximum element is "+max)
}


else 
{

    console.log("Your choice is Wrong");
}

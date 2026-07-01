function sum(arr)
{
    sum = 0

    for(var i = 0 ; i < arr.length ; i++)
    {
        sum += arr[i];
    }

    return sum
}

function sub(arr)
{
    sub = arr[0]

    for(var i = 0 ; i < arr.length;i++ )
    {
        sub -= arr[i];
    }

    return sub;
}

function mul(arr)
{
    mul = 1

    for (var i = 0 ; i < arr.length ; i++)
    {
        mul *= arr[i];
    }

    return mul
}

function div(arr) 
{
    div = 1
    for(var i = 0 ; i < arr.length ; i++)
{
    div = arr[i] / div;

} 

return div
   }


function pow(arr)
{
    pow1= arr[0]
    for (var i = 1 ; i < arr.length ; i++)
    {
        pow1 = arr[i] ** pow1
    }

    return pow1
}




module.exports = 
{
    sum,pow,div,mul,sub
}
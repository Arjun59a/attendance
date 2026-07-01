var arr = process.argv;
var m1 = require('./calc')
var m2 = require('./credit')

var len = arr.length
var operator = len - 1
var nums = []
 for(var i = 2 ; i < len -1 ; i++)
    {
        arr[i] = parseInt(arr[i])
        nums.push(arr[i])

    }

if (arr[operator ]== "sum") {
    console.log(m1.sum(nums))
}
else if (arr[operator]=="sub")
{
    console.log(m1.sub(nums))

}

else if(arr[operator]=="mul")
{
    console.log(m1.mul(nums))

}

else if(arr[operator] == "div")
{
    console.log(m1.div(nums))
}

else if (arr[operator] == "pow")
{
    console.log(m1.pow(nums))
}

else{
    console.log("Your choice is wrong bruuh")
}


console.log(m2.designerby)
var readline = require('readline')
var r1 = readline.createInterface(

    {
        input: process.stdin,
        output: process.stdout
    }
);

var arr = []

r1.question("Making a choice \n 1:ADD Task \n 2: Show Task ", function (ch) {
    if (ch == 1) {
        r1.question("enter the Task which you want to add :", function (task) {
            arr.push(task);
            r1.question("Enter the Task which you want to add : ",
                function (task) {
                    arr.push(task);

                    r1.question("Making a choice \n 1:ADD Task \n 2: Show Task", function (ch) {
                        if (ch == 2) {
                            console.log(arr[0])
                            console.log(arr[1])
                            r1.close();
                        }
                    })



                }
            )


        })
    }





})
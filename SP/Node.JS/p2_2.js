var readline =require('readline')
var r1 = readline.createInterface(

    {
        input: process.stdin,
        output: process.stdout
    }
);

var arr = []
var count = -1

r1.question("1: for the add task \n 2 : for the showing task\n", function (ch) {
    if (ch == 1) {
        r1.question("Enter What ever task you want to add\n", function (task) {
            console.log("Your Task is added temprory\n")
            count += 1
            arr.push(task);
            r1.question("1: for the add task \n 2 : for the showing task\n", function (ch) {
                if (ch == 1) {
                    r1.question("Enter the What ever Task you want to add\n", function (task) {
                        console.log("Your task is temporory\n")
                        count += 1
                        arr.push(task)

                        r1.question("1: for the add task \n 2 : for the showing task\n", function (ch) {
                            if (ch == 1) {
                                r1.question("Enter the Task what ever you want to add :\n", function (task) {
                                    console.log("Your Task havebeen added temprory\n")
                                    count += 1
                                    arr.push(task)

                                });

                            }
                            else {
                                if (count > -1) {
                                    console.log(arr[count])
                                    count -= 1

                                    if (count > -1) {
                                        console.log(arr[count])
                                        count -= 1
                                        if (count > -1) {
                                            console.log(arr[count])
                                            count -= 1
                                        }
                                    }


                                }
                                r1.close()
                            }

                            if (ch == 1) {
                                console.log("Np further task is adding ok so showing the task !!!!\n")
                                if (count > -1) {
                                    console.log(arr[count])
                                    count -= 1

                                    if (count > -1) {
                                        console.log(arr[count])
                                        count -= 1
                                        if (count > -1) {
                                            console.log(arr[count])
                                            count -= 1
                                        }
                                    }
                                    r1.close()

                                }
                            }
                        });
                    })

                }

                else {
                    console.log(arr[count]);

                    r1.close();


                }
            });
        });
    }
    else {
        if (arr.length == 0) {
            console.log("You havent any task yer Sorry\n")
            r1.close()
        }
    }

});





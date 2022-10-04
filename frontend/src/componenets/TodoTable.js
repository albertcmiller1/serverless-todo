import React, { useState, useEffect } from 'react';
import { Button, Spinner } from 'reactstrap';

function TodoTable(props) {
    const URL = "https://xgrmbxql1h.execute-api.us-east-1.amazonaws.com/Prod"
    const [todoArr, setTodoArr] = useState(false)
    // const [todoArr, setTodoArr] = useState([{
    //     productId: "009",
    //     name: "fuck"
    // }])
    
    useEffect(() => {
        getTodos()
    },[]);
    
    const getTodos = () => {
        try {
            fetch(URL + "/products")
                .then(res => res.json())
                .then(json => {
                    console.log("found these items: ")
                    console.log(json.products.Items)
                    setTodoArr(json.products.Items)
                    console.log("todoArr: ")
                    console.log(todoArr)
                })
                .then(() => console.log())
                .catch(err => console.log(err))

        } catch (e){
            console.log("found this error:", e)
        }
    }

    if (todoArr){
        return (
            <div>
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Product Id</th>
                            <th scope="col">Product</th>
                            <th scope="col">Handle</th>
                        </tr>
                    </thead>
                    <tbody>
                        {todoArr.map(todo => 
                            <tr key={todo.productId}> 
                                <th scope="row">1</th>
                                <td>{todo.productId}</td>
                                <td>{todo.name}</td>
                                <td><Button color="danger">Danger!</Button></td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        )
    } else {
        return <Spinner color='primary' />
    }
}

export default TodoTable
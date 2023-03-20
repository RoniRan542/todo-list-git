const getCredentials = async (email, password) => {
    const resp = await fetch(`login`, { 
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, password: password }) 
     })

     if(!resp.ok) throw Error("There was a problem in the login request")

     if(resp.status === 401){
          throw("Invalid credentials")
     }
     else if(resp.status === 400){
          throw ("Invalid email or password format")
     }
     const data = await resp.json()
     
     localStorage.setItem("jwt-token", data.access_token);
     localStorage.setItem("user_id", data.id);
     localStorage.setItem("user_name", data.name);
     console.log(data);

     loginResponse(data.name, data.id);
     }

const loginResponse = (name, id) => {
     window.location.href = `todo_list/${id}`;
}

const logout = () => {
  localStorage.removeItem('jwt-token');
  localStorage.removeItem('user');
  window.location.href = '/';
}

const addTask = async (title, description) => {
     // retrieve token and id form localStorage
     const id = localStorage.getItem('user_id');
     const token = localStorage.getItem('jwt-token');

     const resp = await fetch(`/add_task/${id}`, {
        method: 'POST',
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` // ⬅⬅⬅ authorization token
        },
        body: JSON.stringify({ name: title, description: description })  
     })
     if(!resp.ok) throw Error("There was a problem in the login request")

     else if(resp.status === 403){
         throw Error("Missing or invalid token");
     }
    
     console.log("task added successfully");
     window.location.reload();
}

const deleteTask = async (task) => {
     // retrieve token and id form localStorage
     const id = localStorage.getItem('user_id');
     const token = localStorage.getItem('jwt-token');

     const resp = await fetch(`/delete_task/${id}?task_id=${task.id}`, {
        method: 'DELETE',
        headers: { 
          "Content-Type": "application/text",
          "Authorization": `Bearer ${token}` // ⬅⬅⬅ authorization token
        }
     })
     if(!resp.ok) throw Error("There was a problem in the login request")

     else if(resp.status === 403){
         throw Error("Missing or invalid token");
     }
    
     console.log("task deleted successfully");
     window.location.reload();
}

const goRegister = () => {
     console.log("Registering redirect");
     fetch(`/register-page`, {
        method: 'GET',
        headers: { 
          "Content-Type": "application/text",
        }
     }).then(console.log('redirecting to registration...'))
}

const editTask = async(task, title, content) => {
     const id = localStorage.getItem('user_id');
     const token = localStorage.getItem('jwt-token');

     const resp = await fetch(`/edit_task/${id}?task_id=${task.id}`, {
        method: 'PUT',
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` // ⬅⬅⬅ authorization token
        },
        body: JSON.stringify({name: title, description: content })  
     })
     if(!resp.ok) throw Error("There was a problem in the login request")

     else if(resp.status === 403){
         throw Error("Missing or invalid token");
     }
    
     console.log("task edited successfully");
     // window.location.reload();
}
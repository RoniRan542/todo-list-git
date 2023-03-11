console.log("Working...");
const getCredentials = async (email, password) => {
    console.log("inside login " + email); 
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
     
     return data
}

const loginResponse = (name, id) => {
  const response = `
            <h2> You are logged in ${name}! </h2>
            <button class="btn btn-primary btn-lg btn-block" onclick="window.location.href = 'todo_list/${id}';"> Your todo-list </button>
            `;
  document.getElementById("form-container").innerHTML = response;
  
}

const logout = () => {
  localStorage.removeItem('jwt-token');
  localStorage.removeItem('user');
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
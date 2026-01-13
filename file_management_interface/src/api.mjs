//temporary token storage

let accessToken = null;

//modify when cookies implemented

function authHeaders() {
  const headers = {
    "Content-Type": "application/json"
  };

  if (accessToken) {
    headers["Authorization"] = `Bearer ${accessToken}`;
  }

  return headers;
}

export const API_URL = 'http://localhost:5000';

export async function getUsers() {
  return fetch(`${API_URL}/users/`, {
    method: "GET",
    headers: authHeaders()
  })
  .then(res => res.json())
  .then(data => {
    console.log("GET response:", data)
    return data
  })
  .catch(err => {
      console.error("GET error:", err);
      throw err;
    });
};

export async function getUser(mail) {
  return fetch(`${API_URL}/users/${mail}`, {
    method: "GET",
    headers: authHeaders()
  })
  .then(res => res.json())
  .then(data => {
    console.log("GET response:", data)
    return data
  })
  .catch(err => {
      console.error("GET error:", err);
      throw err;
    });
};

export async function addUser(first_name, last_name, email, password, user_type_id) {
  return fetch(`${API_URL}/users/`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ first_name, last_name, email, password, user_type_id })
  })
    .then(res => res.json())
    .then(data => {
      console.log("POST response:", data);
      return data;
    })
    .catch(err => {
      console.error("POST error:", err);
      throw err;
    });
};

export async function authUser(email, password){
  return fetch(`${API_URL}/auth/`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({email, password})
  })
  .then(res => res.json())
  .then(data => {
    console.log("POST response:", data);
    accessToken = data.access_token;
    return data;
  })
  .catch(err => {
    console.error("POST error:", err);
    throw err;
  })
}

async function main() {
  
  await authUser('admin@test.com', 'strongpassword');
  await addUser('Ann', 'smith', "ann@mail.com", "passwordtest1", 1);
  await addUser('Kate', 'Johnson', "kate@mail.com", "passwordtest2", 1);
  await addUser('Kristy', 'Albert', "kristy@mail.com", "passwordtest3", 1);
  await getUsers();
  await getUser('ann@mail.com');
  }

main();
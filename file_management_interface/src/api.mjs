import fetch from 'node-fetch'
export const API_URL = 'http://localhost:5000';

export async function addUser(name, email, pass) {
  return fetch(`${API_URL}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, pass })
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

export async function getUsers() {
  return fetch(`${API_URL}/users`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
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

export async function getUser(id) {
  console.log(`${API_URL}/users/${id}`)
  return fetch(`${API_URL}/users/${id}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
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

export async function delUser(email) {
  return fetch(`${API_URL}/users`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  })
  .then(res => res.json())
  .then(data => {
    console.log("DELETE response:", data)
    return data
  })
  .catch(err => {
      console.error("DELETE error:", err);
      throw err;
    });
}

async function main() {
  await addUser('Ann', "ann@mail.com", "passwordtest1");
  await addUser('Kate', "kate@mail.com", "passwordtest2");
  await getUsers();
  await getUser(1);
  /*
  await delUser("ann@mail.com");
  await delUser("kate@mail.com");
  */
  }

main();
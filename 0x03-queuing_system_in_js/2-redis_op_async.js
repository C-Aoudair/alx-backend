import { createClient, print } from "redis";

const client = createClient();

client.on("error", (err) => {
  console.error("Redis client not connected to the server: ", err);
});

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

async function redisOperations() {
  await client.connect();

  await displaySchoolValue("Holberton");
  await setNewSchool("HolbertonSanFrancisco", "100");
  await displaySchoolValue("HolbertonSanFrancisco");

  client.disconnect();
}

async function setNewSchool(schoolName, value) {
  return client
    .set(schoolName, value)
    .then((reply) => console.log(`Reply: ${reply}`))
    .catch((error) => console.log(error));
}

async function displaySchoolValue(schoolName) {
  return client
    .get(schoolName)
    .then((value) => console.log(value))
    .catch((error) => console.log(error));
}

redisOperations();

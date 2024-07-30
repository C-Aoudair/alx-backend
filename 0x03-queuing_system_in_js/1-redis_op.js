import { createClient, print } from 'redis';

const client = createClient();

client.on('error', (err) => {
  console.error("Redis client not connected to the server: ", err);
});

client.on('connect', () => {
  console.log("Redis client connected to the server");
});

async function redisConnect() {
  try {
    await client.connect();
    
    await displaySchoolValue('Holberton');
    await setNewSchool('HolbertonSanFrancisco', '100');
    await displaySchoolValue('HolbertonSanFrancisco');

  } catch (error) {
    console.error("An error occurred:", error);
  }
}

async function setNewSchool(schoolName, value) {
  const setResult = await client.set(schoolName, value);
  console.log(`Reply: ${setResult}`);
}

async function displaySchoolValue(schoolName) {
  const value = await client.get(schoolName);
  console.log(value);
}

redisConnect();

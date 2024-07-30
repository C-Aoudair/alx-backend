import { createClient } from "redis";

async function redisConnect() {
  try {
    const client = createClient();
    client.on('error', (err) => {
      console.log("Redis client not connected to the server: ", err);
    });
    await client.connect();

    console.log("Redis client connected to the server");
    await client.disconnect();
  } catch (error) {
    console.log("An error occurs");
  }
}

redisConnect();

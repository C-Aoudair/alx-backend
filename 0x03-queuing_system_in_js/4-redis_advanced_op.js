import { createClient, print } from "redis";

const client = createClient();

const props = {
  Portland: 50,
  Seattle: 80,
  "New York": 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

for (const [key, value] of Object.entries(props)) {
  console.log(key, value);
  client.hset("HolbertonSchools", key, value, (err, res) => {
    if (err) console.log(err);
    else print(`Reply: ${res}`);
  });
}

client.hgetall("HolbertonSchools", (err, res) => {
  if (err) console.log(err);
  else console.log(res);
});

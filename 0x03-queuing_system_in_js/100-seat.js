import { createClient } from "redis";
import express from "express";
import kue from "kue";
import { promisify } from "util";

const client = createClient();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

function reserveSeat(number) {
  return setAsync(`available_seats`, number)
    .then(() => {
      client.publish("available_seats", number);
    })
    .catch((err) => {
      console.log("Error: an error occurred while reserving the seat");
    });
}

function getCurrentAvailableSeats() {
  return getAsync(`available_seats`);
}

let reservationEnabled = true;

const subscriber = createClient();
subscriber.subscribe("available_seats");
subscriber.on("message", async (channel, message) => {
  reservationEnabled = message !== "0";
});

const queue = kue.createQueue();

const app = express();

app.use(express.json());

app.get("/available_seats", async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get("/reserve_seat", async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: "Reservation are blocked" });
  }

  const job = queue.create("reserve_seat", {});

  job.save((error) => {
    if (error) {
      return res.json({ status: "Reservation failed" });
    }
  });

  job.on("complete", () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });
  job.on("failed", (err) => {
    console.log(`Seat reservation job ${job.id} failed` + err);
  });
  res.json({ status: "Reservation in process" });
});

app.get("/process", async (req, res) => {
  queue.process("reserve_seat", async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats === "0") {
      done(new Error("Not enough seats available"));
    } else {
      await reserveSeat(parseInt(availableSeats, 10) - 1);
      done();
    }
  });
  res.json({ status: "Queue processing" });
});

app.listen(1245, () => {
  reserveSeat(50);
  console.log("API server is running on port 1245");
});

import kue from "kue";

const processQueue = kue.createQueue();
const blackList = ["4153518780", "4153518781"];

processQueue.process("push_notification_code_2", 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});

function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100);
  if (blackList.includes(phoneNumber)) {
    return done(Error(`Phone number ${phoneNumber} is blacklisted`));
  } else {
    job.progress(50, 100);
    console.log(
      `Sending notification to ${phoneNumber}, with message: ${message}`,
    );
  }
  done();
}

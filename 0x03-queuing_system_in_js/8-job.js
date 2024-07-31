export default function createPushNotification(jobs, queue) {
  if (!(jobs instanceof Array)) {
    throw Error("Jobs is not an array");
  }

  jobs.forEach((jobData) => {
    const job = queue.createJob("push_notification_code_3", jobData);
    job.save((err) => {
      if (!err) {
        console.log(`Notification job created: ${job.id}`);
      }
    });
    job.on("complete", () => {
      console.log(`Notification job ${job.id} completed`);
    });
    job.on("failed", (err) => {
      console.log(`Notification job ${job.id} failed: ${err}`);
    });
    job.on("progress", (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  });
}

import kue from 'kue';
import { expect } from 'chai';
import sinon from 'sinon';
import createPushNotification from './8-job.js';

const queue = kue.createQueue();

queue.testMode.enter();

describe('createPushNotification', () => {
  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotification({}, queue)).to.throw('Jobs is not an array');
    expect(() => createPushNotification(null, queue)).to.throw('Jobs is not an array');
  });

  it('should create jobs when provided with an array of job data', () => {
    const jobs = [
      { phoneNumber: '1234567890', message: 'Test message 1' },
      { phoneNumber: '0987654321', message: 'Test message 2' }
    ];

    createPushNotification(jobs, queue);

    const createdJobs = queue.testMode.jobs;
    expect(createdJobs.length).to.equal(2);
    expect(createdJobs[0].type).to.equal('push_notification_code_3');
    expect(createdJobs[0].data).to.deep.equal(jobs[0]);
    expect(createdJobs[1].data).to.deep.equal(jobs[1]);
  });

  it('should set up complete, failed, and progress listeners for each job', () => {
    const jobs = [{ phoneNumber: '1234567890', message: 'Test message' }];
    const consoleSpy = sinon.spy(console, 'log');

    createPushNotification(jobs, queue);

    const job = queue.testMode.jobs[0];
    job.emit('complete');
    job.emit('failed', new Error('Test error'));
    job.emit('progress', 50);

    expect(consoleSpy.calledWith(`Notification job ${job.id} completed`)).to.be.true;
    expect(consoleSpy.calledWith(`Notification job ${job.id} failed: Error: Test error`)).to.be.true;
    expect(consoleSpy.calledWith(`Notification job ${job.id} 50% complete`)).to.be.true;

    consoleSpy.restore();
  });
});

import kue from 'kue';
import { expect } from 'chai';

const queue = kue.createQueue();

before(function() {
  queue.testMode.enter();
});

afterEach(function() {
  queue.testMode.clear();
});

after(function() {
  queue.testMode.exit()
});

it('does something cool', function() {
  const job = queue.createJob('myJob', { foo: 'bar' });
  job.save((err) => {
    console.log(`error: ${err}`)
    console.log(`Job: ${job}`)
    if (!err) console.log(`Job created: ${job}`);
  })
  console.log(`Job: ${job}`)
  console.dir(queue.createJob)
  queue.createJob('anotherJob', { baz: 'bip' }).save();
  expect(queue.testMode.jobs.length).to.equal(2);
  expect(queue.testMode.jobs[0].type).to.equal('myJob');
  expect(queue.testMode.jobs[0].data).to.eql({ foo: 'bar' });
});
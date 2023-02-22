# Worker Pool

Worker pools are a “concurrency pattern” in which a fixed number of workers runs parallel in order to work in a number of task that are holding in a queue.

In golang we use goroutines and channels to build this pattern. Usually will the workers be defined by a goroutine that is holding until it get data through a channel which is the responsibility to coordinate the workers and the task in the queue (usually a buffered channel).

![[Pasted image 20230222164558.png]]
![[Pasted image 20230222164614.png]]

Reference: https://blog.devgenius.io/golang-concurrency-worker-pool-2aff9cbc6255
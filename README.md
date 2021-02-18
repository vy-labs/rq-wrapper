
# rq-wrapper

## Dependencies required to run rq-wrapper

-   Python 3
-   rq
-   python-dotenv

## Get a copy of source code

- Clone the rq-wrapper repository and `cd ` into the directory.

```
git clone git@github.com:vy-labs/rq-wrapper.git
cd rq-wrapper
```
## Install rq-wrapper in your project locally

-`cd` into the project directory.

```
pip install -e path-to-rq-wrapper
```

## Use rq-wrapper

- First run a redis server
```
redis-server
```

- Define a function

```python
import requests

def count_words_at_url(url):
    """Just an example function that's called async."""
    resp = requests.get(url)
    return len(resp.text.split())
```

- Create a queue

```python
from redis import Redis
from rq_wrapper import Queue

queue = Queue(job_id=<JOB_ID>, connection=Redis())
```

- Enqueue the function call

```python
from my_module import count_words_at_url
job = queue.enqueue(count_words_at_url, 'http://nvie.com')
```

- Schedule jobs

```python
# Schedule job to run at 9:15, October 10th
job = queue.enqueue_at(datetime(2019, 10, 8, 9, 15), say_hello)

# Schedule job to run in 10 seconds
job = queue.enqueue_in(timedelta(seconds=10), say_hello)
```

- Retry failed jobs

```python
from rq_wrapper import Retry

# Retry up to 3 times, failed job will be requeued immediately
queue.enqueue(say_hello, retry=Retry(max=3))

# Retry up to 3 times, with configurable intervals between retries
queue.enqueue(say_hello, retry=Retry(max=3, interval=[10, 30, 60]))
```
- For more information head over to [rq's documentation](https://python-rq.org/), but don't forget to replace `rq` with `rq_wrapper`

## The worker

- Start executing the function calls in the background, start a worker in your project's directory

```
rq_wrapper worker
*** Listening for work on default
Got count_words_at_url('http://nvie.com') from default
Job result = 818
*** Listening for work on default
```

- Provide `JOB_ID` for the worker
```
JOB_ID=<job_id> rq_wrapper worker
```

## Dashboard

#### Usage
```shell
RQ_NAMESPACE=<queue_name> local_dashboard
```




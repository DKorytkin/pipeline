# pipeline
Simple pipelines of Python functions


## Usage

```python
from pipeline import Stage


class CollectData(Stage):
    def execute(self):
        # todo some stuff
        self.context.data = [b * 3 for b in range(10)] * 3


class ProcessingData(Stage):
    def execute(self):
        # todo some stuff
        print("Processing data={}".format(len(self.context.data)))


class StoreData(Stage):
    def execute(self):
        # todo some stuff
        print("Storing data to DB")
        return
```
Execution:
```python
pipeline = CollectData() >> ProcessingData() >> StoreData()
pipeline()
```
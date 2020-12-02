import abc


class PipelineContext:
    pass


class Stage:

    @property
    def context(self):
        c = getattr(self, "_context", None)
        if c is None:
            c = PipelineContext()
            setattr(self, "_context", c)
        return c

    @context.setter
    def context(self, context):
        setattr(self, "_context", context)

    @property
    def current_stage(self) -> "Stage":
        cs = getattr(self, "_current_stage", None)
        if cs is None:
            return self
        return cs

    @property
    def next_stage(self) -> "Stage":
        return getattr(self, "_next_stage", None)

    @next_stage.setter
    def next_stage(self, stage: "Stage"):
        assert isinstance(stage, Stage)
        stage.context = self.context
        setattr(self, "_next_stage", stage)

    def setup_next_stage(self, stage: "Stage"):
        self.current_stage.next_stage = stage
        setattr(self, "_current_stage", stage)
        return self

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def __rshift__(self, other):
        return self.setup_next_stage(other)

    def __call__(self, *args, **kwargs):
        self.execute(*args, **kwargs)
        if self.next_stage:
            return self.next_stage()


class CollectData(Stage):
    def execute(self):
        print("Collecting data")
        self.context.data = [b * 3 for b in self.context.build_ids] * 3


class ProcessingData(Stage):
    def execute(self):
        print("Processing data={}".format(len(self.context.data)))


class StoreData(Stage):
    def execute(self):
        print("Storing data to DB")
        return

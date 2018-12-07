# @generated by generate_proto_mypy_stubs.py.  Do not edit!
from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    List as typing___List,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    cast as typing___cast,
)


class TaskType(int):
    @classmethod
    def Name(cls, number: int) -> str: ...
    @classmethod
    def Value(cls, name: str) -> int: ...
    @classmethod
    def keys(cls) -> typing___List[str]: ...
    @classmethod
    def values(cls) -> typing___List[int]: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[str, int]]: ...
TASK_TYPE_UNDEFINED = typing___cast(TaskType, 0)
CLASSIFICATION = typing___cast(TaskType, 1)
REGRESSION = typing___cast(TaskType, 2)
CLUSTERING = typing___cast(TaskType, 3)
LINK_PREDICTION = typing___cast(TaskType, 4)
VERTEX_NOMINATION = typing___cast(TaskType, 5)
COMMUNITY_DETECTION = typing___cast(TaskType, 6)
GRAPH_CLUSTERING = typing___cast(TaskType, 7)
GRAPH_MATCHING = typing___cast(TaskType, 8)
TIME_SERIES_FORECASTING = typing___cast(TaskType, 9)
COLLABORATIVE_FILTERING = typing___cast(TaskType, 10)
OBJECT_DETECTION = typing___cast(TaskType, 11)

class TaskSubtype(int):
    @classmethod
    def Name(cls, number: int) -> str: ...
    @classmethod
    def Value(cls, name: str) -> int: ...
    @classmethod
    def keys(cls) -> typing___List[str]: ...
    @classmethod
    def values(cls) -> typing___List[int]: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[str, int]]: ...
TASK_SUBTYPE_UNDEFINED = typing___cast(TaskSubtype, 0)
NONE = typing___cast(TaskSubtype, 1)
BINARY = typing___cast(TaskSubtype, 2)
MULTICLASS = typing___cast(TaskSubtype, 3)
MULTILABEL = typing___cast(TaskSubtype, 4)
UNIVARIATE = typing___cast(TaskSubtype, 5)
MULTIVARIATE = typing___cast(TaskSubtype, 6)
OVERLAPPING = typing___cast(TaskSubtype, 7)
NONOVERLAPPING = typing___cast(TaskSubtype, 8)

class PerformanceMetric(int):
    @classmethod
    def Name(cls, number: int) -> str: ...
    @classmethod
    def Value(cls, name: str) -> int: ...
    @classmethod
    def keys(cls) -> typing___List[str]: ...
    @classmethod
    def values(cls) -> typing___List[int]: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[str, int]]: ...
METRIC_UNDEFINED = typing___cast(PerformanceMetric, 0)
ACCURACY = typing___cast(PerformanceMetric, 1)
PRECISION = typing___cast(PerformanceMetric, 2)
RECALL = typing___cast(PerformanceMetric, 3)
F1 = typing___cast(PerformanceMetric, 4)
F1_MICRO = typing___cast(PerformanceMetric, 5)
F1_MACRO = typing___cast(PerformanceMetric, 6)
ROC_AUC = typing___cast(PerformanceMetric, 7)
ROC_AUC_MICRO = typing___cast(PerformanceMetric, 8)
ROC_AUC_MACRO = typing___cast(PerformanceMetric, 9)
MEAN_SQUARED_ERROR = typing___cast(PerformanceMetric, 10)
ROOT_MEAN_SQUARED_ERROR = typing___cast(PerformanceMetric, 11)
ROOT_MEAN_SQUARED_ERROR_AVG = typing___cast(PerformanceMetric, 12)
MEAN_ABSOLUTE_ERROR = typing___cast(PerformanceMetric, 13)
R_SQUARED = typing___cast(PerformanceMetric, 14)
NORMALIZED_MUTUAL_INFORMATION = typing___cast(PerformanceMetric, 15)
JACCARD_SIMILARITY_SCORE = typing___cast(PerformanceMetric, 16)
PRECISION_AT_TOP_K = typing___cast(PerformanceMetric, 17)
OBJECT_DETECTION_AVERAGE_PRECISION = typing___cast(PerformanceMetric, 18)
LOSS = typing___cast(PerformanceMetric, 100)

class ProblemPerformanceMetric(google___protobuf___message___Message):
    metric = ... # type: PerformanceMetric
    k = ... # type: int
    pos_label = ... # type: typing___Text

    def __init__(self,
        metric : typing___Optional[PerformanceMetric] = None,
        k : typing___Optional[int] = None,
        pos_label : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ProblemPerformanceMetric: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Problem(google___protobuf___message___Message):
    id = ... # type: typing___Text
    version = ... # type: typing___Text
    name = ... # type: typing___Text
    description = ... # type: typing___Text
    task_type = ... # type: TaskType
    task_subtype = ... # type: TaskSubtype

    @property
    def performance_metrics(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ProblemPerformanceMetric]: ...

    def __init__(self,
        id : typing___Optional[typing___Text] = None,
        version : typing___Optional[typing___Text] = None,
        name : typing___Optional[typing___Text] = None,
        description : typing___Optional[typing___Text] = None,
        task_type : typing___Optional[TaskType] = None,
        task_subtype : typing___Optional[TaskSubtype] = None,
        performance_metrics : typing___Optional[typing___Iterable[ProblemPerformanceMetric]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Problem: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class ProblemTarget(google___protobuf___message___Message):
    target_index = ... # type: int
    resource_id = ... # type: typing___Text
    column_index = ... # type: int
    column_name = ... # type: typing___Text
    clusters_number = ... # type: int

    def __init__(self,
        target_index : typing___Optional[int] = None,
        resource_id : typing___Optional[typing___Text] = None,
        column_index : typing___Optional[int] = None,
        column_name : typing___Optional[typing___Text] = None,
        clusters_number : typing___Optional[int] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ProblemTarget: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class ProblemInput(google___protobuf___message___Message):
    dataset_id = ... # type: typing___Text

    @property
    def targets(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ProblemTarget]: ...

    def __init__(self,
        dataset_id : typing___Optional[typing___Text] = None,
        targets : typing___Optional[typing___Iterable[ProblemTarget]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ProblemInput: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class ProblemDescription(google___protobuf___message___Message):

    @property
    def problem(self) -> Problem: ...

    @property
    def inputs(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ProblemInput]: ...

    def __init__(self,
        problem : typing___Optional[Problem] = None,
        inputs : typing___Optional[typing___Iterable[ProblemInput]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ProblemDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

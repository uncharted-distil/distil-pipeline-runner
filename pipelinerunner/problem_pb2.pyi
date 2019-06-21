# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
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

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


class TaskType(int):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    @classmethod
    def Name(cls, number: int) -> str: ...
    @classmethod
    def Value(cls, name: str) -> TaskType: ...
    @classmethod
    def keys(cls) -> typing___List[str]: ...
    @classmethod
    def values(cls) -> typing___List[TaskType]: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[str, TaskType]]: ...
TASK_TYPE_UNDEFINED = typing___cast(TaskType, 0)
CLASSIFICATION = typing___cast(TaskType, 1)
REGRESSION = typing___cast(TaskType, 2)
CLUSTERING = typing___cast(TaskType, 3)
LINK_PREDICTION = typing___cast(TaskType, 4)
VERTEX_NOMINATION = typing___cast(TaskType, 5)
VERTEX_CLASSIFICATION = typing___cast(TaskType, 6)
COMMUNITY_DETECTION = typing___cast(TaskType, 7)
GRAPH_MATCHING = typing___cast(TaskType, 8)
TIME_SERIES_FORECASTING = typing___cast(TaskType, 9)
COLLABORATIVE_FILTERING = typing___cast(TaskType, 10)
OBJECT_DETECTION = typing___cast(TaskType, 11)
SEMISUPERVISED_CLASSIFICATION = typing___cast(TaskType, 12)
SEMISUPERVISED_REGRESSION = typing___cast(TaskType, 13)

class TaskSubtype(int):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    @classmethod
    def Name(cls, number: int) -> str: ...
    @classmethod
    def Value(cls, name: str) -> TaskSubtype: ...
    @classmethod
    def keys(cls) -> typing___List[str]: ...
    @classmethod
    def values(cls) -> typing___List[TaskSubtype]: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[str, TaskSubtype]]: ...
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
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    @classmethod
    def Name(cls, number: int) -> str: ...
    @classmethod
    def Value(cls, name: str) -> PerformanceMetric: ...
    @classmethod
    def keys(cls) -> typing___List[str]: ...
    @classmethod
    def values(cls) -> typing___List[PerformanceMetric]: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[str, PerformanceMetric]]: ...
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
MEAN_ABSOLUTE_ERROR = typing___cast(PerformanceMetric, 12)
R_SQUARED = typing___cast(PerformanceMetric, 13)
NORMALIZED_MUTUAL_INFORMATION = typing___cast(PerformanceMetric, 14)
JACCARD_SIMILARITY_SCORE = typing___cast(PerformanceMetric, 15)
PRECISION_AT_TOP_K = typing___cast(PerformanceMetric, 17)
OBJECT_DETECTION_AVERAGE_PRECISION = typing___cast(PerformanceMetric, 18)
HAMMING_LOSS = typing___cast(PerformanceMetric, 19)
RANK = typing___cast(PerformanceMetric, 99)
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
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"k",u"metric",u"pos_label"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"k",b"metric",b"pos_label"]) -> None: ...

class Problem(google___protobuf___message___Message):
    task_type = ... # type: TaskType
    task_subtype = ... # type: TaskSubtype

    @property
    def performance_metrics(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ProblemPerformanceMetric]: ...

    def __init__(self,
        task_type : typing___Optional[TaskType] = None,
        task_subtype : typing___Optional[TaskSubtype] = None,
        performance_metrics : typing___Optional[typing___Iterable[ProblemPerformanceMetric]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Problem: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"performance_metrics",u"task_subtype",u"task_type"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"performance_metrics",b"task_subtype",b"task_type"]) -> None: ...

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
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"clusters_number",u"column_index",u"column_name",u"resource_id",u"target_index"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"clusters_number",b"column_index",b"column_name",b"resource_id",b"target_index"]) -> None: ...

class ProblemPrivilegedData(google___protobuf___message___Message):
    privileged_data_index = ... # type: int
    resource_id = ... # type: typing___Text
    column_index = ... # type: int
    column_name = ... # type: typing___Text

    def __init__(self,
        privileged_data_index : typing___Optional[int] = None,
        resource_id : typing___Optional[typing___Text] = None,
        column_index : typing___Optional[int] = None,
        column_name : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ProblemPrivilegedData: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"column_index",u"column_name",u"privileged_data_index",u"resource_id"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"column_index",b"column_name",b"privileged_data_index",b"resource_id"]) -> None: ...

class ProblemInput(google___protobuf___message___Message):
    dataset_id = ... # type: typing___Text

    @property
    def targets(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ProblemTarget]: ...

    @property
    def privileged_data(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ProblemPrivilegedData]: ...

    def __init__(self,
        dataset_id : typing___Optional[typing___Text] = None,
        targets : typing___Optional[typing___Iterable[ProblemTarget]] = None,
        privileged_data : typing___Optional[typing___Iterable[ProblemPrivilegedData]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ProblemInput: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"dataset_id",u"privileged_data",u"targets"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"dataset_id",b"privileged_data",b"targets"]) -> None: ...

class DataAugmentation(google___protobuf___message___Message):
    domain = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    keywords = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    def __init__(self,
        domain : typing___Optional[typing___Iterable[typing___Text]] = None,
        keywords : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> DataAugmentation: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"domain",u"keywords"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"domain",b"keywords"]) -> None: ...

class ProblemDescription(google___protobuf___message___Message):
    id = ... # type: typing___Text
    version = ... # type: typing___Text
    name = ... # type: typing___Text
    description = ... # type: typing___Text
    digest = ... # type: typing___Text
    other_names = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    @property
    def problem(self) -> Problem: ...

    @property
    def inputs(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ProblemInput]: ...

    @property
    def data_augmentation(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[DataAugmentation]: ...

    def __init__(self,
        problem : typing___Optional[Problem] = None,
        inputs : typing___Optional[typing___Iterable[ProblemInput]] = None,
        id : typing___Optional[typing___Text] = None,
        version : typing___Optional[typing___Text] = None,
        name : typing___Optional[typing___Text] = None,
        description : typing___Optional[typing___Text] = None,
        digest : typing___Optional[typing___Text] = None,
        data_augmentation : typing___Optional[typing___Iterable[DataAugmentation]] = None,
        other_names : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ProblemDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"problem"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"data_augmentation",u"description",u"digest",u"id",u"inputs",u"name",u"other_names",u"problem",u"version"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"problem",b"problem"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[b"data_augmentation",b"description",b"digest",b"id",b"inputs",b"name",b"other_names",b"problem",b"version"]) -> None: ...

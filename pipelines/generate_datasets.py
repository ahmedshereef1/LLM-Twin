from zenml import pipeline

from services.domain.dataset import DatasetType
from scripts.generate_datasets.generate_instruction_dataset import (
    generate_intruction_dataset,
)
from scripts.generate_datasets.generate_preference_dataset import (
    generate_preference_dataset,
)
from scripts.generate_datasets.query_feature_store import query_feature_store
from scripts.generate_datasets.create_prompts import create_prompts
from scripts.generate_datasets.push_to_huggingface import push_to_huggingface


@pipeline
def generate_datasets(
    dataset_type: DatasetType = DatasetType.INSTRUCTION,
    test_split_size: float = 0.1,
    push_to_hugface: bool = False,
    dataset_id: str | None = None,
    mock: bool = False,
    wait_for: str | list[str] | None = None,
) -> None:
    cleaned_documents = query_feature_store(after=wait_for)
    prompts = create_prompts(documents=cleaned_documents, document_type=dataset_type)

    if dataset_type == DatasetType.INSTRUCTION:
        dataset = generate_intruction_dataset(
            prompts=prompts, test_split_size=test_split_size, mock=mock
        )
    elif dataset_type == DatasetType.PREFERENCE:
        dataset = generate_preference_dataset(
            prompts=prompts, test_split_size=test_split_size, mock=mock
        )
    else:
        raise ValueError(f"Invalid dataset type: {dataset_type}")

    if push_to_hugface:
        push_to_huggingface(dataset=dataset, dataset_id=dataset_id)

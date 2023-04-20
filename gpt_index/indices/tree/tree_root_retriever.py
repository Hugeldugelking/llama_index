"""Retrieve query."""
import logging
from typing import Any, List

from gpt_index.data_structs.node_v2 import Node, NodeWithScore
from gpt_index.indices.common.base_retriever import BaseRetriever
from gpt_index.indices.query.base import BaseGPTIndexQuery
from gpt_index.indices.query.schema import QueryBundle
from gpt_index.indices.response.type import ResponseMode
from gpt_index.indices.tree.base import GPTTreeIndex
from gpt_index.indices.utils import get_sorted_node_list

logger = logging.getLogger(__name__)


class TreeRootRetriever(BaseRetriever):
    """GPT Tree Index retrieve query.

    This class directly retrieves the answer from the root nodes.

    Unlike GPTTreeIndexLeafQuery, this class assumes the graph already stores
    the answer (because it was constructed with a query_str), so it does not
    attempt to parse information down the graph in order to synthesize an answer.

    .. code-block:: python

        response = index.query("<query_str>", mode="retrieve")

    Args:
        text_qa_template (Optional[QuestionAnswerPrompt]): Question-Answer Prompt
            (see :ref:`Prompt-Templates`).

    """

    def __init__(self, index: GPTTreeIndex):
        self._index = index
        self._index_struct = index.index_struct
        self._docstore = index.docstore

    def retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[Node]:
        """Get nodes for response."""
        logger.info(f"> Starting query: {query_bundle.query_str}")
        root_nodes = self._docstore.get_node_dict(self._index_struct.root_nodes)
        sorted_nodes = get_sorted_node_list(root_nodes)
        return [NodeWithScore(node) for node in sorted_nodes]

    @classmethod
    def from_args(  # type: ignore
        cls,
        response_mode: ResponseMode = ResponseMode.SIMPLE_SUMMARIZE,
        **kwargs: Any,
    ) -> BaseGPTIndexQuery:
        if response_mode != ResponseMode.SIMPLE_SUMMARIZE:
            raise ValueError("response_mode should not be specified for retrieve query")

        return super().from_args(
            response_mode=response_mode,
            **kwargs,
        )
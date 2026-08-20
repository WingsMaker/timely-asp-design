"""
This module defines the `ModelExplainability` class, which is responsible for providing
insights into the behavior and decision-making processes of machine learning models.
The class supports both global and local explainability.
"""


import logging
from typing import Any, Dict, List, Union

import pandas as pd
from interpret.glassbox import ExplainableBoostingClassifier
from modeling.model_classification import EBMModel
from plotly.graph_objects import Figure


class ModelExplainability:
    """
    ModelExplainability class for providing insights into machine learning model behavior.
    Designed to facilitate both global and local explainability for explainable models.

    The main methods enable users to:
        - Retrieve global explanations for feature importance and interactions through
            visualizations.
        - Access JSON formatted global explanations for integration into reporting tools.
        - Generate local explanations for individual predictions, including visual
            and JSON outputs.
        - Extract explanations for all instances in a dataset
        - Filter output data to return only relevant keys

    Initializes a ModelExplainability object.

    Args:
        model (Union[EBMModel, ExplainableBoostingClassifier]):
            An instance of an explainable model used for generating explanations.
        preselected_keys (List[str], optional):
            A list of keys to be included in the output JSON explanations.
            Defaults to a predefined set.

    Attributes:
        logger (logging.Logger):
            Logger instance for logging information during explainability processing.
        explainable_model (Union[EBMModel, ExplainableBoostingClassifier]):
            The model object used to generate explanations, extracted from the input model.
        explainable_global:
            Global explanation object that provides insights into feature importance.
        feature_names_list (List[str]):
            List of feature names utilized by the explainable model for generating explanations.
        preselected_keys (List[str]):
            The keys selected to filter the output JSON data for better usability.
    """

    def __init__(
        self,
        model: Union[EBMModel, ExplainableBoostingClassifier],
        preselected_keys: List[str] = None,
    ) -> None:

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Check model type
        if isinstance(model, EBMModel):
            self.explainable_model = model.get_model_object()
        elif isinstance(model, ExplainableBoostingClassifier):
            self.explainable_model = model
        else:
            self.explainable_model = None

        # Assign only if it is supported
        if self.explainable_model is None:
            self.logger.error(f"Unsupported model type: {type(model)}")
            raise TypeError("Unsupported model type")
        else:
            self.explainable_global = self.explainable_model.explain_global()
            self.feature_names_list = self.explainable_model.feature_names_in_

        if preselected_keys is None:
            self.preselected_keys = ["names", "scores", "values", "extra"]
        else:
            self.preselected_keys = preselected_keys

    # =====================
    # Global explainability
    # =====================
    def get_explanation_global_image(self, feature_name) -> Figure:
        """
        Generate and retrieve the global explanation visualization for a specific feature.

        This method creates a global explainability plot for the given feature name. It uses the
        explainable model's global explanation method to display how the feature contributes to the
        overall predictions made by the model.

        Args:
            feature_name (str): The name of the feature for which to generate the
                                global explanation.This must be one of the features used
                                by the model during training.

        Raises:
            ValueError: If the provided feature name is not found in the model's feature list,
                        an error is raised, indicating the valid feature names.

        Returns:
            Figure: A Plotly Figure object that visually explains the global impact
            of the selected feature on the model's predictions.
        """
        if feature_name not in self.feature_names_list:
            raise ValueError(
                f"Feature_name must part of feature name list"
                f"\nFeature name: {feature_name}"
                f"\nFeature name list: {self.feature_names_list}"
            )

        selected_index = self.feature_names_list.index(feature_name)
        image = self.explainable_global.visualize(selected_index)
        return image

    def get_explanation_global_json(self) -> Dict[str, Any]:
        """
        Retrieve and filter the global explanation data for the model.

        This method extracts the global explainability information from the model, providing
        insights into the contribution and importance of features in the overall model predictions.
        The raw data is filtered to include only the keys specified during initialization
        (e.g., 'names', 'scores', 'values'), ensuring the returned dictionary
        contains only the most relevant information.

        Returns:
            Dict[str, Any]: A dictionary containing the global explainability data,
            filtered by the preselected keys (e.g., feature names, scores, etc.).

        Raises:
            TypeError: If the data is not formatted as expected, it will raise an error
                         to ensure proper filtering.
        """

        json_data = self.explainable_global.data()
        json_data = self._filter_data(json_data)

        return json_data

    # ====================
    # Local explainability
    # ====================
    def get_explanation_local_image(
        self,
        input_features: pd.DataFrame,
        target_labels: pd.Series,
        selected_index: int = 0,
    ):
        """
        Generate a visual representation of local explainability for a specific instance.

        This method provides insights into how the model arrived at its prediction
        for a particular instance (row) in the input dataset. It generates a Plotly
        figure that visualizes the contribution of each feature to the prediction
        for the selected instance.

        Args:
            input_features (pd.DataFrame): A DataFrame containing the input features
                                        used for making predictions.
            target_labels (pd.Series): A Series containing the true labels or targets
                                    associated with the input features.
            selected_index (int, optional): The index of the instance for which to generate
                                            the local explainability. Defaults to 0.

        Returns:
            Figure: A Plotly Figure object representing the local explainability
            for the selected instance, showing feature contributions to the prediction.

        Raises:
            ValueError: Raised if the `selected_index` exceeds the number of instances
                        in the input data or if the length of `input_features`
                        does not match the length of `target_labels`.
        """

        if selected_index >= len(input_features):
            raise ValueError(
                f"Selected_index must be smaller than length of data"
                f"\nSelected Index: {selected_index}"
                f"\nLength of data: {len(input_features)}"
            )
        elif len(input_features) != len(target_labels):
            raise ValueError(
                f"Length of input feature must be same as target labels"
                f"\nLength of input features: {len(input_features)}"
                f"\nLength of target labels: {len(target_labels)}"
            )

        explainable_local = self.explainable_model.explain_local(
            input_features, target_labels
        )
        image = explainable_local.visualize(selected_index)

        return image

    def get_explanation_local_json(
        self,
        input_features: pd.DataFrame,
        target_labels: pd.Series,
        selected_index: int = 0,
    ) -> Dict[str, Any]:
        """
        Retrieve and format the local explanation data for a specific instance.

        This method generates local explainability for a selected instance (based on the
        `selected_index`) by analyzing the contribution of each feature to the model's prediction.
        The output is a dictionary containing the local explanation data, filtered by the
        preselected keys set during initialization.

        Args:
            input_features (pd.DataFrame): A DataFrame containing the input features
                                        used for making predictions.
            target_labels (pd.Series): A Series containing the true labels or targets
                                    corresponding to the input features.
            selected_index (int, optional): The index of the specific instance to
                                            retrieve local explainability for.
                                            Defaults to 0.

        Returns:
            Dict[str, Any]: A dictionary containing
            local explanation data, filtered by the
            preselected keys, for the selected instance.

        Raises:
            ValueError:
                - If `selected_index` is greater than or equal
                to the number of instances in `input_features`.
                - If the number of rows in `input_features` does not match
                the number of entries in `target_labels`.
        """

        if selected_index >= len(input_features):
            raise ValueError(
                f"Selected_index must be smaller than length of data"
                f"\nSelected Index: {selected_index}"
                f"\nLength of data: {len(input_features)}"
            )
        elif len(input_features) != len(target_labels):
            raise ValueError(
                f"Length of input feature must be same as target labels"
                f"\nLength of input features: {len(input_features)}"
                f"\nLength of target labels: {len(target_labels)}"
            )

        single_input = input_features[selected_index : selected_index + 1]
        single_target = target_labels[selected_index : selected_index + 1]
        explainable_local = self.explainable_model.explain_local(
            single_input, single_target
        )
        json_data = explainable_local.data(0)
        json_data = self._filter_data(json_data)

        return json_data

    def get_all_explanation_local_json(
        self,
        input_features: pd.DataFrame,
        target_labels: pd.Series,
    ) -> List[str]:
        """
        Retrieve and format the local explanation data for the entire dataset.

        This method computes local explainability for all instances in the provided
        input dataset. For each instance, the method analyzes the contribution of
        each feature to the model's prediction and returns a list of local explanations
        in JSON format. Each JSON object contains the local explanation data filtered
        by preselected keys defined during the initialization of the class.

        Args:
            input_features (pd.DataFrame): A DataFrame containing the input features
                                        used for model predictions.
            target_labels (pd.Series): A Series containing the true labels or targets
                                    corresponding to the input features.

        Returns:
            List[str]: A list of JSON objects where each entry corresponds to the
            local explainability data for a specific instance in the dataset.

        Raises:
            ValueError: If the number of rows in `input_features` does not match the number
                        of entries in `target_labels`.
        """

        if len(input_features) != len(target_labels):
            raise ValueError(
                f"Length of input feature must be same as target labels"
                f"\nLength of input features: {len(input_features)}"
                f"\nLength of target labels: {len(target_labels)}"
            )
        explainable_local = self.explainable_model.explain_local(
            input_features, target_labels
        )

        json_results_list = []
        for idx in range(0, len(input_features)):
            json_data = explainable_local.data(idx)
            json_data = self._filter_data(json_data)
            json_results_list.append(json_data)

        return json_results_list

    # ====================
    # Supporting functions
    # ====================
    def _filter_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter the provided dictionary to include only the preselected keys.

        This method filters the input dictionary, `json_data`, by removing any keys
        that are not present in the `preselected_keys` attribute. It ensures that
        only relevant information remains in the returned dictionary.

        Args:
            json_data (Dict[str, Any]): The dictionary containing explanation data
                                        to be filtered.

        Returns:
            Dict[str, Any]: A filtered dictionary containing only the keys
            specified in `preselected_keys`.

        Raises:
            TypeError: If the provided `json_data` is not a dictionary.
        """

        if isinstance(json_data, dict):
            for key in list(json_data.keys()):
                if key not in self.preselected_keys:
                    json_data.pop(key)
        else:
            raise TypeError(f"json_data must be a dict: {json_data}")

        return json_data

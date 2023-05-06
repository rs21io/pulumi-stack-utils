# pylint: disable=attribute-defined-outside-init

import json
import os
import random
from datetime import datetime
from unittest import mock

import pytest
from dateutil.tz import tzutc

from pulumi_stack_utils import stack_reference


def mock_download_fileobj(stream):
    """Mock download_fileobj method of S3.Object"""
    latest = random.choice(["latest", "Latest"])
    mock_state = {
        "checkpoint": {
            latest: {
                "resources": [
                    {
                        "type": "pulumi:pulumi:Stack",
                        "outputs": {"test-output": "test-value"},
                    }
                ]
            }
        }
    }
    stream.write(json.dumps(mock_state).encode())


class TestStackReference:
    @mock.patch("boto3.resource")
    def setup_method(self, _, mock_s3):
        """This setup method is optional and will run before every test.
        Good for things class instantiation or setting variables
        that will be reused in multiple tests.
        """
        mock_object = mock.MagicMock()
        mock_object.last_modified = datetime.now(tz=tzutc())
        mock_object.download_fileobj = mock_download_fileobj
        mock_s3.return_value.Object.return_value = mock_object
        stack_name = "test-stack"
        self.ref = stack_reference.StackReference(
            stack_name, backend_url="s3://test-bucket/test-prefix/"
        )
        self.ref._s3 = mock_s3

    def test_get_output(self):
        output = self.ref.get_output("test-output")
        assert output == "test-value"

    def test_config_not_found(self):
        with pytest.raises(FileNotFoundError):
            stack_reference.StackReference("test-stack")

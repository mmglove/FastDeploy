"""
# Copyright (c) 2025  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

import os
import unittest
from unittest.mock import patch

from fastdeploy import envs
from fastdeploy.envs import _validate_split_kv_size


class TestEnvironmentVariableDefaults(unittest.TestCase):
    """Test default values of environment variables in fastdeploy.envs."""

    def test_fd_debug_default(self):
        """FD_DEBUG defaults to 0 (integer)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_DEBUG", None)
            self.assertEqual(envs.FD_DEBUG, 0)
            self.assertIsInstance(envs.FD_DEBUG, int)

    def test_fd_log_dir_default(self):
        """FD_LOG_DIR defaults to 'log' (string)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_LOG_DIR", None)
            self.assertEqual(envs.FD_LOG_DIR, "log")

    def test_fd_model_source_default(self):
        """FD_MODEL_SOURCE defaults to 'AISTUDIO'."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_MODEL_SOURCE", None)
            self.assertEqual(envs.FD_MODEL_SOURCE, "AISTUDIO")

    def test_fd_model_cache_default(self):
        """FD_MODEL_CACHE defaults to None."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_MODEL_CACHE", None)
            self.assertIsNone(envs.FD_MODEL_CACHE)

    def test_fd_max_stop_seqs_num_default(self):
        """FD_MAX_STOP_SEQS_NUM defaults to 5 (integer)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_MAX_STOP_SEQS_NUM", None)
            self.assertEqual(envs.FD_MAX_STOP_SEQS_NUM, 5)
            self.assertIsInstance(envs.FD_MAX_STOP_SEQS_NUM, int)

    def test_fd_stop_seqs_max_len_default(self):
        """FD_STOP_SEQS_MAX_LEN defaults to 8 (integer)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_STOP_SEQS_MAX_LEN", None)
            self.assertEqual(envs.FD_STOP_SEQS_MAX_LEN, 8)
            self.assertIsInstance(envs.FD_STOP_SEQS_MAX_LEN, int)

    def test_fd_use_hf_tokenizer_default(self):
        """FD_USE_HF_TOKENIZER defaults to False (bool)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_USE_HF_TOKENIZER", None)
            self.assertIs(envs.FD_USE_HF_TOKENIZER, False)
            self.assertIsInstance(envs.FD_USE_HF_TOKENIZER, bool)

    def test_fd_attention_backend_default(self):
        """FD_ATTENTION_BACKEND defaults to 'APPEND_ATTN'."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_ATTENTION_BACKEND", None)
            self.assertEqual(envs.FD_ATTENTION_BACKEND, "APPEND_ATTN")

    def test_fd_sampling_class_default(self):
        """FD_SAMPLING_CLASS defaults to 'base'."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_SAMPLING_CLASS", None)
            self.assertEqual(envs.FD_SAMPLING_CLASS, "base")

    def test_fd_moe_backend_default(self):
        """FD_MOE_BACKEND defaults to 'cutlass'."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_MOE_BACKEND", None)
            self.assertEqual(envs.FD_MOE_BACKEND, "cutlass")

    def test_fd_deterministic_mode_default(self):
        """FD_DETERMINISTIC_MODE defaults to False (bool)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_DETERMINISTIC_MODE", None)
            self.assertIs(envs.FD_DETERMINISTIC_MODE, False)
            self.assertIsInstance(envs.FD_DETERMINISTIC_MODE, bool)

    def test_fd_deterministic_split_kv_size_default(self):
        """FD_DETERMINISTIC_SPLIT_KV_SIZE defaults to 16 (integer)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_DETERMINISTIC_SPLIT_KV_SIZE", None)
            self.assertEqual(envs.FD_DETERMINISTIC_SPLIT_KV_SIZE, 16)
            self.assertIsInstance(envs.FD_DETERMINISTIC_SPLIT_KV_SIZE, int)

    def test_fd_use_deep_gemm_default(self):
        """FD_USE_DEEP_GEMM defaults to False (bool)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_USE_DEEP_GEMM", None)
            self.assertIs(envs.FD_USE_DEEP_GEMM, False)
            self.assertIsInstance(envs.FD_USE_DEEP_GEMM, bool)

    def test_fd_worker_alive_timeout_default(self):
        """FD_WORKER_ALIVE_TIMEOUT defaults to 30 (integer)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_WORKER_ALIVE_TIMEOUT", None)
            self.assertEqual(envs.FD_WORKER_ALIVE_TIMEOUT, 30)
            self.assertIsInstance(envs.FD_WORKER_ALIVE_TIMEOUT, int)

    def test_file_backend_storage_dir_default(self):
        """FILE_BACKEND_STORAGE_DIR defaults to '/tmp/fastdeploy'."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FILE_BACKEND_STORAGE_DIR", None)
            self.assertEqual(envs.FILE_BACKEND_STORAGE_DIR, "/tmp/fastdeploy")

    def test_do_not_track_default(self):
        """DO_NOT_TRACK defaults to False (bool)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("DO_NOT_TRACK", None)
            self.assertIs(envs.DO_NOT_TRACK, False)
            self.assertIsInstance(envs.DO_NOT_TRACK, bool)

    def test_enable_v1_kvcache_scheduler_default(self):
        """ENABLE_V1_KVCACHE_SCHEDULER defaults to 1 (integer)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ENABLE_V1_KVCACHE_SCHEDULER", None)
            self.assertEqual(envs.ENABLE_V1_KVCACHE_SCHEDULER, 1)
            self.assertIsInstance(envs.ENABLE_V1_KVCACHE_SCHEDULER, int)

    def test_fd_log_backup_count_default(self):
        """FD_LOG_BACKUP_COUNT defaults to '7' (string)."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FD_LOG_BACKUP_COUNT", None)
            self.assertEqual(envs.FD_LOG_BACKUP_COUNT, "7")

    def test_cuda_visible_devices_default(self):
        """CUDA_VISIBLE_DEVICES defaults to None when not set."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CUDA_VISIBLE_DEVICES", None)
            self.assertIsNone(envs.CUDA_VISIBLE_DEVICES)


class TestEnvironmentVariableFromOS(unittest.TestCase):
    """Test that environment variables are correctly read from OS environment."""

    def test_fd_debug_from_env(self):
        """FD_DEBUG reads integer value from OS environment."""
        with patch.dict(os.environ, {"FD_DEBUG": "1"}):
            self.assertEqual(envs.FD_DEBUG, 1)

    def test_fd_log_dir_from_env(self):
        """FD_LOG_DIR reads string value from OS environment."""
        with patch.dict(os.environ, {"FD_LOG_DIR": "/var/log/fastdeploy"}):
            self.assertEqual(envs.FD_LOG_DIR, "/var/log/fastdeploy")

    def test_fd_model_source_from_env(self):
        """FD_MODEL_SOURCE reads string value from OS environment."""
        with patch.dict(os.environ, {"FD_MODEL_SOURCE": "MODELSCOPE"}):
            self.assertEqual(envs.FD_MODEL_SOURCE, "MODELSCOPE")

    def test_fd_max_stop_seqs_num_from_env(self):
        """FD_MAX_STOP_SEQS_NUM reads integer value from OS environment."""
        with patch.dict(os.environ, {"FD_MAX_STOP_SEQS_NUM": "10"}):
            self.assertEqual(envs.FD_MAX_STOP_SEQS_NUM, 10)
            self.assertIsInstance(envs.FD_MAX_STOP_SEQS_NUM, int)

    def test_fd_use_hf_tokenizer_from_env(self):
        """FD_USE_HF_TOKENIZER reads bool from OS environment when set to '1'."""
        with patch.dict(os.environ, {"FD_USE_HF_TOKENIZER": "1"}):
            self.assertIs(envs.FD_USE_HF_TOKENIZER, True)

    def test_fd_use_hf_tokenizer_from_env_zero(self):
        """FD_USE_HF_TOKENIZER reads bool from OS environment when set to '0'."""
        with patch.dict(os.environ, {"FD_USE_HF_TOKENIZER": "0"}):
            self.assertIs(envs.FD_USE_HF_TOKENIZER, False)

    def test_fd_deterministic_mode_from_env(self):
        """FD_DETERMINISTIC_MODE reads bool from OS environment when set to '1'."""
        with patch.dict(os.environ, {"FD_DETERMINISTIC_MODE": "1"}):
            self.assertIs(envs.FD_DETERMINISTIC_MODE, True)

    def test_fd_use_deep_gemm_from_env(self):
        """FD_USE_DEEP_GEMM reads bool from OS environment when set to '1'."""
        with patch.dict(os.environ, {"FD_USE_DEEP_GEMM": "1"}):
            self.assertIs(envs.FD_USE_DEEP_GEMM, True)

    def test_do_not_track_from_env(self):
        """DO_NOT_TRACK reads bool from OS environment when set to '1'."""
        with patch.dict(os.environ, {"DO_NOT_TRACK": "1"}):
            self.assertIs(envs.DO_NOT_TRACK, True)

    def test_do_not_track_from_env_zero(self):
        """DO_NOT_TRACK returns False when OS environment is set to '0'."""
        with patch.dict(os.environ, {"DO_NOT_TRACK": "0"}):
            self.assertIs(envs.DO_NOT_TRACK, False)

    def test_fd_attention_backend_from_env(self):
        """FD_ATTENTION_BACKEND reads string value from OS environment."""
        with patch.dict(os.environ, {"FD_ATTENTION_BACKEND": "NATIVE_ATTN"}):
            self.assertEqual(envs.FD_ATTENTION_BACKEND, "NATIVE_ATTN")

    def test_fd_deterministic_split_kv_size_from_env(self):
        """FD_DETERMINISTIC_SPLIT_KV_SIZE reads a valid power-of-2 integer."""
        with patch.dict(os.environ, {"FD_DETERMINISTIC_SPLIT_KV_SIZE": "32"}):
            self.assertEqual(envs.FD_DETERMINISTIC_SPLIT_KV_SIZE, 32)

    def test_fd_worker_alive_timeout_from_env(self):
        """FD_WORKER_ALIVE_TIMEOUT reads integer value from OS environment."""
        with patch.dict(os.environ, {"FD_WORKER_ALIVE_TIMEOUT": "60"}):
            self.assertEqual(envs.FD_WORKER_ALIVE_TIMEOUT, 60)

    def test_file_backend_storage_dir_from_env(self):
        """FILE_BACKEND_STORAGE_DIR reads string value from OS environment."""
        with patch.dict(os.environ, {"FILE_BACKEND_STORAGE_DIR": "/data/fastdeploy"}):
            self.assertEqual(envs.FILE_BACKEND_STORAGE_DIR, "/data/fastdeploy")

    def test_fd_log_backup_count_from_env(self):
        """FD_LOG_BACKUP_COUNT reads string value from OS environment."""
        with patch.dict(os.environ, {"FD_LOG_BACKUP_COUNT": "14"}):
            self.assertEqual(envs.FD_LOG_BACKUP_COUNT, "14")

    def test_cuda_visible_devices_from_env(self):
        """CUDA_VISIBLE_DEVICES reads string value from OS environment."""
        with patch.dict(os.environ, {"CUDA_VISIBLE_DEVICES": "0,1,2"}):
            self.assertEqual(envs.CUDA_VISIBLE_DEVICES, "0,1,2")


class TestValidateSplitKvSize(unittest.TestCase):
    """Test the _validate_split_kv_size helper function."""

    def test_valid_power_of_two_values(self):
        """Valid positive powers of 2 pass validation."""
        valid_values = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
        for val in valid_values:
            with self.subTest(value=val):
                result = _validate_split_kv_size(val)
                self.assertEqual(result, val)

    def test_zero_raises_value_error(self):
        """Zero is not a valid power of 2 and should raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            _validate_split_kv_size(0)
        self.assertIn("FD_DETERMINISTIC_SPLIT_KV_SIZE must be a positive power of 2", str(cm.exception))
        self.assertIn("got 0", str(cm.exception))

    def test_negative_raises_value_error(self):
        """Negative numbers are not valid and should raise ValueError."""
        for val in [-1, -16, -100]:
            with self.subTest(value=val):
                with self.assertRaises(ValueError) as cm:
                    _validate_split_kv_size(val)
                self.assertIn("FD_DETERMINISTIC_SPLIT_KV_SIZE must be a positive power of 2", str(cm.exception))

    def test_non_power_of_two_raises_value_error(self):
        """Non-powers of 2 should raise ValueError."""
        non_powers = [3, 5, 6, 7, 9, 10, 12, 15, 17, 24, 48, 100]
        for val in non_powers:
            with self.subTest(value=val):
                with self.assertRaises(ValueError) as cm:
                    _validate_split_kv_size(val)
                self.assertIn("FD_DETERMINISTIC_SPLIT_KV_SIZE must be a positive power of 2", str(cm.exception))
                self.assertIn(f"got {val}", str(cm.exception))

    def test_invalid_split_kv_size_from_env(self):
        """Setting FD_DETERMINISTIC_SPLIT_KV_SIZE to a non-power-of-2 raises ValueError."""
        with patch.dict(os.environ, {"FD_DETERMINISTIC_SPLIT_KV_SIZE": "12"}):
            with self.assertRaises(ValueError):
                _ = envs.FD_DETERMINISTIC_SPLIT_KV_SIZE

    def test_valid_split_kv_size_from_env(self):
        """Setting FD_DETERMINISTIC_SPLIT_KV_SIZE to a valid power-of-2 works."""
        with patch.dict(os.environ, {"FD_DETERMINISTIC_SPLIT_KV_SIZE": "64"}):
            self.assertEqual(envs.FD_DETERMINISTIC_SPLIT_KV_SIZE, 64)


class TestEnvsModuleInterface(unittest.TestCase):
    """Test the module-level __dir__, __getattr__, and __setattr__ of envs."""

    def test_dir_contains_all_expected_variables(self):
        """__dir__ returns all registered environment variable names."""
        available = dir(envs)
        expected_vars = [
            "FD_DEBUG",
            "FD_LOG_DIR",
            "FD_MODEL_SOURCE",
            "FD_MODEL_CACHE",
            "FD_MAX_STOP_SEQS_NUM",
            "FD_STOP_SEQS_MAX_LEN",
            "FD_USE_HF_TOKENIZER",
            "FD_ATTENTION_BACKEND",
            "FD_SAMPLING_CLASS",
            "FD_MOE_BACKEND",
            "FD_DETERMINISTIC_MODE",
            "FD_DETERMINISTIC_SPLIT_KV_SIZE",
            "FD_USE_DEEP_GEMM",
            "FD_WORKER_ALIVE_TIMEOUT",
            "FILE_BACKEND_STORAGE_DIR",
            "DO_NOT_TRACK",
            "ENABLE_V1_KVCACHE_SCHEDULER",
            "CUDA_VISIBLE_DEVICES",
        ]
        for var in expected_vars:
            with self.subTest(variable=var):
                self.assertIn(var, available)

    def test_getattr_raises_for_unknown_variable(self):
        """Accessing an undefined environment variable raises AttributeError."""
        with self.assertRaises(AttributeError) as cm:
            _ = envs.FD_NON_EXISTENT_VARIABLE_XYZ
        self.assertIn("has no attribute", str(cm.exception))

    def test_setattr_overrides_value(self):
        """__setattr__ allows programmatic override of a registered variable via direct call."""
        original_fn = envs.environment_variables["FD_DEBUG"]
        try:
            envs.__setattr__("FD_DEBUG", 42)
            self.assertEqual(envs.FD_DEBUG, 42)
        finally:
            # Restore the original lambda to avoid polluting other tests
            envs.environment_variables["FD_DEBUG"] = original_fn

    def test_setattr_restores_after_reset(self):
        """After resetting the lambda, the default value is returned again."""
        original_fn = envs.environment_variables["FD_DEBUG"]
        try:
            envs.__setattr__("FD_DEBUG", 99)
            self.assertEqual(envs.FD_DEBUG, 99)
            # Restore original function
            envs.environment_variables["FD_DEBUG"] = original_fn
            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop("FD_DEBUG", None)
                self.assertEqual(envs.FD_DEBUG, 0)
        finally:
            envs.environment_variables["FD_DEBUG"] = original_fn

    def test_setattr_raises_for_unknown_variable(self):
        """__setattr__ raises AssertionError when called directly for an unregistered variable."""
        with self.assertRaises(AssertionError):
            envs.__setattr__("FD_UNKNOWN_VARIABLE_THAT_DOES_NOT_EXIST", "value")


class TestEnvsLazyEvaluation(unittest.TestCase):
    """Test that environment variables are evaluated lazily (at access time)."""

    def test_value_reflects_env_change_between_accesses(self):
        """Changing the OS environment between accesses updates the returned value."""
        with patch.dict(os.environ, {"FD_LOG_DIR": "first"}):
            self.assertEqual(envs.FD_LOG_DIR, "first")

        with patch.dict(os.environ, {"FD_LOG_DIR": "second"}):
            self.assertEqual(envs.FD_LOG_DIR, "second")

    def test_fd_debug_changes_with_env(self):
        """FD_DEBUG reflects different OS environment values on each access."""
        with patch.dict(os.environ, {"FD_DEBUG": "0"}):
            self.assertEqual(envs.FD_DEBUG, 0)

        with patch.dict(os.environ, {"FD_DEBUG": "1"}):
            self.assertEqual(envs.FD_DEBUG, 1)


if __name__ == "__main__":
    unittest.main()

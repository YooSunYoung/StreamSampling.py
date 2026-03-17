"""
Basic functionality tests and statistical validation of
the weighted reservoir sampling multi-element algorithms.
"""

import logging
from collections import Counter

import numpy as np
import pytest

import streamsampling as sp
from streamsampling.weighted_sampling_multi_python import (
    SamplingMethod,
    stream_weighted_sample_multi,
    weighted_sample_multi,
)


@pytest.mark.parametrize(
    'method',
    [
        pytest.param(
            SamplingMethod.A_RES, marks=pytest.mark.skip(reason="Not Implemented Yet")
        ),
        pytest.param(
            SamplingMethod.A_EXPJ, marks=pytest.mark.skip(reason="Not Implemented Yet")
        ),
        SamplingMethod.WRSWR_SKIP,
    ],
)
def test_basic_functionality(method):
    """Test basic functionality of all algorithms."""
    elements = list(range(1, 11))
    weights = [1.0] * 10  # Equal weights
    n_sample = 5

    # Test one-shot sampling
    sample = weighted_sample_multi(elements, weights, n_sample, method)
    assert len(sample) == n_sample, f"{method} failed: wrong sample size"
    assert all(x in elements for x in sample), f"{method} failed: invalid elements"

    # Test streaming
    sampler = stream_weighted_sample_multi(n_sample, method)
    for elem, weight in zip(elements, weights):
        sampler.fit(elem, weight)

    stream_sample = sampler.value()
    assert len(stream_sample) == n_sample, (
        f"{method} streaming failed: wrong sample size"
    )


@pytest.mark.parametrize(
    'method',
    [
        pytest.param(
            SamplingMethod.A_RES, marks=pytest.mark.skip(reason="Not Implemented Yet")
        ),
        pytest.param(
            SamplingMethod.A_EXPJ, marks=pytest.mark.skip(reason="Not Implemented Yet")
        ),
        SamplingMethod.WRSWR_SKIP,
    ],
)
def test_statistical_properties(method):
    """Test that the algorithms produce correct probability distributions."""

    # Test with more elements so sampling without replacement makes sense
    elements = [1, 2, 3, 4]
    weights = [1.0, 3.0, 1.0, 1.0]  # Element 2 should be 3x more likely than others
    n_sample = 2  # Sample 2 out of 4
    n_trials = 5000

    results = []
    rng = np.random.default_rng(42)

    for _ in range(n_trials):
        sample = weighted_sample_multi(
            elements,
            weights,
            n_sample,
            method,
            rng=np.random.default_rng(rng.integers(0, 2**32)),
        )
        results.extend(sample)

    counter = Counter(results)
    total = len(results)

    # For element 2 with weight 3.0 out of total weight 6.0
    freq2 = counter[2] / total
    expected2 = 3.0 / 6.0  # 0.5

    # Allow reasonable deviation for statistical variation
    tolerance = 0.15

    # Focus on testing element 2 which has distinctly different weight
    assert abs(freq2 - expected2) < tolerance, (
        f"{method} failed statistical test: element 2 (freq={freq2:.3f}, expected={expected2:.3f})"
    )


@pytest.mark.skip(reason="SamplingMethod.A_RES/A_EXPJ not available yet.")
def test_edge_cases():
    """Test edge cases and error conditions."""

    # Test with single element
    sample = weighted_sample_multi([42], [1.0], 1, SamplingMethod.A_RES)
    assert sample == [42], "Single element test failed"

    # Test with weight function
    elements = [1, 2, 3, 4, 5]

    def weight_func(x):
        return x  # Weight equals value

    sample = weighted_sample_multi(elements, weight_func, 3, SamplingMethod.A_EXPJ)
    assert len(sample) == 3, "Weight function test failed"

    # Test ordered sampling
    sample_ordered = weighted_sample_multi(
        elements,
        [1] * 5,
        3,
        SamplingMethod.A_RES,
        ordered=True,
        rng=np.random.default_rng(42),
    )
    sampler = stream_weighted_sample_multi(
        3, SamplingMethod.A_RES, ordered=True, rng=np.random.default_rng(42)
    )
    for elem in elements:
        sampler.fit(elem, 1.0)

    stream_ordered = sampler.ordered_value()

    # Both should be ordered (though content may differ due to randomness)
    assert len(sample_ordered) == 3, "Ordered sampling failed"
    assert len(stream_ordered) == 3, "Ordered streaming failed"

    # Test error conditions
    with pytest.raises(ValueError, match="Value"):
        weighted_sample_multi(
            [1, 2], [1.0], 1, SamplingMethod.A_RES
        )  # Mismatched lengths

    sampler = stream_weighted_sample_multi(3, SamplingMethod.A_RES)
    with pytest.raises(ValueError, match="Value"):
        sampler.fit(1, 0.0)  # Zero weight


@pytest.mark.parametrize(
    'method',
    [
        pytest.param(
            SamplingMethod.A_RES, marks=pytest.mark.skip(reason="Not Implemented Yet")
        ),
        pytest.param(
            SamplingMethod.A_EXPJ, marks=pytest.mark.skip(reason="Not Implemented Yet")
        ),
        SamplingMethod.WRSWR_SKIP,
    ],
)
def test_performance(method):
    """Basic performance test."""
    # TODO: Turn this into a proper benchmarking report.
    import time

    # Generate larger test dataset
    n_elements = 10000
    n_sample = 100
    elements = list(range(n_elements))
    weights = np.random.exponential(1.0, n_elements)

    start_time = time.time()
    sample = weighted_sample_multi(elements, weights, n_sample, method)
    end_time = time.time()

    assert len(sample) == n_sample, (
        f"{method} performance test failed: wrong sample size"
    )
    duration = end_time - start_time
    assert duration < 0.1
    # print(f"Duration: {duration}")

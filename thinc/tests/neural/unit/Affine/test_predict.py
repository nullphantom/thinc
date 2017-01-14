import numpy
import pytest
from numpy.testing import assert_allclose
from hypothesis import given, settings
from hypothesis.strategies import integers

from ....ops import NumpyOps
from ...._classes.affine import Affine
from ....exceptions import ShapeError

from ...strategies import arrays_OI_O_BI


@settings(max_examples=100)
@given(arrays_OI_O_BI(max_batch=8, max_out=8, max_in=8))
def test_predict_small(W_b_input):
    W, b, input_ = W_b_input
    nr_out, nr_in = W.shape
    model = Affine(nr_out, nr_in)
    model.W[:] = W
    model.b[:] = b

    einsummed = numpy.einsum('oi,bi->bo', numpy.asarray(W, dtype='float64'),
                            numpy.asarray(input_, dtype='float64'))
    
    expected_output = einsummed + b
    
    predicted_output = model.predict(input_)
    assert_allclose(predicted_output, expected_output, rtol=1e-03, atol=0.001)

@pytest.mark.skip
@given(arrays_OI_O_BI(max_batch=100, max_out=100, max_in=100))
def test_predict_extensive(W_b_input):
    W, b, input_ = W_b_input
    nr_out, nr_in = W.shape
    model = Affine(nr_out, nr_in)
    model.W[:] = W
    model.b[:] = b

    einsummed = numpy.einsum('oi,bi->bo', numpy.asarray(W, dtype='float64'),
                            numpy.asarray(input_, dtype='float64'))
    
    expected_output = einsummed + b
    
    predicted_output = model.predict(input_)
    assert_allclose(predicted_output, expected_output, rtol=1e-04, atol=0.0001)
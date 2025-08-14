import pytest

#function to check square
def square(n):
    return n ** 2

#function to check cube
def cube(n):
    return n ** 3

#function to check fourth power
def fourth_power(n):
    return n ** 4

#function to check fifth power
def fifth_power(n):
    return n ** 5       

#Testing the square function
def test_square():
    assert square(2) == 4 , "Test failed: Square should be 4"
    assert square(3) == 9 , "Test failed: Square should be 9"
    assert square(4) == 16 , "Test failed: Square should be 16"

#Testing for cube function
def test_cube():
    assert cube(2) == 8 , "Test failed: Cube should be 8"
    assert cube(3) == 27 , "Test failed: Cube should be 27"
    assert cube(4) == 64 , "Test failed: Cube should be 64"

#Testing for fourth power
def test_fourth_power():
    assert fourth_power(2) == 16 , "Test failed: Fourth power should be 16"
    assert fourth_power(3) == 81 , "Test failed: Fourth power should be 81"
    assert fourth_power(4) == 256 , "Test failed: Fourth power should be 256"

#Testing for fifth power
def test_fifth_power():
    assert fifth_power(2) == 32 , "Test failed: Fifth power should be 32"
    assert fifth_power(3) == 243 , "Test failed: Fifth power should be 243"
    assert fifth_power(4) == 1024 , "Test failed: Fifth power should be 1024"

def test_invalid_inputs():
    with pytest.raises(TypeError):
        square("a")
    with pytest.raises(TypeError):
        cube("b")
    with pytest.raises(TypeError):
        fourth_power("c")
    with pytest.raises(TypeError):
        fifth_power("d")    
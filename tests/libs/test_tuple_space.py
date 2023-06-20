import uuid

from src.libs.tuple_space import TupleSpace


def test_tuple_space_start_empty():
    tuple_space = TupleSpace()
    result = tuple_space.read(("foo",))

    assert result is None


def test_write_and_read_tuple_space():
    tuple_space = TupleSpace()
    tuple_space.write(("foo",))
    result = tuple_space.read(("foo",))

    assert result == ("foo",)


def test_read_not_remove_tuple_from_space():
    tuple_space = TupleSpace()
    tuple_space.write(("foo",))
    result = tuple_space.read(("foo",))
    result2 = tuple_space.read(("foo",))

    assert result == ("foo",)
    assert result2 == ("foo",)


def test_take_remove_tuple_from_space():
    tuple_space = TupleSpace()
    tuple_space.write(("foo",))
    result = tuple_space.take(("foo",))
    result2 = tuple_space.read(("foo",))

    assert result == ("foo",)
    assert result2 is None


def test_read_and_take_tuple_with_pattern_int_and_str():
    tuple_space = TupleSpace()
    tuple_space.write(("foo",))
    tuple_space.write((1,))

    result_read_tuple_int = tuple_space.read((int,))
    result_read_tuple_str = tuple_space.read((str,))
    assert result_read_tuple_int == (1,)
    assert result_read_tuple_str == ("foo",)

    result_take_tuple_int = tuple_space.take((int,))
    result_take_tuple_str = tuple_space.take((str,))
    assert result_take_tuple_int == (1,)
    assert result_take_tuple_str == ("foo",)


def test_read_and_take_tuple_with_pattern_uuid():
    tuple_space = TupleSpace()
    example_uuid = uuid.uuid4()
    tuple_space.write((example_uuid,))

    result_tuple_read_uuid = tuple_space.read((uuid.UUID,))
    assert result_tuple_read_uuid == (example_uuid,)

    result_tuple_take_uuid = tuple_space.take((uuid.UUID,))
    assert result_tuple_take_uuid == (example_uuid,)


def test_read_all_tuples_empty():
    tuple_space = TupleSpace()
    result = tuple_space.read_all((str,))

    assert isinstance(result, list)
    assert len(result) == 0


def test_read_all_tuples():
    tuple_space = TupleSpace()
    tuple_space.write(("foo",))
    tuple_space.write(("bar",))
    result = tuple_space.read_all((str,))

    assert isinstance(result, list)
    assert len(result) == 2
    assert ("foo",) in result
    assert ("bar",) in result

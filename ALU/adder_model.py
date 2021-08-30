from cocotb.triggers import ReadWrite


def adder_model(a: int, b: int) -> int:
    """ model of adder """
    return a+b


def sub_model(a, b):
    return a-b


def or_model(a, b):
    return a | b


def and_model(a, b):
    return a & b

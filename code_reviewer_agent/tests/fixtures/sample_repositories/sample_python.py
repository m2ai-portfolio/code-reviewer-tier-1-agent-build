"""Sample Python code with intentional issues for testing."""

import os
import sys
import random  # This should trigger weak random warning


# Hardcoded credentials - SECURITY ISSUE
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
password = "admin123"


def complex_function_with_many_branches(x, y, z, w, v, u):
    """Function with too many parameters and high complexity."""
    # Magic number - STYLE ISSUE
    if x > 100:
        if y < 50:
            if z == 25:
                if w != 0:
                    if v > 10:
                        if u < 5:
                            return x + y + z + w + v + u
                        else:
                            return x - y
                    else:
                        return y + z
                else:
                    return z + w
            else:
                return w + v
        else:
            return v + u
    else:
        return u


def vulnerable_sql_query(user_input):
    """SQL injection vulnerability."""
    query = "SELECT * FROM users WHERE username = '%s'" % user_input
    # This should be flagged as SQL injection risk
    return query


def dangerous_eval_usage(user_code):
    """Using eval is dangerous."""
    result = eval(user_code)  # CRITICAL SECURITY ISSUE
    return result


def function_with_mutable_default(items=[]):
    """Mutable default argument - BAD PRACTICE."""
    items.append("new")
    return items


class GodClass:
    """A class that does too many things."""

    def __init__(self):
        self.data = []
        self.config = {}
        self.cache = {}
        self.stats = {}

    def method1(self):
        pass

    def method2(self):
        pass

    def method3(self):
        pass

    def method4(self):
        pass

    def method5(self):
        pass

    def method6(self):
        pass

    def method7(self):
        pass

    def method8(self):
        pass

    def method9(self):
        pass

    def method10(self):
        pass


# Missing docstring
def undocumented_function():
    x = 42  # Magic number
    return x * 2


# Commented out code - should be removed
# def old_function():
#     return "This is old code"


# Duplicate code
def calculate_sum_a(a, b):
    return a + b


def calculate_sum_b(a, b):
    return a + b


def calculate_sum_c(a, b):
    return a + b


# Weak cryptography
import hashlib


def weak_hash(data):
    """Using MD5 is not secure."""
    return hashlib.md5(data.encode()).hexdigest()


# Unused import (sys is imported but not used)

# This file intentionally contains multiple code quality issues
# for testing the code reviewer agent.
